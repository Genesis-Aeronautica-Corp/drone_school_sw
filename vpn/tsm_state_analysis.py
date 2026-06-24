import os

import shutil
from pathlib import Path
from utils.safe_subprocess import safe_subp_run

import logging

logger = logging.getLogger("Vpn")


def is_tailscale_installed(self) -> str | bool:
    """Determine whether Tailscale is installed (CLI, macOS GUI, or both)."""
    logger.info("Check whether tailscale is installed")

    if self.os_code == 2:
        try:
            logger.info("Searching TS on win")
            result = safe_subp_run(
                ["where", "tailscale"], capture_output=True, text=True
            )
            if result.returncode == 0:
                self.is_installed.set()
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Can't find tailscale on win: {e}")
            return False

    if self.os_code == 1:
        logger.info("Searching TS on mac gui")
        gui_path = self.find_gui_tailscale_path_macos()
        if gui_path and os.path.exists(gui_path):
            self.is_installed.set()
            self.mac_os_gui_flg.set()
            return True
        else:
            logger.debug("Macos GUI Tailscale Client not found")

        # brew fallback
        for brew_path in ["/opt/homebrew/bin/tailscale", "/usr/local/bin/tailscale"]:
            if os.path.exists(brew_path):
                logger.debug(f"Found tailscale binary on macos: {brew_path}")
                self.ts_bin_path = brew_path
                self.is_installed.set()
                return True
        logger.debug("No tailscale binaries found on macos")

    if shutil.which("tailscale"):
        self.is_installed.set()
        return True

    return False


def find_gui_tailscale_path_macos(self) -> str | None:
    """Try to locate the macOS GUI Tailscale binary via Spotlight or standard folders."""
    try:
        result = safe_subp_run(
            ["mdfind", "kMDItemCFBundleIdentifier == 'com.tailscale.ipn.macsys'"],
            capture_output=True,
            text=True,
        )
        for app_path in result.stdout.strip().splitlines():
            candidate = os.path.join(app_path, "Contents", "MacOS", "Tailscale")
            if os.path.exists(candidate):
                self.ts_bin_path = candidate
                return candidate
    except Exception:
        logger.error("Can't find GUI Tailscale path on macos")

    possible_dirs = [
        "/Applications",
        os.path.expanduser("~/Applications"),
        os.path.expanduser("~/Downloads"),
        "/Users/Shared",
    ]

    for directory in possible_dirs:
        if not os.path.exists(directory):
            continue
        for item in os.listdir(directory):
            if item.lower().startswith("tailscale") and item.endswith(".app"):
                candidate = os.path.join(
                    directory, item, "Contents", "MacOS", "Tailscale"
                )
                if os.path.exists(candidate):
                    self.ts_bin_path = candidate
                    return candidate

    fallback = os.getenv(
        "MAC_GUI_TAILSCALE_PATH", "/Applications/Tailscale.app/Contents/MacOS/Tailscale"
    )
    candidate = fallback if os.path.exists(fallback) else None
    self.ts_bin_path = candidate
    return candidate


def get_tailscale_path(self) -> str | None:
    """Locate the Tailscale CLI binary based on platform."""
    logger.info("Try to find tailscale binary on the system")

    if self.ts_bin_path:
        logger.debug(f"Tailscale path: {self.ts_bin_path}")
        return self.ts_bin_path

    if self.os_code == 2:
        try:
            result = safe_subp_run(
                ["where", "tailscale"], capture_output=True, text=True
            )
            if result.returncode == 0:
                path = result.stdout.strip().splitlines()[0]
                if os.path.exists(path):
                    self.ts_bin_path = path
                    logger.debug(f"Tailscale path: {self.ts_bin_path}")
                    return path
        except Exception as e:
            logger.error(f"Can't get tailscale path: {e}")
            return None

    found = shutil.which("tailscale")
    if found and os.path.exists(found):
        self.ts_bin_path = found
        logger.debug(f"Tailscale path: {self.ts_bin_path}")
        return found

    logger.error("Tailscale binary not found on this system.")
    return None


def get_tailscaled_path(self):
    """Find the tailscaled binary if available (Linux/macOS only)."""
    if self.os_code < 2 and self.mac_os_gui_flg.is_set():
        logger.info("Skip finding tailscale MacOS gui")
        return None

    logger.info("Try to find tailscaled binary on the system")
    path = shutil.which("tailscaled")
    if path and os.path.exists(path):
        self.tsd_bin_path = path
        logger.debug(f"Tailscaled path: {self.tsd_bin_path}")
        return path

    fallback_paths = [
        "/opt/homebrew/bin/tailscaled",  # Apple Silicon
        "/usr/local/bin/tailscaled",
        str(Path.home() / os.getenv("TAILSCALED_PATH", ".homebrew/bin/tailscaled")),
    ]
    for alt_path in fallback_paths:
        if os.path.exists(alt_path):
            self.tsd_bin_path = path
            logger.debug(f"Tailscaled path: {self.tsd_bin_path}")
            return alt_path

    return None


def is_tailscaled_running(self) -> bool:
    """Check if tailscaled (or Tailscale service) is running on this platform."""
    running = False
    try:
        if self.os_code < 2:
            # Unix: use pgrep
            result = safe_subp_run(
                ["pgrep", "tailscale"], capture_output=True, text=True
            )
            running = result.returncode == 0
            logger.debug(f"[Unix] tailscaled running: {running}")

        elif self.os_code == 2:
            # Windows: check service status
            result = safe_subp_run(
                [
                    "powershell",
                    "-Command",
                    "Get-Service Tailscale | Select-Object -ExpandProperty Status",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )
            running = result.returncode == 0 and "Running" in result.stdout
            logger.debug(f"[Windows] Tailscale service running: {running}")

        else:
            logger.warning(f"Unknown system: {self.os_code}")
            running = False

        if running:
            self.tsd_running.set()
        else:
            self.tsd_running.clear()

        logger.info(f"Is tailscale installed: {running}")
        return running

    except Exception as e:
        logger.warning(f"Error checking tailscaled status on {self.os_code}: {e}")
        self.tsd_running.clear()
        return False


def get_local_tailscale_state(self):
    if self.os_code == 2:
        base = Path("C:\\ProgramData\\Tailscale")
    elif self.os_code == 1:
        base = Path("/Library/Tailscale/")
    elif self.os_code == 0:
        base = Path("/var/lib/tailscale")
    else:
        return None

    logger.debug(f"Base state path: {base}")

    if base.exists():
        logger.info(f"State data found in {base}")
        self.ts_state_dir = base
        return True

    logger.info("No state data was found")
    return False
