"""
portzap.core.ports
------------------
Fetch all open network connections from the OS using psutil.
Returns a list of PortEntry objects.
"""
from __future__ import annotations

import socket
import psutil
from typing import List

from .models import PortEntry


def _safe_proc_info(pid: int) -> tuple[str, str, str]:
    """Return (process_name, username, command) safely — a dead/gone process won't crash us."""
    try:
        proc = psutil.Process(pid)
        with proc.oneshot():
            name    = proc.name() or "?"
            user    = proc.username() or "?"
            try:
                cmdline = " ".join(proc.cmdline()) or name
            except (psutil.AccessDenied, psutil.ZombieProcess):
                cmdline = name
        return name, user, cmdline
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "?", "?", "?"


def fetch_ports() -> List[PortEntry]:
    """Return all open TCP/UDP connections as PortEntry objects."""
    entries: List[PortEntry] = []
    seen: set[tuple] = set()

    # Build pid → conn mapping via net_connections for speed
    try:
        connections = psutil.net_connections(kind="inet")
    except psutil.AccessDenied:
        connections = []

    for conn in connections:
        if not conn.laddr:
            continue

        port  = conn.laddr.port
        pid   = conn.pid or 0
        proto = "UDP" if conn.type == socket.SOCK_DGRAM else "TCP"

        local_addr  = f"{conn.laddr.ip}:{conn.laddr.port}"
        remote_addr = (
            f"{conn.raddr.ip}:{conn.raddr.port}"
            if conn.raddr else "—"
        )
        status = conn.status if conn.status else "NONE"

        # Deduplicate (same pid + port + proto)
        key = (pid, port, proto)
        if key in seen:
            continue
        seen.add(key)

        name, user, command = _safe_proc_info(pid)

        entries.append(
            PortEntry(
                port=port,
                pid=pid,
                process_name=name,
                protocol=proto,
                status=status,
                local_address=local_addr,
                remote_address=remote_addr,
                username=user,
                command=command,
            )
        )

    # Sort by port number ascending
    entries.sort(key=lambda e: e.port)
    return entries
