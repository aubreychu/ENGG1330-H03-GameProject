Game Purpose and Rules:
  - Game is inspired by the Titanic
    - Complete a series of tasks to escape the Titanic and survive!
    - Each task represents a floor you must scale to reach the escape at the top of the boat
  - Rules
    - All actions taken concerning the game must be taken directly in the terminal
    - Using external notes or means of memorisation ruin the purpose of many tasks in the game
    - A limited time is assigned to each task
    - Additional time left over after a time is completed is added to the time allowed for the following task
    - Fail to meet the allocated time, the sink ships and you go down with it

Group Details:
  - Group members
    - Erwann Hare Zylberberg
    - Lee Min-En
    - Chu Viet Tung
    - Tseng Wei Hua
  - Tutorial subclass: H
  - Group Number: 3
  
Environment and Execution:
  - Docker course container: v4.48.0
  - Command required to run game: "main.py"

Test and Limitations:
  - Tests:
    - Due to their being various combinations of puzzles a user can come across (Over 3 million), ther is no single test to be conducted on the game
    - For this reason we used a systemmatic way to test each individual compnent of the game
    - Normal game play:
      - Inputing expected values when prompted to do so in order to play the game
      - For instance puzzle 15 asks the user to input a single character "l" or "r"
    - Boundary inputs:
      - Inputing values that should still work but are at the boundary of the restrictions set on input
      - For instance puzzle 14 asks the user for a number between 1 and 5, hence entering 5 or 1 should not cause a crash, but 6 should
    - Abnormal inputs:
      - Input values that are in the wrong format and should lead to the program gracefuly failing
      - For instance entering a string when an integer is entered in puzzle should lead to a message specifying the required type of input
  - Limitations
    - No known limitations

Comntribution Record:
  - Erwann Hare Zylberberg:
    - Conceptual brain storm 
    - Documentation
    - Writing up 5 puzzles
  - Lee Min-En:
    - Writing up 5 puzzles
    - Demo
  - Chu Viet Tung:
    - Wrote the main framework to connect all the puzzles together and global game state
    - Created the title screen with animations using the curses library
    - Timer system implemenation
  - Tseng Wei Hua:
    - Writing up 5 puzzles
    - Debugging
    - Trailer

Sources:
  - Curses:
    - Component: main.py
    - Source: Created with information from [Python.org](https://docs.python.org/3/howto/curses.html?fbclid=PARlRTSAVXyyxleHRuA2FlbQIxMABwZG9mAmZkaWQWURmy4TvVLyMLuxi_q4pUMdQ4XU_sIHNydGMGYXBwX2lkDzEyNDAyNDU3NDI4NzQxNAABp0l47ITT2_0cxZ96vCDx_94WWCJIiREZF_PzXhrQnTQx2T1qaLVHF33XB6yn_aem_WUAHHVbT3V50H1GP23njhA)
    - Liscence: Python Software Foundation License Version 2
    - Usage: Used the library and the information detailed by the webpage to achieve the animated user interface look
  - Lambda fucntions:
    - Component: puzzle10.py
    - Source: Create with information from [W3Schools](https://www.w3schools.com/python/exercise.asp?x=xrcise_lambda1&fbclid=PARlRTSAVXzsNleHRuA2FlbQIxMABwZG9mAmZkaWQWURlm2ZP8jRh8ALhlpa5v5P9Noo_d5XNydGMGYXBwX2lkDzEyNDAyNDU3NDI4NzQxNAABp9aAZKov2X2gY8HmdKZtjvgT03HTkHIG2Rx7PXFYCbG2Sx4VkpiV749yS0Qv_aem_2ncnM9Gok3Xkgx7da1g0IA)
    - Liscence: N/A
    - Usage: Implemented in the main function of puzzle10 in order to enable intended purpose of the code
  - Type Writer effect:
    - Component: puzzle1-15.py
    - Source: Created with inspiration from [Divinemonk](https://github.com/Divinemonk/typewriter_effect_python)
    - Lisence: N/A
    - Usage: Inspired the code used to type out text on screen
  - Timer:
    - Component: timed_screen.py, main.py
     Source: Created with information from [Python.org](https://docs.python.org/3.7/library/time.html)
    - Lisence: Python Software Foundation License Version 2
    - Usage: Used the library and the information detailed by the webpage to achieve the timing functions
  - Ideas for puzzle 1-3:
    - Component: puzzle1-3.py
     Source: Created with inspiration from [Stake](https://stake.com/zh)
    - Lisence: N/A
    - Usage: Ideas for creating puzzle1-3

Trailer Video Link: https://youtu.be/ycqQRj1OYfo
Demo Video Link: https://youtu.be/huBnhXWqJQ0