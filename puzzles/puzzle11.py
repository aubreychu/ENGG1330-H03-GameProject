#Puzzle will involve trying to open a locked door where the password changes
import random
import time
def run_puzzle():
    key = random.randint(1,5)
    result = False
    message = "You've arrived at a dead end! The only way out is the locked door infront of you. \nThe door has a keypad with numbers from 0 to 9, use the hints to open this door and continue your escape! \nBut beware, a failed attempt resets the password.\n*Some hints refer to length and content, others not."
    #Writing the message as if it were beign typed
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)
    #A series of passwords with correspondign hints
    pas1 = "011235"
    hint1 = "The past dictates the future. Who's scared of 7?"
    pas2 = "321"
    hint2 = "Go!"
    pas3 = "1000"
    hint3 = "8 in binary"
    pas4 = "123456"
    hint4 = "As simple as it gets. And as deep as you go when it ends"
    pas5 = "00000"
    hint5 = "This number has no magnuitude, yet it take up just as much space as the word 'hello'"
    #Loop that will run until the user has correctly guessed the password, using a random password and hint every time
    while result == False:
        key = random.randint(1,5)
        if key == 1:
            print("\nHint: " + hint1)
            guess = input("Enter the your guess: ")
            if guess == pas1:
                result = True
                message= "Correct! The door opens! Good luck on the rest of your escape!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
            else:
                message= "The door still doesnt budge! Try again!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
        elif key == 2:
            print("\nHint: " + hint2)
            guess = input("Enter the your guess: ")
            if guess == pas2:
                result = True
                message= "Correct! The door opens! Good luck on the rest of your escape!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
            else:
                message= "The door still doesnt budge! Try again!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
        elif key == 3:
            print("\nHint: " + hint3)
            guess = input("Enter the your guess: ")
            if guess == pas3:
                result = True
                message= "Correct! The door opens! Good luck on the rest of your escape!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
            else:
                message= "The door still doesnt budge! Try again!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
        elif key == 4:
            print("\nHint: " + hint4)
            guess = input("Enter the your guess: ")
            if guess == pas4:
                result = True
                message= "Correct! The door opens! Good luck on the rest of your escape!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
            else:
                message= "The door still doesnt budge! Try again!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
        elif key == 5:
            print("\nHint: " + hint5)
            guess = input("Enter the your guess: ")
            if guess == pas5:
                result = True
                message= "Correct! The door opens! Good luck on the rest of your escape!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
            else:
                message= "The door still doesnt budge! Try again!"
                for char in message:
                        print(char, end='', flush=True)
                        time.sleep(0.05)
    pass 
