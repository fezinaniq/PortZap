"""
portzup.main
------------
Entry point. Runs the Textual application.
"""
from __future__ import annotations

from typing import List

from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import ModalScreen
from textual.widgets import DataTable, Header, Input, Static

from .config import config
from .core.killer import kill_process
from .core.models import PortEntry
from .core.ports import fetch_ports
from .ui.detail import DetailPane
from .ui.footer import StatusBar
from .ui.table import COLUMNS, COL_TO_ATTR, PortTable


# ─────────────────────────── Help Modal ────────────────────────────

HELP_TEXT = """\
[bold cyan]portzup[/bold cyan] — keybindings

[bold]↑ / ↓[/bold]      Navigate the port list
[bold]Click header[/bold] Sort by that column (click again to reverse)
[bold]/[/bold]          Open search / filter
[bold]Escape[/bold]     Clear search / close panel
[bold]k[/bold]          Kill selected process
[bold]i[/bold]          Toggle process detail pane
[bold]r[/bold]          Force refresh
[bold]s[/bold]          Cycle sort column (keyboard shortcut)
[bold]q[/bold]          Quit portzup
[bold]?[/bold]          Show this help

[dim]Colours: [green]LISTEN[/green]  [cyan]ESTABLISHED[/cyan]  [yellow]TIME_WAIT[/yellow]  [magenta]CLOSE_WAIT[/magenta][/dim]
"""


