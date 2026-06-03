from dataclasses import dataclass
from typing import Optional


# Maps TCP state strings to Rich color names used in the table and detail pane.
_STATUS_COLORS: dict[str, str] = {
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
}


@dataclass
class PortEntry:
    port:           int
    pid:            int
    process_name:   str
    protocol:       str   # "TCP" or "UDP"
    status:         str   # LISTEN / ESTABLISHED / TIME_WAIT / etc.
    local_address:  str
    remote_address: str
    username:       str
    command:        str   # full argv[0..n] of the owning process

    @property
    def status_color(self) -> str:
        return _STATUS_COLORS.get(self.status.upper(), "white")

    @property
    def display_status(self) -> str:
        return self.status or "—"

    @property
    def display_remote(self) -> str:
        if self.remote_address and self.remote_address != "0.0.0.0:0":
            return self.remote_address
        return "—"
