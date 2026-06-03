"""
portzap.core.killer
-------------------
Safely kill a process by PID.
Returns (success: bool, message: str).
"""
from __future__ import annotations

import os
import signal
import psutil


def kill_process(pid: int) -> tuple[bool, str]:
    """
    Attempt to terminate a process gracefully (SIGTERM), then forcefully (SIGKILL).
    Returns (True, message) on success or (False, error_message) on failure.
    """
    if pid <= 0:
        return False, f"Invalid PID: {pid}"

    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()

        # Try SIGTERM first
        proc.terminate()
        try:
            proc.wait(timeout=3)
            return True, f"Terminated '{proc_name}' (PID {pid})"
        except psutil.TimeoutExpired:
            # Fall back to SIGKILL
            proc.kill()
            proc.wait(timeout=2)
            return True, f"Killed '{proc_name}' (PID {pid}) with SIGKILL"

    except psutil.NoSuchProcess:
        return False, f"PID {pid} no longer exists"
    except psutil.AccessDenied:
        return False, f"Permission denied — try running portzap with sudo"
    except Exception as exc:
        return False, f"Unexpected error: {exc}"