class HelpScreen(ModalScreen):
    BINDINGS = [Binding("escape,q,?", "dismiss", "Close")]

    def compose(self) -> ComposeResult:
        yield Static(HELP_TEXT, id="help-box")

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }
    #help-box {
        width: 56;
        padding: 2 3;
        border: double $accent;
        background: $surface;
    }
    """


# ─────────────────────────── Kill Confirm ───────────────────────────

class KillConfirmScreen(ModalScreen[bool]):
    def __init__(self, entry: PortEntry) -> None:
        super().__init__()
        self._entry = entry

    BINDINGS = [
        Binding("y", "confirm", "Yes"),
        Binding("n,escape", "cancel", "No"),
    ]

    def compose(self) -> ComposeResult:
        e = self._entry
        yield Static(
            f"[bold red]Kill process?[/bold red]\n\n"
            f"[bold]{e.process_name}[/bold]  PID {e.pid}  port [bold cyan]{e.port}[/bold cyan]\n\n"
            f"[dim]{e.command[:60]}{'…' if len(e.command) > 60 else ''}[/dim]\n\n"
            f"Press [bold]y[/bold] to confirm · [bold]n / Esc[/bold] to cancel",
            id="confirm-box",
        )

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)

    DEFAULT_CSS = """
    KillConfirmScreen { align: center middle; }
    #confirm-box {
        width: 52;
        padding: 2 3;
        border: double red;
        background: $surface;
    }
    """


# ────────────────────────── Main App ────────────────────────────────

# All column keys in order, used by the `s` keyboard shortcut
_ALL_COLS = [label.lower() for label, _ in COLUMNS]


class PortzupApp(App):
    """portzup — beautiful TUI port manager."""

    TITLE = "portzup 🔌"
    CSS = """
    Screen {
        layout: vertical;
    }
    #search-bar {
        height: 3;
        dock: top;
        display: none;
    }
    #search-bar.visible {
        display: block;
    }
    #main-row {
        height: 1fr;
    }
    PortTable {
        width: 1fr;
    }
    DetailPane {
        display: none;
    }
    DetailPane.visible {
        display: block;
    }
    """

    BINDINGS = [
        Binding("q",             "quit",        "Quit",    show=False),
        Binding("k",             "kill",         "Kill",    show=False),
        Binding("i",             "inspect",      "Inspect", show=False),
        Binding("r",             "refresh",      "Refresh", show=False),
        Binding("s",             "sort_toggle",  "Sort",    show=False),
        Binding("/",             "search",       "Search",  show=False),
        Binding("escape",        "escape",       "Escape",  show=False),
        Binding("question_mark", "help",         "Help",    show=False),
    ]

    _entries:     List[PortEntry] = []
    _search_open: bool = False
    _detail_open: bool = False
    _query:       str = ""

    # ── compose ──────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Input(placeholder="Filter by port, process, status…", id="search-bar")
        with Horizontal(id="main-row"):
            yield PortTable(id="port-table")
            yield DetailPane(id="detail-pane")
        yield StatusBar(id="status-bar")

    # ── lifecycle ─────────────────────────────────────────────────────

    def on_mount(self) -> None:
        self.refresh_ports()
        self.set_interval(config.refresh_interval, self._auto_refresh)

    def _auto_refresh(self) -> None:
        if not self._search_open:
            self.refresh_ports()

    # ── data loading ─────────────────────────────────────────────────

    @work(thread=True)
    def refresh_ports(self) -> None:
        entries = fetch_ports()
        self.call_from_thread(self._update_table, entries)

    def _update_table(self, entries: List[PortEntry]) -> None:
        self._entries = entries  # store raw; table applies sort internally
        table = self.query_one(PortTable)
        table.populate(self._entries, self._query)
        self.query_one(StatusBar).set_status(
            f"{len(self._entries)} connections", style="dim"
        )

    # ── column-header click → sort ────────────────────────────────────

    def on_data_table_header_selected(self, event: DataTable.HeaderSelected) -> None:
        table = self.query_one(PortTable)
        col = str(event.column_key)

        if col not in COL_TO_ATTR:
            return  # ignore clicks on unknown keys (e.g. if label has indicator)

        if col == table.sort_col:
            # Same column: flip direction
            table.set_sort(col, not table.sort_asc)
        else:
            # New column: default ascending
            table.set_sort(col, True)

        table.populate(self._entries, self._query)
        direction = "▲" if table.sort_asc else "▼"
        col_display = col.upper()
        self.query_one(StatusBar).set_status(
            f"Sorted by {col_display} {direction}", style="cyan"
        )

    # ── actions ───────────────────────────────────────────────────────

    def action_refresh(self) -> None:
        self.query_one(StatusBar).set_status("Refreshing…", style="yellow")
        self.refresh_ports()

    def action_sort_toggle(self) -> None:
        """Cycle through all columns via the `s` key (keyboard fallback)."""
        table = self.query_one(PortTable)
        try:
            current_idx = _ALL_COLS.index(table.sort_col)
        except ValueError:
            current_idx = 0
        next_col = _ALL_COLS[(current_idx + 1) % len(_ALL_COLS)]
        table.set_sort(next_col, True)
        table.populate(self._entries, self._query)
        self.query_one(StatusBar).set_status(
            f"Sorted by {next_col.upper()} ▲", style="cyan"
        )

    def action_search(self) -> None:
        bar = self.query_one("#search-bar", Input)
        bar.add_class("visible")
        bar.focus()
        self._search_open = True

    def action_escape(self) -> None:
        if self._search_open:
            inp = self.query_one("#search-bar", Input)
            inp.value = ""
            inp.remove_class("visible")
            self._search_open = False
            self._query = ""
            table = self.query_one(PortTable)
            table.populate(self._entries, "")
            table.focus()
        elif self._detail_open:
            self.action_inspect()

    def action_inspect(self) -> None:
        pane  = self.query_one(DetailPane)
        table = self.query_one(PortTable)

        if self._detail_open:
            pane.remove_class("visible")
            pane.hide()
            self._detail_open = False
        else:
            entry = table.selected_entry(self._entries, self._query)
            if entry:
                pane.show(entry)
                pane.add_class("visible")
                self._detail_open = True

    def action_kill(self) -> None:
        table = self.query_one(PortTable)
        entry = table.selected_entry(self._entries, self._query)
        if not entry:
            self.query_one(StatusBar).set_status("No process selected", style="yellow")
            return
        self.push_screen(KillConfirmScreen(entry), self._handle_kill_confirm)

    def _handle_kill_confirm(self, confirmed: bool) -> None:
        if not confirmed:
            return
        table = self.query_one(PortTable)
        entry = table.selected_entry(self._entries, self._query)
        if not entry:
            return
        success, message = kill_process(entry.pid)
        bar = self.query_one(StatusBar)
        if success:
            bar.set_status(f"✓ {message}", style="bold green")
            self.refresh_ports()
        else:
            bar.set_status(f"✗ {message}", style="bold red")

    def action_help(self) -> None:
        self.push_screen(HelpScreen())

    # ── search input handler ──────────────────────────────────────────

    @on(Input.Changed, "#search-bar")
    def on_search_changed(self, event: Input.Changed) -> None:
        self._query = event.value
        table = self.query_one(PortTable)
        table.populate(self._entries, self._query)
        if self._detail_open:
            entry = table.selected_entry(self._entries, self._query)
            pane  = self.query_one(DetailPane)
            if entry:
                pane.show(entry)
            else:
                pane.hide()
                self._detail_open = False


def run() -> None:
    app = PortzupApp()
    app.run()


if __name__ == "__main__":
    run()
