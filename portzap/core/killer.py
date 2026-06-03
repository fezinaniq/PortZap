from __future__ import annotations

import psutil


def kill_process(pid: int) -> tuple[bool, str]:
    if pid <= 0:
        return False, f"Invalid PID: {pid}"

    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()

        proc.terminate()
        try:
            proc.wait(timeout=3)
            return True, f"Terminated '{proc_name}' (PID {pid})"
        except psutil.TimeoutExpired:
            # SIGTERM didn't land in time; escalate to SIGKILL
            proc.kill()
            proc.wait(timeout=2)
            return True, f"Killed '{proc_name}' (PID {pid}) with SIGKILL"

    except psutil.NoSuchProcess:
        return False, f"PID {pid} no longer exists"
    except psutil.AccessDenied:
        return False, "Permission denied — try running portzap with sudo"
    except Exception as exc:
        return False, f"Unexpected error: {exc}"
