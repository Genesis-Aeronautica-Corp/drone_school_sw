from utils import safe_subp_run
import logging

logger = logging.getLogger("Vpn")


def tailscale_down(self):
    """Disconnect from Tailscale and stop tailscaled if needed."""

    cmd = [self.ts_bin_path, "down"]
    shell_flag = self.os_code == 2

    logger.info("Disconnecting from Tailnet...")
    print("Disconnecting from Tailnet...")
    try:
        safe_subp_run(
            cmd,
            retries=3,
            timeout=45,
            delay_between_retries=3,
            check=True,
            capture_output=True,
            text=True,
            shell=shell_flag,
            enable_sudo_retry=True,
            promt="Please enter your password to finish Tailscale",
        )
        print("Tailscale VPN disconnected.")
        logger.info("Tailscale VPN disconnected")
        self.ts_running.clear()

    except Exception as e:
        print("Unexpected error while disconnecting Tailscale:", e)
        logger.exception(f"Unexpected error during Tailscale disconnect: {e}")


def stop_tailscaled(self) -> bool:
    """Stop tailscaled process via sudo kill."""
    try:
        result = safe_subp_run(["pgrep", "tailscaled"], capture_output=True, text=True)
        if result.returncode != 0:
            return False

        for pid in result.stdout.strip().split():
            safe_subp_run(
                ["kill", pid],
                retries=3,
                timeout=45,
                delay_between_retries=3,
                check=True,
                capture_output=True,
                text=True,
                enable_sudo_retry=True,
                promt="Please enter your password to finish Tailscaled daemon",
            )
        logger.info("Tailscaled was killed")
        self.tsd_running.clear()
        return True
    except Exception as e:
        logger.warning(f"Could not stop tailscaled: {e}")
        return False


def logout(self) -> bool:
    """Logs out user from his current tailnet"""
    try:
        logger.info("Logging out")
        return (
            safe_subp_run(
                [self.ts_bin_path, "logout"],
                enable_sudo_retry=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            ).returncode
            == 0
        )
    except Exception as e:
        logger.error(f"Can't logout user from TSnet: {e}")
        return False
