# portzap 🔌

[![PyPI](https://img.shields.io/pypi/v/portzap)](https://pypi.org/project/portzap/)
[![GitHub Stars](https://img.shields.io/github/stars/fezinaniq/portzap)](https://github.com/fezinaniq/portzap)

> **Because `lsof -i :3000` is not a personality.**

A beautiful terminal UI that shows every process running on your machine's network ports — live, searchable, and killable in one keypress. No more googling commands. No more chaining `lsof | grep | kill`. Just open `portzap` and see everything.

![Demo](https://raw.githubusercontent.com/fezinaniq/portzap/main/screenshots/portzap.png)

---

## Install

```bash
pip install portzap
```

Then run:

```bash
portzap
```

That's it. Zero to running in under 30 seconds.

---

## Why portzap?

You know this moment:

```
Error: listen EADDRINUSE: address already in use :::3000
```

Then the ritual:

1. Google "how to kill port 3000"
2. Find a Stack Overflow answer
3. Run `lsof -ti:3000 | xargs kill -9`
4. Forget it by next week
5. Google it again

**portzap ends this loop.**

---

## Features

| | |
|---|---|
| **Live port table** | Every open port, process name, PID, protocol, status — updated every 2 seconds |
| **Fuzzy search** | Press `/` and type to filter by port number, process name, or status |
| **Kill with one key** | Press `k` to terminate the selected process (with confirmation) |
| **Process detail pane** | Press `i` to see full command, user, local/remote addresses |
| **Sort** | Press `s` to cycle between sort modes: port → PID → process name |
| **Auto-refresh** | Table stays live — or press `r` to force an instant refresh |
| **Cross-platform** | Linux ✅  macOS ✅  Windows (v1.1) |

---

## Keybindings

| Key | Action |
|---|---|
| `↑` / `↓` | Navigate the port list |
| `/` | Open fuzzy search |
| `Escape` | Clear search / close detail pane |
| `k` | Kill selected process |
| `i` | Toggle process detail pane |
| `r` | Force refresh |
| `s` | Cycle sort (port → PID → name) |
| `q` | Quit |
| `?` | Show help |

---

## Status colours

| Colour | Status |
|---|---|
| 🟢 Green | `LISTEN` |
| 🔵 Cyan | `ESTABLISHED` |
| 🟡 Yellow | `TIME_WAIT` |
| 🟣 Magenta | `CLOSE_WAIT` |
| 🔴 Red | `FIN_WAIT` |

---

## Platform support

| Platform | Status |
|---|---|
| Linux | ✅ Fully supported |
| macOS | ✅ Fully supported |
| Windows | ✅ Fully supported (run as Administrator) |

---

## Stack

| | |
|---|---|
| Language | Python 3.10+ |
| TUI | [Textual](https://github.com/Textualize/textual) |
| System data | [psutil](https://github.com/giampaolo/psutil) |
| Packaging | pip / PyPI |

---

## Contributing

PRs are welcome! The project is MIT licensed.

```
portzap/
├── portzap/
│   ├── main.py          # Textual App — entry point
│   ├── ui/
│   │   ├── table.py     # Port table widget
│   │   ├── detail.py    # Process detail pane
│   │   └── footer.py    # Status bar
│   ├── core/
│   │   ├── ports.py     # psutil port fetching
│   │   ├── killer.py    # Safe process kill
│   │   └── models.py    # PortEntry dataclass
│   └── config.py
├── tests/
├── pyproject.toml
└── README.md
```

Run tests:

```bash
pip install pytest
pytest tests/
```

---

## License

MIT — open, contribution-friendly, no friction.

---

*Built with Python + Textual. Inspired by the daily frustration of every developer who has ever googled "how to kill port 3000".*
