import subprocess
import time
import sys
import os
import signal
import logging

logger = logging.getLogger("Subprocess")


def _needs_sudo_retry(stderr: str, os_name: str) -> bool:
    """Check if sudo/admin retry is needed based on stderr output."""
    stderr = (stderr or "").lower()

    common_indicators = [
        "failed to connect to local tailscaled",
        "can't connect",
        "permission denied",
        "access denied",
        "connect: permission denied",
        "not permitted",
        "root",
        "requires elevation",
        "is not recognized as an internal or external command",  # for failed pkexec/sudo
    ]

    if os_name.startswith(("linux", "darwin", "win")):
        return any(msg in stderr for msg in common_indicators)

    return False


def check_backg_subp(p, command):
    time.sleep(1)
    retcode = p.poll()
    if retcode is not None:
        stderr = p.stderr.read().decode() if p.stderr else ""
        raise subprocess.CalledProcessError(
            returncode=retcode, cmd=command, stderr=stderr
        )


def safe_subp_run(
    command,
    retries=3,
    timeout=10,
    delay_between_retries=2,
    enable_sudo_retry=False,
    promt="Please enter your password to continue",
    background=False,
    start_new_session=False,
    cli_mode=True,
    force_sudo=False,
    **kwargs,
):
    """
    Runs a subprocess with a timeout and optional retries.
    Optionally retries with sudo or GUI elevation on certain errors (Linux/macOS only).

    :param command: Command list (e.g., ['tailscale', 'up'])
    :param cli_mode: Use CLI sudo instead of GUI pkexec/osascript (default: False)
    :param kwargs: Extra args passed to subprocess.run
    """
    os_name = sys.platform
    last_exception = None

    if os_name.startswith("win"):
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

    for attempt in range(1, retries + 1):
        try:
            if force_sudo:
                raise subprocess.CalledProcessError(
                    cmd=command, stderr="Permission denied", returncode=1
                )
            logger.info(f"[{attempt}/{retries}] Running: {' '.join(command)}")
            if background:
                p = subprocess.Popen(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    start_new_session=start_new_session,
                    **kwargs,
                )
                check_backg_subp(p, command)
            else:
                p = subprocess.run(command, timeout=timeout, **kwargs)
            logger.info(f"✅ Subprocess <{' '.join(command)}> succeeded.")
            return p

        except subprocess.TimeoutExpired as e:
            logger.warning(
                f"[{attempt}] Subprocess: <{' '.join(command)}> Timeout after {timeout}s"
            )
            last_exception = e

        except subprocess.CalledProcessError as e:
            logger.warning(f"[{attempt}] CalledProcessError: {e}. {e.stderr}")
            last_exception = e
            logger.debug(
                f"STDERR: {e.stderr}, STDOUT: {e.stdout}, needs_sudo: {_needs_sudo_retry(e.stderr or '', os_name)}"
            )
            if (
                enable_sudo_retry and _needs_sudo_retry(e.stderr or "", os_name)
            ) or force_sudo:
                try:
                    if cli_mode:
                        subprocess.run(["sudo", "-v"])  # autorize

                        sudo_cmd = ["sudo"] + command
                        logger.info(f"🔁 Retrying with CLI sudo: {' '.join(sudo_cmd)}")
                        if background:
                            p = subprocess.Popen(
                                sudo_cmd,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                **kwargs,
                            )
                            check_backg_subp(p, sudo_cmd)
                        else:
                            p = subprocess.run(sudo_cmd, timeout=timeout, **kwargs)

                        logger.info(f"✅ Subprocess <{' '.join(sudo_cmd)}> succeeded.")
                        return p

                    elif os_name.startswith("darwin"):
                        quoted_cmd = " ".join(command).replace('"', '\\"')
                        applescript = (
                            f'do shell script "{quoted_cmd}" '
                            f"with administrator privileges "
                            f'with prompt "{promt}"'
                        )
                        logger.info(f"🔁 Retrying via AppleScript: {applescript}")
                        osas_cmd = ["osascript", "-e", applescript]
                        if background:
                            p = subprocess.Popen(
                                osas_cmd,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                **kwargs,
                            )
                            check_backg_subp(p, osas_cmd)
                        else:
                            p = subprocess.run(
                                osas_cmd,
                                timeout=timeout,
                                capture_output=True,
                                text=True,
                                **kwargs,
                            )
                        logger.info(f"✅ Subprocess <{' '.join(osas_cmd)}> succeeded.")
                        return p

                    elif os_name.startswith("linux") and cli_mode == False:
                        pkexec_cmd = ["pkexec"] + command
                        logger.info(f"🔁 Retrying via pkexec: {' '.join(pkexec_cmd)}")
                        if background:
                            p = subprocess.Popen(
                                pkexec_cmd,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                **kwargs,
                            )
                            check_backg_subp(p, pkexec_cmd)
                        else:
                            p = subprocess.run(pkexec_cmd, timeout=timeout, **kwargs)

                        logger.info(
                            f"✅ Subprocess <{' '.join(pkexec_cmd)}> succeeded."
                        )
                        return p

                    elif os_name.startswith("win"):
                        ps_command = [
                            "powershell",
                            "-Command",
                            f"Start-Process '{command[0]}' -ArgumentList '{' '.join(command[1:])}' -Verb runAs",
                        ]
                        logger.info(
                            f"🔁 Retrying via PowerShell (admin): {' '.join(ps_command)}"
                        )
                        if background:
                            p = subprocess.Popen(
                                ps_command,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                **kwargs,
                            )
                            check_backg_subp(p, ps_command)
                        else:
                            p = subprocess.run(ps_command, timeout=timeout, **kwargs)
                        logger.info(
                            f"✅ Subprocess <{' '.join(ps_command)}> succeeded."
                        )
                        return p

                except Exception as retry_err:
                    logger.error(f"❌ Retry with elevation failed: {retry_err}")
                    last_exception = retry_err
                    logger.debug(f"STDERR: {last_exception.stderr}")
            else:
                logger.error(f"Unexpected exception: {e}")
                logger.debug(f"STDERR: {e.stderr}")
                return e

        except Exception as e:
            logger.warning(f"[{attempt}] Unexpected exception: {e}")
            last_exception = e
            logger.debug(f"STDERR: {e.stderr}")

        if attempt < retries:
            logger.info(f"Waiting {delay_between_retries}s before retry...")
            time.sleep(delay_between_retries)

    logger.error(f"❌ All attempts failed for command: {' '.join(command)}")
    logger.debug(f"STDERR: {last_exception.stderr}")
    raise last_exception


def kill_background_proc(proc: subprocess.Popen, name=""):
    logger.debug(f"Killing background process {name}")
    if proc and proc.poll() is None:
        try:
            # Сначала пытаемся убить группу процесса (если он лидер группы)
            pgid = os.getpgid(proc.pid)
            if pgid != os.getpgrp():  # чтобы случайно не убить себя
                os.killpg(pgid, signal.SIGTERM)
            else:
                proc.terminate()
        except Exception:
            proc.terminate()

        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                if pgid != os.getpgrp():
                    os.killpg(pgid, signal.SIGKILL)
                else:
                    proc.kill()
            except Exception:
                proc.kill()
            proc.wait()

        logger.debug(f"Background process {name} killed")
