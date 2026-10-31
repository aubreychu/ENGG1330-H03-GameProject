# AGENTS.md — Operational Guidelines for AI Assistants

## 1. Project Context & Pedagogical Philosophy
- **Course**: University of Hong Kong (HKU) — ENGG1330 Computer Programming (Group Project 2026–27).
- **Core Philosophy**: **This is a student learning project.**
  - The student is learning foundational Python and computer science concepts.
  - **Do NOT generate full code implementations unprompted.**
  - **Do NOT rush ahead or skip intermediate steps.**
  - Keep programming concepts strictly aligned with beginner-friendly Python: functions, dictionaries, lists, tuples, loops, conditionals, basic string manipulation, and standard libraries.
  - Avoid complex OOP hierarchies, metaprogramming, third-party frameworks, or unnecessary design patterns.
  - Act as a patient pair-programming mentor: ask guiding questions, explain the "why", review code, and assist with debugging and edge cases.

---

## 2. Hard Course & Technical Constraints
All AI agents collaborating on this project must strictly enforce the following rules:

1. **Docker Environment**:
   - Must run inside the provided course Docker container: `engg1330-project:2026-v03`.
   - The repository volume is mounted as `./project -> /workspace` (configured in `compose.yaml`).
   - The primary game entry point must be `project/main.py`.
   - No external packages beyond the standard library and starter environment (`requirements.txt`).
2. **Terminal Size Restriction (Strict 80 × 24)**:
   - Strictly constrained to **80 columns by 24 rows (`80x24`)**.
   - No drawing or messages outside this area; no accidental wrapping or scrolling.
   - If the terminal size drops below 80×24, the game must pause execution and display a resize notice until restored (following the pattern in `project/tic_tac_toe.py`).
3. **Turn-Based & Offline Specification**:
   - Offline, single-player console game. No graphical windows, no audio, no networking.
4. **Academic Integrity & AI Transparency (`ai_use.md`)**:
   - Every substantive interaction, architectural decision, or code assistance must be documented in `ai_use.md` following the course template.

---

## 3. Game Identity & Architectural Decisions (Grill-Me Consensus)

- **Theme**: RMS Titanic Escape (1912).
- **Objective**: Ascend through the ship's levels to reach the Boat Deck and launch a lifeboat before the ship sinks.
- **Timer & Threat Mechanic**:
  - Real-time countdown timer starting at **7 minutes 30 seconds (450 seconds)**.
  - Managed via non-blocking curses input polling (`screen.timeout(100)`).
  - Mistakes/penalties: Wrong guesses or puzzle errors deduct **30 seconds** from the master countdown.
  - Loss condition: Timer reaches 00:00 (ship sinks).
- **Progression Structure (6–8 Rooms per Run)**:
  - **Anchor Room 1**: Fixed starting room in the flooded lower decks.
  - **Intermediate Rooms (4–6 Rooms)**: Drawn from a catalog of 15 premade rooms and chained in completely random sequence.
  - **Anchor Final Room**: Fixed escape finale on the Boat Deck (Lifeboat launch).
  - **Connected Puzzle**: A story connection between Room 1 and the final room (currently marked as a placeholder for teammate puzzle integration).
- **Puzzle Format**:
  - Pure mini-game per room, inspired by *Keep Talking and Nobody Explodes* (KTANE) style modules (wire cutting, keypads, Morse code, memory, pressure valves).
  - Teammate puzzle contract: Each puzzle is an independent module with a standardized `play_puzzle(screen, helpers) -> bool` function.
  - Engine reserves Rows 0–2 for global header and clock; teammates render within Rows 3–21.
- **Game Flow**:
  - Title Screen (`project/title_screen.py`):
    - Controls: `[C] Start Escape`, `[H] How to Play`, `[Q] Quit`.
    - Visual Layout: Spiky Iceberg with nested menu (Cols 0–27), 10-column open water channel, detailed 4-funnel Titanic (Cols 32–77).
    - Dynamics: Vertical buoyancy bobbing (+0/+1 row toggle), rolling ocean waves, animated 4-funnel steam plumes, crescent moon, and flying bird with full-width screen crossing.
  - In-game End Screen: Outcome narrative with stats (time remaining, rooms cleared), and prompt: `[R] Restart / [Q] Quit`.

---

## 4. Rules of Engagement for AI Agents
1. When asked for advice, offer simple, modular options with clear trade-offs.
2. When helping write code, keep functions small, readable, and well-commented.
3. Always verify changes against the `80x24` terminal constraint and Docker mount structure.
4. Never implement puzzles or game systems without the student leading the design and understanding every line.
5. **Terminal Visual & Animation Guidelines (80x24)**:
   - **Composition (The 25/75 Rule)**: Reserve bottom ~25% (Rows 18–23) for water/floor; reserve top ~75% for sky, structures, and atmosphere to prevent cramped framing.
   - **Layering & Clipping**: Dynamic actors (birds, debris, projectiles) must render above terrain and smoothly clip offscreen using negative column slicing (`col < -len(sprite)`).
   - **Buoyancy**: Cut floating silhouettes cleanly at the waterline; simulate ocean swell by bobbing the hull into/out of the top water row rather than exposing an underwater keel.
   - **Particles**: Use bold multi-character clusters (e.g. `( )`, `(~)`, `(@)`) rather than loose single dots for distinct, readable steam/smoke.
   - **Preview Fallback**: Modules with curses rendering should provide an ANSI escape `--preview` mode so students can verify layouts directly in local PowerShell without waiting for Docker boots.
