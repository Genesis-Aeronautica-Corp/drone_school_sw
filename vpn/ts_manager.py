import os
import sys
import time
import json
import subprocess
from utils import safe_subp_run
import threading
import logging

from vpn.tsm_state_analysis import (
    is_tailscale_installed,
    get_tailscale_path,
    get_tailscaled_path,
    is_tailscaled_running,
    get_local_tailscale_state,
)
from vpn.tsm_start_flow import tailscale_up, start_win_gui, start_tailscaled
from vpn.tsm_stop_flow import logout, tailscale_down, stop_tailscaled

logger = logging.getLogger("Vpn")


class TSManager:
    def __init__(self, feedback_func=print):
        self.feedback_func = feedback_func

        self.os_code = None
        os_name = sys.platform
        if "linux" in os_name:
            self.os_code = 0
        elif os_name == "darwin":
            self.os_code = 1
        elif "win" in os_name:
            self.os_code = 2

        self.is_installed = threading.Event()
        self.mac_os_gui_flg = threading.Event()
        self.tsd_running = threading.Event()
        self.ts_running = threading.Event()

        self.ts_state_dir = ""
        self.ts_bin_path = ""
        self.tsd_bin_path = ""

        self.analysis_finished = threading.Event()
        self.analysis_failed = threading.Event()

        threading.Thread(target=self.analyze_state, daemon=True).start()

    def analyze_state(self):
        if not is_tailscale_installed(self):
            self.analysis_failed.set()
            logger.error("Analysis failed on is_tailscale_installed")
            return
        if not get_tailscale_path(self):
            self.analysis_failed.set()
            logger.error("Analysis failed on get tailscale path")
            return
        if (
            self.os_code is not None
            and self.os_code < 2
            and not self.mac_os_gui_flg.is_set()
        ):
            if not get_tailscaled_path(self):
                self.analysis_failed.set()
                logger.error("Analysis failed on get tailscaled path")
                return

        is_tailscaled_running(self)

        get_local_tailscale_state(self)

        self.analysis_finished.set()
        logger.info("Analysis finished")

    def start(self, auth_token, hostname):
        if self.ts_running.is_set():
            logger.error("Tailscale is already running")
            return False

        while not self.analysis_failed.is_set() and not self.analysis_finished.is_set():
            time.sleep(0.1)
        if self.analysis_failed.is_set():
            logger.error("Can't start tailscale - analysis has failed")
            return False

        if (self.status() or {}).get("BackendState") == "Running":
            self.stop()

        if not logout(self):
            logger.error("Can't logout from tailscale")

        is_tailscaled_running(self)
        if not self.tsd_running.is_set():
            if not start_tailscaled(self):
                return False
            time.sleep(3)

        if self.os_code == 2:
            start_win_gui(
                self
            )  # Run GUI app (without it process doesn't work properly on WIN)

        res = tailscale_up(self, auth_token, hostname)

        """
        correct_conn = False
        if res == 'ok':
            for i in range(n_retries): # wait till the our hostname appear in tailscale status
                correct_conn = self.check_connection(hostname)
                if correct_conn:
                    break
                time.sleep(retry_delay)
        """

        if res != "ok":  # res == 'needs_reset' or (not correct_conn and res == 'ok'):
            logger.warning("Can't connect most likely to accounts conflict")
            # if self.feedback_func:
            #    self.feedback_func("Looks like you are already logged in Tailscale with another account. Please try again.")
            self.stop()
            return False
        else:
            return res == "ok"

    def stop(self):
        try:
            logout(self)
            tailscale_down(self)
            logger.info("TSM stopped")
            return True
        except Exception as e:
            logger.error(f"Can't stop TSM: {e}")
            return False

    def close(self):
        try:
            self.stop()

            if (
                not self.mac_os_gui_flg.is_set() and self.os_code == 1
            ) or self.os_code == 0:
                if stop_tailscaled(self):
                    logger.info("tailscaled daemon process stopped.")
                else:
                    logger.warning(
                        "tailscaled was not running or could not be stopped."
                    )
            else:
                logger.warning("Don't stop tailscaled on Win/MacosGUI")
            logger.info("TSM Closed")
            return True
        except Exception as e:
            logger.error(f"Can't close TSM: {e}")
            return False

    def check_connection(self, hostname):
        # tailscale status --json --peers=false | jq -r .Self.DNSName
        cmd = [self.ts_bin_path, "status", "--json", "--peers=false"]
        try:
            logger.debug(f"Check cmd: {cmd}")
            result = safe_subp_run(
                cmd, check=True, capture_output=True, text=True, timeout=5
            ).stdout
            logger.debug(f"{result}")
            return hostname in json.loads(result)["Self"]["DNSName"]
        except Exception as e:
            logger.error(f"Failed to check connection: {e}")
            return False

    def status(self, json_flg=True):
        cmd = [self.ts_bin_path, "status"] + ["--json"] * json_flg
        try:
            logger.debug(f"Status cmd: {cmd}")
            result = safe_subp_run(
                cmd, check=True, capture_output=True, text=True, timeout=5
            ).stdout
            return json.loads(result) if json_flg else result

        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Error executing tailscale: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"[!] Failed to parse tailscale JSON output: {e}")
        except Exception as e:
            logger.error(f"[!] Unexpected error: {e}")

        return None

    # === Get IPs ===
    def get_tailscale_ip_by_hostname(
        self, hostname: str, peer_flg: bool = True
    ) -> str | None:
        """Get Tailscale IP for a given peer or local host by hostname."""
        data = self.status()
        if not data:
            return None

        logger.debug(f"{data}")

        if peer_flg:
            peers = data.get("Peer", {}) or data.get("Peer[]", {})
            for peer_data in peers.values():
                if peer_data.get("HostName", "").split(".")[0] == hostname:
                    ips = peer_data.get("TailscaleIPs", [])
                    ipv4s = [ip for ip in ips if "." in ip]
                    logger.info(f"Retrieved IPs {ipv4s} for hostname {hostname}")
                    return ipv4s[0] if ipv4s else None
        else:
            self_data = data.get("Self", {})
            if self_data.get("HostName", "").split(".")[0] == hostname:
                ips = self_data.get("TailscaleIPs", [])
                ipv4s = [ip for ip in ips if "." in ip]
                logger.info(f"Retrieved self IPs {ipv4s} for hostname {hostname}")
                return ipv4s[0] if ipv4s else None


