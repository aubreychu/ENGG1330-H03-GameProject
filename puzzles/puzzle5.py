import time

def run_puzzle():
    print("=== CHILL SESSION (｡･ω･｡) ===")
    input("Press ENTER to take a little break...")

    message = """
    (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧

    Heyyy! You've been doing pretty well so far!

    After all those games, you deserve a little break.
    (´｡• ᵕ •｡`) ♡

    Imagine yourself sitting in a cozy cafe.
    It's raining softly outside.  ☂
    A warm cup of hot chocolate sits beside you.
    (っ˘ڡ˘ς) ☕

    There's no timer.
    No money to lose.
    No decisions to make.

    Just the gentle sound of rain,
    and a moment to yourself. ( ˘ω˘ )

    ...

    You take another sip of your drink.
    The rain begins to slow down.
    A little sunlight peeks through the clouds. ☀

    Sometimes, it's nice to do absolutely nothing.
    (｡•̀ᴗ-)✧

    Anyway, your break is almost over.
    There are still more adventures waiting for you!

    Take your time. No rush. ♡
    ヾ(＾▽＾)ﾉ
    """

    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.04)

    input("\nPress ENTER whenever you're ready to continue... (ﾉ´ヮ`)ﾉ*: ･ﾟ")
    return True

if __name__ == "__main__":
    run_puzzle()