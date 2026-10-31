# AI Use

Generative AI used: Yes

## Entry

Member and date: Tung, 13 October 2026
Tool: Gemini 3.8 Flash (High) via Antigravity
Purpose: Prototype an animated 80x24 curses title screen (iceberg menu, bobbing Titanic, moving waves, flying birds).
Prompts used: User requests: "Let's make a title screen. Before beginning, I want to know what's the best way to make stylized ascii art with this resolution?", hand-drawn concept sketch with iceberg on the left and Titanic on the right, "Let's make it coloured, the iceberg more spiky/iceberg-like, and occasionally birds fly above the sky", "Option 2 please. But shift the ship to the right a bit so it look less cramped."
Files affected: project/title_screen.py
What we kept, changed or rejected:
- Kept: Spiky iceberg menu, detailed Titanic, bobbing/water/bird animations, and ANSI preview.
- Changed: Shifted ship right, lowered waterline, added crescent moon, animated smoke, and fixed bird layering/despawn bugs.
- Rejected: Moving background overwriting static menu text
- How we checked it: Rendered ANSI previews for animation states, verified strict 80x24 boundaries, checked safe imports, and verified user screenshots and bird flight paths in the Docker container.

## Entry
Member and Date: Tung, 31 October 2026
Tools Used: Gemini 3.8 Flash (High) & Gemini 4 Argon (High) via Antigravity
Prompts used: "Help me convert all the newly added puzzles into curses and ensure they are in the resolution of the project.", "1. Yes 2. No"
Purpose: Implement the 6-room randomized run progression in main.py, register all 15 puzzle modules, and convert all puzzles to curses within strict 80x24 boundaries (Rows 4–22, Cols 2–75).
Files Affected: project/main.py, project/puzzles/puzzle1.py – puzzle15.py
What we kept, changed or rejected:
- Kept: All original puzzle logic, riddles, passcodes, rewards/penalties, ASCII art, and feedback messages.
- Changed: Registered all 15 puzzles into the 6-room randomized loop in main.py, Replaced print/input and os.system('cls') with curses addstr/getstr and clrtoeol(), Standardized standalone scripts (puzzle6–10) into run_puzzle(screen) functions returning True/False.
- Rejected: Standard print() scrolling exceeding 24 rows and text lines over 80 columns that would crash curses.
- Verification: Compiled all modules via py_compile in the course Docker container, verified run_puzzle(screen) signatures, and ran an AST coordinate audit confirming strict 80x24 compliance.
