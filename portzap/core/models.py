from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PortEntry:
    port: int
    pid: int
    process_name: str
    protocol: str          # TCP / UDP
    status: str            # LISTEN / ESTABLISHED / TIME_WAIT / etc.
    local_address: str
    remote_address: str
    username: str
    command: str           # Full command that opened this port

    @property
    def status_color(self) -> str:
        """Return a Rich color name for this status."""
        return {
            "LISTEN":      "green",
            "ESTABLISHED": "cyan",
            "TIME_WAIT":   "yellow",
            "CLOSE_WAIT":  "magenta",
            "FIN_WAIT1":   "red",
            "FIN_WAIT2":   "red",
            "SYN_SENT":    "blue",
            "SYN_RECV":    "blue",
            "CLOSED":      "dim white",
            "NONE":        "dim white",
        }.get(self.status.upper(), "white")

    @property
    def display_status(self) -> str:
        return self.status if self.status else "—"

    @property
    def display_remote(self) -> str:
        return self.remote_address if self.remote_address and self.remote_address != "0.0.0.0:0" else "—"
