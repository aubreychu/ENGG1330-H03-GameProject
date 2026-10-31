# Titanic Escape — Technical Architecture & Agent Reference Guide

> **Notice**: This document is reserved for AI agents and developer reference to guide architecture and pair-programming sessions. The student submission `README.md` for grading will be authored separately.

---

## 1. High-Level Summary & Design Consensus

- **Game Name**: Titanic Escape
- **Setting**: The sinking RMS Titanic (April 14–15, 1912).
- **Core Loop**: Ascend from the flooded depths through 6–8 rooms to the Boat Deck and board a lifeboat before time expires.
- **Timer Engine**: Real-time countdown clock (starting at **7 minutes 30 seconds / 450s**), implemented via curses non-blocking polling (`screen.timeout(100)`).
- **Mistake Penalty**: Each incorrect guess or mistake in a mini-game deducts **30 seconds** from the clock.
- **Run Structure**:
  - Pool of **15 premade puzzle rooms**.
  - Each run selects **6 to 8 rooms total**.
  - **Room 1**: Fixed starting anchor (flooded lower compartment).
  - **Intermediate Rooms (4 to 6 rooms)**: Randomly drawn from the pool and placed in completely random sequence.
  - **Final Room**: Fixed escape anchor on the Boat Deck.
  - **Connected Puzzle**: Story link connecting Room 1 and the Final Room (currently a placeholder awaiting teammate puzzle details).
- **Puzzle Style**: Pure mini-games per room inspired by *Keep Talking and Nobody Explodes* (KTANE) modules (e.g. wire circuits, keypad codes, Morse telegraph, pressure gauges).

---

## 2. Directory & Workspace Structure

The game runs inside the course Docker container (`engg1330-project:2026-v03`), which mounts `./project` to `/workspace`.

```text
project_docker/
├── .dockerignore
├── compose.yaml              # Docker Compose volume mount: ./project -> /workspace
├── dockerfile                # Course container image definition
├── requirements.txt          # Allowed Python libraries (pytest, curses, rich, etc.)
├── agents.md                 # Agent operational rules & pedagogical guidelines
├── README_AGENTS.md          # This technical architecture blueprint
├── ai_use.md                 # Required course AI disclosure log
├── puzzles/                  # Teammate scratch/staging directory for testing individual puzzles
│   └── testpuzzle.py
└── project/                  # Mounted root in Docker container (/workspace)
    ├── main.py               # Main entry point (starts curses wrapper, title screen)
    ├── engine/               # Core game engine
    │   ├── __init__.py
    │   ├── display.py        # 80x24 layout manager, curses colors, resize detection
    │   ├── timer.py          # Real-time countdown manager with penalty deductions
    │   └── game_loop.py      # State machine: Title -> Instructions -> Room Loop -> Win/Loss
    └── rooms/                # The 15 modular puzzle rooms
        ├── __init__.py
        ├── room_anchor_start.py   # Room 1 (Start Anchor)
        ├── room_anchor_exit.py    # Final Room (Boat Deck Anchor)
        └── (modules 1 through 13 for intermediate puzzles)
```

---

## 3. Terminal Layout Specification (Strict 80 × 24)

All visuals, text, and inputs must strictly fit within an **80-column by 24-row** terminal screen without wrapping or scrolling.

```text
Row 00: +------------------------------------------------------------------------------+
Row 01: | TITANIC ESCAPE  |  Room [3/7]: Boiler Room 6  |  TIME LEFT: 05:42  [-30s]   |
Row 02: +------------------------------------------------------------------------------+
Row 03: |                                                                              |
Row 04: |   [ Teammate Mini-Game Workspace: Rows 3 to 21 (19 rows x 80 cols) ]         |
Row 05: |                                                                              |
...     |   Examples:                                                                  |
...     |   - Wire Cutting: display 4-6 colored wires and cutting options              |
...     |   - Pressure Gauges: display dial needles and valve toggles                  |
...     |   - Telegraph: Morse code dashes and deciphering letters                     |
...     |   - Keypad: 4 symbolic buttons with entry sequence                           |
Row 20: |                                                                              |
Row 21: |                                                                              |
Row 22: +------------------------------------------------------------------------------+
Row 23: | Press [1-4] to act, [H] Help, [Q] Abandon Ship.                              |
```

