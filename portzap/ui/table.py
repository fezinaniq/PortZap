from __future__ import annotations

from typing import List, Optional

from rich.text import Text
from textual.widgets import DataTable

from ..core.models import PortEntry


# (header label, column width) — order matches add_row() calls in populate()
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


class PortTable(DataTable):
    BINDINGS = []  # key handling lives in the parent App

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True
        for label, width in COLUMNS:
            self.add_column(label, width=width, key=label.lower())

    def populate(self, entries: List[PortEntry], query: str = "") -> None:
        self.clear()
        for entry in self._filter(entries, query):
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
        filtered = self._filter(entries, query)
        try:
            row_index = self.cursor_row
            if 0 <= row_index < len(filtered):
                return filtered[row_index]
        except Exception:
            pass
        return None
