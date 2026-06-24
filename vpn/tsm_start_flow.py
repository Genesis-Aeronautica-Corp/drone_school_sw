import time
import subprocess
import logging

from utils.safe_subprocess import safe_subp_run

logger = logging.getLogger("Vpn")


def start_tailscaled(self) -> bool:
    """Start tailscaled (CLI), GUI (macOS), or Tailscale service (Windows) if needed."""

    logger.info("tailscaled - attempting to start")

    # --- Windows: Start Tailscale service
    if self.os_code == 2:  # Windows
        logger.info("Detected Windows — trying to start Tailscale service")

        try:
            # Try to start the service
            start_cmd = ["powershell", "-Command", "Start-Service Tailscale"]
            safe_subp_run(start_cmd, check=True)
            logger.info("✅ Tailscale service started on Windows")

            # Give some time for tailscaled to initialize
            for _ in range(10):
                self.is_tailscaled_running()
                time.sleep(1.5)
                if self.tsd_running.is_set():
                    logger.info("tailscaled is now running")
                    return True

            logger.error("tailscaled did not respond after service start")
            return False

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to start Tailscale service: {e}")
            return False

    # --- macOS GUI-путь
    if self.os_code == 1 and self.mac_os_gui_flg.is_set():
        try:
            safe_subp_run(command=["open", "-a", self.ts_bin_path], background=True)
            logger.info("Tailscale GUI launched to trigger tailscaled")
            for _ in range(10):
                self.is_tailscaled_running()
                time.sleep(1.5)
                if self.tsd_running.is_set():
                    logger.info("tailscaled started via GUI")
                    return True
            logger.error("tailscaled did not start after GUI launch")
            return False
        except Exception as e:
            logger.error(f"Failed to open Tailscale GUI: {e}")
            return False

    # --- CLI tailscaled (Linux, etc.)
    if not self.tsd_bin_path:
        logger.error("❌ tailscaled binary not found.")
        return False

    try:
        logger.info(f"🚀 Starting tailscaled via: {self.tsd_bin_path}")
        shell_cmd = [self.tsd_bin_path, "--state=mem:"]

        safe_subp_run(
            shell_cmd,
            retries=3,
            timeout=45,
            delay_between_retries=3,
            enable_sudo_retry=True,
            background=True,
            stdin=subprocess.DEVNULL,
            force_sudo=True,
            promt="Please enter your password to run Tailscale",
        )

        for _ in range(10):
            self.is_tailscaled_running()
            time.sleep(1.5)
            if self.tsd_running.is_set():
                logger.info("tailscaled is now running")
                return True

        logger.error("tailscaled did not start within timeout.")
        return False

    except Exception as e:
        logger.error(f"❌ Failed to start tailscaled: {e}")
        return False


def start_win_gui(self):
    if self.os_code != 2:
        return
    try:
        output = subprocess.check_output(
            ["tasklist"],
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,  # type: ignore
        )
        if "tailscale-ipn.exe" in output:
            return
    except subprocess.CalledProcessError:
        return

    start_cmd = [self.ts_bin_path.replace("tailscale.exe", "tailscale-ipn.exe")]
    safe_subp_run(
        start_cmd,
        background=True,
        stdin=subprocess.DEVNULL,
    )
    logger.info("Start tailscale IPN")


def tailscale_up(self, auth_token, hostname):
    cmd = [
        self.ts_bin_path,
        "up",
        f"--authkey={auth_token}",
        f"--hostname={hostname}",
        "--reset",
    ]

    try:
        logger.info(f"Starting tailscale for {hostname}")
        safe_subp_run(
            cmd,
            retries=1,
            timeout=30,
            delay_between_retries=3,
            check=True,
            capture_output=True,
            text=True,
            shell=self.os_code == 2,
            enable_sudo_retry=True,
            promt="Please enter your password to run Tailscale",
        )
        print("Tailscale started.")
        logger.info(f"{hostname} Tailscale start succeeded on {self.os_code}")
        self.ts_running.set()
        return "ok"

    except subprocess.TimeoutExpired:
        logger.error("Timeout in tailscale up")
        return "needs_reset"

    except Exception as e:
        logger.error(f"Tailscale start failed with Exception {e}", exc_info=True)
        return "error"