### Screen Sizing & Resize Behavior
Following the course's `project/tic_tac_toe.py`:
- Before every draw or input read, `os.get_terminal_size(sys.stdin.fileno())` checks if `lines >= 24` and `columns >= 80`.
- If the window is smaller, execution pauses, the screen clears, and a message displays:
  ```text
  Resize terminal to at least 80 x 24
  Current size: [cols] x [rows]
  ```
- Resizing automatically restores the current room screen without resetting the game state.

---

## 4. Teammate Puzzle Module Contract

To make collaboration smooth for university teammates with beginner Python experience, every puzzle module adheres to a dead-simple contract.

### The Contract:
Each puzzle module defines a single main function:
```python
def play_puzzle(screen, helpers) -> bool:
    """
    Executes the interactive mini-game.
    
    Parameters:
      screen:  The curses screen object for rendering.
      helpers: An engine helper object providing:
               - helpers.penalize(seconds): Deducts penalty time (e.g. 30s) on error.
               - helpers.get_time_left() -> float: Returns remaining seconds.
               - helpers.draw_header(room_title): Refreshes the top 3 header lines.
               - helpers.is_time_up() -> bool: Checks if the timer has reached 0.
               
    Returns:
      True  -> Puzzle solved successfully (advances to next room).
      False -> Player quit / abandoned the game.
    """
```

### Why this design?
- Teammates only need to write their mini-game logic.
- They do not need to understand complex global variables or multi-file dependencies.
- They draw inside rows 3–21 and let the engine handle the ticking clock, room transitions, and win/loss screens.

---

## 5. Game State Machine

```
   [ Launch: python main.py ]
               │
               ▼
       ┌───────────────┐
       │ Title Screen  ├─────────────► [ Instructions Screen ]
       └───────┬───────┘                        │
               │ [P] Play                       │ Back to Title
               ▼                                │
       ┌───────────────┐                        ▼
       │ Start Anchor  │◄───────────────────────┘
       │   (Room 1)    │
       └───────┬───────┘
               │ Solved
               ▼
     ┌───────────────────┐
     │ 4 to 6 Randomized │ ◄──── (Incorrect guess: -30s penalty)
     │   Middle Rooms    │
     └─────────┬─────────┘
               │ All Solved
               ▼
       ┌───────────────┐
       │  Final Anchor │
       │  (Boat Deck)  │
       └───────┬───────┘
               │
        ┌──────┴──────┐
        ▼             ▼
  [ Victory ]    [ Game Over ] (Timer <= 0)
        │             │
        └──────┬──────┘
               ▼
     [ Press R to Restart / Q to Quit ]
```

---

## 6. Development Phasing (Learning Roadmap)

1. **Phase 1: Minimal Playable Engine (Current Next Step)**
   - Create `project/main.py` with basic curses setup, 80x24 boundary check, and title screen.
   - Build `timer.py` supporting non-blocking 100ms ticks and the 7:30 countdown with time penalties.
   - Build a dummy test puzzle to verify the `play_puzzle(screen, helpers)` contract.
2. **Phase 2: Teammate Puzzle Integration**
   - Provide the puzzle template to teammates.
   - Integrate teammates' KTANE-style puzzles into the `rooms/` catalog as they finish them.
   - Implement the anchor room connected puzzle mechanic once puzzle designs are finalized.
3. **Phase 3: Randomizer & Polish**
   - Implement run selection: picking 6–8 rooms randomly per run.
   - Add ASCII art flourishes (Titanic silhouette, water level markers) strictly within 80x24.
4. **Phase 4: Testing & Video Preparation**
   - Write unit tests using `pytest` for input validation and state transitions.
   - Prepare script and gameplay footage for the under-1-min Trailer and under-5-min Demo Video.
