# This puzzle will involve the user opening the correct door in order to progress along the game
import random
import time

def run_puzzle():
    message = "You arrive upon 5 identical doors!\nOpen the right door to continue your escape!\nBeware, every failed attempt causes the correct door to change location."
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)
    result = False
    while result == False:
        print("")
        current = random.randint(1,5)
        print(" ___   ___   ___   ___   ___")
        print("|   | |   | |   | |   | |   |")
        print("| 1 | | 2 | | 3 | | 4 | | 5 |")
        print("|   | |   | |   | |   | |   |")
        print("|___| |___| |___| |___| |___|")
        guess = int(input("Which door leads to your escape: "))
        if guess == current:
            message = "Hurray the door leads to a corridor, the key to your escape!"
            for char in message:
                print(char, end='', flush=True)
                time.sleep(0.05)
            result = True
        else:
            message = "Oh no, the door leads to a dead end, try again!"
            for char in message:
                print(char, end='', flush=True)
                time.sleep(0.05)

run_puzzle()