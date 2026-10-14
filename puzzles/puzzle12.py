#Puzzle will involve finding a leaking pipe and prefroming a pattern of turns to stop the leak
import random
import time
import sys
def run_puzzle():
    message = "You stumble accross a leaking pipe! \nStop the leaking before the entire room floods, and continue on your escape!\nA series of number will be breifly displayed on screen, showing you how to turn the valve and stop the leak.\nOnce prompted write this series to show you know how to fix the leak!"
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)
    result = False
    while result == False:
        nums = random.sample(range(0, 10), 8)
        code = ''.join(str(num) for num in nums)
        sys.stdout.write("\nThe code is: " + str(code))
        time.sleep(5)
        sys.stdout.flush()
        print("\r", len(str(code)) * "", end="")
        print("                    ")
        time.sleep(5)
        guess = input("Enter the sequence: ")
        if guess == str(code):
            result = True
            message= "The valave makes a sudden shutting sound and the leak ends!\nYou may now continue your escape!"
            for char in message:
                    print(char, end='', flush=True)
                    time.sleep(0.05)
        else:
            message= "Nothing changes, the water is still gushing out!\nTry again."
            for char in message:
                    print(char, end='', flush=True)
                    time.sleep(0.05)
