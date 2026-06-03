"""
portzap.ui.footer
-----------------
Slim status bar showing key bindings and live feedback.
"""
from __future__ import annotations

from textual.widgets import Static


_HINTS = (
    "[bold]/[/bold] search  "
    "[bold]k[/bold] kill  "
    "[bold]i[/bold] inspect  "
    "[bold]r[/bold] refresh  "
    "[bold]s[/bold] sort  "
    "[bold]q[/bold] quit  "
    "[bold]?[/bold] help"
)


class StatusBar(Static):
    """Bottom bar: key hints + live status messages."""

    DEFAULT_CSS = """
    StatusBar {
        dock: bottom;
        height: 1;
        padding: 0 1;
        background: $accent-darken-2;
        color: $text;
    }
    """

    def on_mount(self) -> None:
        self.update(_HINTS)

    def set_status(self, message: str, style: str = "bold green") -> None:
        self.update(f"[{style}]{message}[/{style}]  {_HINTS}")

    def clear_status(self) -> None:
        self.update(_HINTS)
