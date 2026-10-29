import random

print("Nim")
print("There are 15 sticks.")
print("Take turns removing 1, 2, or 3 sticks.")
print("Whoever takes the LAST stick LOSES.")
print("You go first.\n")

sticks = 15

while sticks > 0:
    print(f"Sticks left: {sticks}")

    # player turn
    while True:
        take = input("How many do you take? (1-3): ").strip()
        if take in ("1", "2", "3"):
            take = int(take)
            if take <= sticks:
                break
        print("Take 1, 2, or 3 (and not more than remain)\n")

    sticks -= take
    print(f"You take {take}. Sticks left: {sticks}")

    if sticks == 0:
        print("\nYou took the last stick. Computer wins!")
        break

    # computer turn — smart play
    # optimal: leave a multiple of 4 for the opponent
    if sticks % 4 == 0:
        take = random.randint(1, 3)  # already losing, take random
    else:
        take = sticks % 4
    if take > sticks:
        take = sticks

    sticks -= take
    print(f"Computer takes {take}. Sticks left: {sticks}")

    if sticks == 0:
        print("\ Computer took the last stick. You win!")
        break

    print()