# Test
if __name__ == "__main__":
    tsm = TSManager()
    if len(sys.argv) > 1 and sys.argv[1] == "up":
        res = tsm.start(os.getenv("TEST_CLIENT_AUTH_KEY"), "test")
        print(f"{res} Start:\n\n{tsm.status(False)}\n\n")
    elif len(sys.argv) > 1 and sys.argv[1] == "status":
        time.sleep(3)
        print(f"Status:\n\n{tsm.status(False)}\n\n")
    elif len(sys.argv) > 1 and sys.argv[1] == "down":
        time.sleep(3)
        tsm.stop()
    elif len(sys.argv) > 1 and sys.argv[1] == "org":
        res = tsm.start(os.getenv("TEST_TS_ORG_KEY"), "test-client")
        print(f"{res} Start:\n\n{tsm.status(False)}\n\n")
    else:
        tsm = TSManager()
        res = tsm.start(os.getenv("TEST_CLIENT_AUTH_KEY"), "test")
        print(f"{res} Start:\n\n{tsm.status(False)}\n\n")
        tsm.stop()
        print(f"Stop:\n\n{tsm.status(False)}\n\n")
        res = tsm.start(os.getenv("TEST_CLIENT_AUTH_KEY"), "test")
        print(f"{res} Start:\n\n{tsm.status(False)}\n\n")
        tsm.stop()
        print(f"Stop:\n\n{tsm.status(False)}\n\n")
        tsm.close()
        print(f"Close:\n\n{tsm.status(False)}\n\n")

    if len(sys.argv) > 1 and sys.argv[1] == "relogin":
        print("Relogin\n\n")
        tsm = None
        tsm = TSManager()
        # Test relogin over the old (foreign) account
        res = tsm.start(os.getenv("TEST_TS_ORG_KEY"), "test-client")
        print(f"{res} Start:\n\n{tsm.status(False)}\n\n")
        tsm.stop()
        print(f"Stop:\n\n{tsm.status(False)}\n\n")
        tsm.close()
        print(f"Close:\n\n{tsm.status(False)}\n\n")
