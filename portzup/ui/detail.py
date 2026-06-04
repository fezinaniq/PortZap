from __future__ import annotations

from typing import Optional

from rich.text import Text
from textual.widgets import Static

from ..core.models import PortEntry


_EMPTY = "[dim]Press [bold]i[/bold] on a row to inspect a process.[/dim]"


def _render(entry: PortEntry) -> str:
    c = entry.status_color
    lines = [
        "[bold cyan]── Process Detail ─────────────────────[/bold cyan]",
        "",
        f"[bold]Process[/bold]   {entry.process_name}",
        f"[bold]PID[/bold]       {entry.pid}",
        f"[bold]User[/bold]      {entry.username}",
        "",
        f"[bold]Port[/bold]      {entry.port}",
        f"[bold]Protocol[/bold]  {entry.protocol}",
        f"[bold]Status[/bold]    [{c}]{entry.display_status}[/{c}]",
        "",
        f"[bold]Local[/bold]     {entry.local_address}",
        f"[bold]Remote[/bold]    {entry.display_remote}",
        "",
        "[bold]Command[/bold]",
        f"[dim]{entry.command}[/dim]",
        "",
        "[dim]Press [bold]k[/bold] to kill · [bold]i[/bold] to close[/dim]",
    ]
    return "\n".join(lines)


class DetailPane(Static):
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
