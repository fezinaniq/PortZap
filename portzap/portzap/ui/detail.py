"""
portzap.ui.detail
-----------------
Side panel showing full details of the selected PortEntry.
"""
from __future__ import annotations

from typing import Optional

from rich.text import Text
from textual.app import ComposeResult
from textual.widgets import Static
from textual.reactive import reactive

from ..core.models import PortEntry


_EMPTY = """[dim]Press [bold]i[/bold] on a row to inspect a process.[/dim]"""


def _render(entry: PortEntry) -> str:
    lines = [
        f"[bold cyan]── Process Detail ─────────────────────[/bold cyan]",
        f"",
        f"[bold]Process[/bold]   {entry.process_name}",
        f"[bold]PID[/bold]       {entry.pid}",
        f"[bold]User[/bold]      {entry.username}",
        f"",
        f"[bold]Port[/bold]      {entry.port}",
        f"[bold]Protocol[/bold]  {entry.protocol}",
        f"[bold]Status[/bold]    [{entry.status_color}]{entry.display_status}[/{entry.status_color}]",
        f"",
        f"[bold]Local[/bold]     {entry.local_address}",
        f"[bold]Remote[/bold]    {entry.display_remote}",
        f"",
        f"[bold]Command[/bold]",
        f"[dim]{entry.command}[/dim]",
        f"",
        f"[dim]Press [bold]k[/bold] to kill · [bold]i[/bold] to close[/dim]",
    ]
    return "\n".join(lines)


class DetailPane(Static):
    """Renders process details in a side panel."""

    DEFAULT_CSS = """
    DetailPane {
        width: 42;
        padding: 1 2;
        border: tall $accent;
        background: $surface;
    }
    """

    _entry: Optional[PortEntry] = None

    def show(self, entry: PortEntry) -> None:
        self._entry = entry
        self.update(_render(entry))
        self.display = True

    def hide(self) -> None:
        self._entry = None
        self.update(_EMPTY)
        self.display = False

    def current_entry(self) -> Optional[PortEntry]:
        return self._entry
