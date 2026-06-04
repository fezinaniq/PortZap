from __future__ import annotations

from typing import List, Optional

from rich.text import Text
from textual.widgets import DataTable

from ..core.models import PortEntry


COLUMNS: list[tuple[str, int]] = [
    ("PORT",    6),
    ("PROTO",   6),
    ("STATUS",  13),
    ("PID",     7),
    ("PROCESS", 20),
    ("USER",    12),
    ("LOCAL",   22),
    ("REMOTE",  22),
]

# Maps column key → PortEntry attribute name
COL_TO_ATTR: dict[str, str] = {
    "port":    "port",
    "proto":   "protocol",
    "status":  "status",
    "pid":     "pid",
    "process": "process_name",
    "user":    "username",
    "local":   "local_address",
    "remote":  "remote_address",
}


def _make_sort_key(attr: str):
    """Returns a sort key function for the given PortEntry attribute."""
    def key(entry: PortEntry):
        val = getattr(entry, attr, "")
        return val if isinstance(val, int) else str(val).lower()
    return key


class PortTable(DataTable):
    BINDINGS = []  # key handling lives in the parent App

    sort_col: str = "port"
    sort_asc: bool = True

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True
        self._refresh_columns()

    def _refresh_columns(self) -> None:
        """Clear everything and re-add column headers with the current sort indicator."""
        self.clear(columns=True)
        for label, width in COLUMNS:
            key = label.lower()
            if key == self.sort_col:
                indicator = " ▲" if self.sort_asc else " ▼"
                display = f"{label}{indicator}"
            else:
                display = label
            self.add_column(display, width=width, key=key)

    def set_sort(self, col: str, asc: bool) -> None:
        """Update sort state and refresh column headers."""
        self.sort_col = col
        self.sort_asc = asc
        self._refresh_columns()

    def populate(self, entries: List[PortEntry], query: str = "") -> None:
        """Filter, sort, and render entries into the table."""
        self.clear()  # rows only — columns keep their indicators
        filtered = self._filter(entries, query)
        attr = COL_TO_ATTR.get(self.sort_col, "port")
        filtered = sorted(filtered, key=_make_sort_key(attr), reverse=not self.sort_asc)
        for entry in filtered:
            status_text = Text(entry.display_status, style=f"bold {entry.status_color}")
            self.add_row(
                str(entry.port),
                entry.protocol,
                status_text,
                str(entry.pid) if entry.pid else "?",
                entry.process_name,
                entry.username,
                entry.local_address,
                entry.display_remote,
                key=f"{entry.pid}:{entry.port}:{entry.protocol}",
            )

    @staticmethod
    def _filter(entries: List[PortEntry], query: str) -> List[PortEntry]:
        if not query:
            return entries
        q = query.lower()
        return [
            e for e in entries
            if q in str(e.port)
            or q in e.process_name.lower()
            or q in e.protocol.lower()
            or q in e.status.lower()
            or q in e.username.lower()
        ]

    def selected_entry(self, entries: List[PortEntry], query: str = "") -> Optional[PortEntry]:
        """Return the PortEntry under the cursor, respecting current sort + filter."""
        attr = COL_TO_ATTR.get(self.sort_col, "port")
        filtered = sorted(
            self._filter(entries, query),
            key=_make_sort_key(attr),
            reverse=not self.sort_asc,
        )
        try:
            row_index = self.cursor_row
            if 0 <= row_index < len(filtered):
                return filtered[row_index]
        except Exception:
            pass
        return None
