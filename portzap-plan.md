# portzap 🔌
### A beautiful TUI port manager for developers
> *Because `lsof -i :3000` is not a personality.*

---

## What is portzap?

A terminal UI tool that shows every process running on your machine's network ports — live, searchable, and killable in one keypress. No more googling commands. No more chaining `lsof | grep | kill`. Just open `portzap` and see everything.

---

## The Problem It Solves

Every developer knows this moment:

```
Error: listen EADDRINUSE: address already in use :::3000
```

Then the painful ritual:
1. Google "how to kill port 3000"
2. Find a Stack Overflow answer
3. Run `lsof -ti:3000 | xargs kill -9`
4. Forget it by next week
5. Google it again

**portzap ends this loop forever.**

---

## Core Features (v1.0)

| Feature | Description |
|---|---|
| Live port table | See all open ports, process name, PID, protocol, status |
| Fuzzy search | Type to filter by port number or process name |
| Kill with keypress | Press `k` to kill the selected process |
| Process details | Press `i` to see full command, user, uptime |
| Auto-refresh | Table updates every 2 seconds live |
| Cross-platform | Works on Linux, macOS, Windows |

---

## Feature Roadmap

### v1.0 — MVP (ship this first)
- [ ] Live table of all open ports
- [ ] Process name, PID, protocol (TCP/UDP), status
- [ ] Fuzzy search / filter
- [ ] Kill a process with `k`
- [ ] Detail pane with `i`
- [ ] Auto-refresh every 2s
- [ ] Works on Linux + macOS

### v1.1 — Polish
- [ ] Windows support
- [ ] Sort by port / PID / process name
- [ ] Color coding by status (LISTEN, ESTABLISHED, TIME_WAIT)
- [ ] Kill confirmation prompt (safety)
- [ ] Config file for refresh rate

### v1.2 — Power features
- [ ] Filter by protocol (TCP only / UDP only)
- [ ] Port range filter (e.g. 3000–4000)
- [ ] Export port list to JSON/CSV
- [ ] Docker container name resolution (show container name instead of PID)
- [ ] Bookmark / watch specific ports

### Future ideas
- [ ] Conflict detector — warn when two services fight over a port
- [ ] Port history — see which ports were recently used
- [ ] Team config — share a port layout with your team

---

## Tech Stack

```
Language    →  Python 3.10+
TUI         →  Textual  (beautiful, modern, well-documented)
System data →  psutil   (cross-platform port + process reading)
Styling     →  Rich     (comes bundled with Textual)
Packaging   →  pip / PyPI
```

### Why this stack?
- **Textual** has 26k stars — the Python TUI community is massive and active
- **psutil** does the hard work (reading `/proc/net` on Linux, `netstat` on macOS/Windows) so you don't have to
- Ships as a simple `pip install portzap` — zero friction for users

---

## Project Structure

```
portzap/
│
├── portzap/
│   ├── __init__.py
│   ├── main.py          # Entry point, Textual App class
│   ├── ui/
│   │   ├── table.py     # Port table widget
│   │   ├── detail.py    # Process detail pane widget
│   │   └── footer.py    # Keybinding hints footer
│   ├── core/
│   │   ├── ports.py     # psutil logic — fetch all port data
│   │   ├── killer.py    # Safe process kill logic
│   │   └── models.py    # PortEntry dataclass
│   └── config.py        # Refresh rate, theme settings
│
├── tests/
│   ├── test_ports.py
│   └── test_killer.py
│
├── screenshots/
│   └── demo.gif         # 🔑 THE MOST IMPORTANT FILE
│
├── pyproject.toml       # Build config + dependencies
├── README.md
└── LICENSE              # MIT
```

---

## Core Data Model

```python
@dataclass
class PortEntry:
    port: int
    pid: int
    process_name: str
    protocol: str        # TCP / UDP
    status: str          # LISTEN / ESTABLISHED / TIME_WAIT
    local_address: str
    remote_address: str
    username: str
    command: str         # Full command that opened this port
```

---

## Key Bindings

| Key | Action |
|---|---|
| `↑` / `↓` | Navigate the port list |
| `/` | Open fuzzy search |
| `k` | Kill selected process |
| `i` | Open process detail pane |
| `r` | Force refresh |
| `s` | Sort toggle (port / pid / name) |
| `q` | Quit |
| `?` | Show help |

---

## Installation Plan (for users)

```bash
# Install
pip install portzap

# Run
portzap

# Or directly
python -m portzap
```

Goal: from zero to running in under 30 seconds.

---

## README Strategy (critical for stars ⭐)

The README is the product page. It needs:

1. **One-line description** — what it does, instantly clear
2. **GIF demo** — record a 15-second demo of killing a stuck port
3. **Install command** — `pip install portzap` front and center
4. **Why portzap?** — the `lsof` pain story, relatable
5. **Features list** — clean, scannable
6. **Platform support badges** — Linux ✅ macOS ✅ Windows ✅
7. **Contributing guide** — lowers barrier for PRs

> 🎯 The GIF demo is the single highest-ROI thing you can make.
> A 15-second screen recording of portzap killing a stuck port = more stars than any feature.

---

## Launch Strategy

### Day of launch — do all of these:

| Platform | What to post |
|---|---|
| **Hacker News** | Show HN: portzap – Kill stuck ports without googling lsof ever again |
| **r/Python** | "Built a TUI port manager with Textual — feedback welcome" |
| **r/devtools** | Share the GIF demo |
| **r/programming** | Focus on the problem story |
| **Twitter / X** | Short GIF + "tired of googling lsof? made this" |
| **dev.to** | Write a short post: "I built portzap in a weekend — here's how" |

### The HN title formula that works:
```
Show HN: portzap – a TUI to see and kill processes on any port (no more lsof)
```

Personal story beats technical description every time.

---

## Success Metrics

| Milestone | Target |
|---|---|
| First star | Day 1 |
| 10 stars | Day 1 (from friends + HN) |
| 50 stars | Week 1 |
| 100 stars | Month 1 ← main goal |
| 500 stars | Month 3 (if HN post lands well) |
| First issue opened | Week 1 |
| First outside contributor | Month 2 |

---

## Competitive Advantage

All existing competitors (killport-tui, portpilot, icport) have near-zero stars because **they never marketed**. The code was fine. The README was not. The launch never happened.

portzap wins by:
- Polished README with GIF demo
- Real launch on HN + Reddit on day one
- Working perfectly on macOS (where most GitHub users are)
- `pip install portzap` — frictionless install

---

## Build Timeline

| Phase | Tasks | Time |
|---|---|---|
| **Day 1 AM** | Setup project, psutil port fetching, basic data model | 3h |
| **Day 1 PM** | Textual TUI — table widget, live refresh | 3h |
| **Day 2 AM** | Search, kill, detail pane, keybindings | 3h |
| **Day 2 PM** | Polish, edge cases, test on macOS + Linux | 2h |
| **Day 3** | README, GIF demo recording, PyPI publish, launch | Full day |

**Total: ~3 days from zero to launch.**

---

## License

MIT — keeps it open, contribution-friendly, and no friction for anyone who wants to use it.

---

*Built with Python + Textual. Inspired by the daily frustration of every developer who has ever googled "how to kill port 3000".*
