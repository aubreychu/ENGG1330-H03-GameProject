#Puzzle will involve the user findign a key in a dark room
import random
import time

def run_puzzle():
    message = "You open a door and enter a dark room.\nIn this room you must find the key to open the door at the end of the room and continue your escape!\nA matrix will be displayed made up of 0s and a single o, which represents the key.\nLocate the key and correctly enter the location in the following format row:, and column: "
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)
    result = False
    while result == False:
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        line = ""
        print("")
        for i in range(10):
            for j in range(10):
                if i == row and j == col:
                    line += "o "
                else:
                    line += "0 "
            line += "\n"
        print(line)
        gRow = input("Enter the row: ")
        gCol = input("Enter the column: ")
        if gRow == str(row+1) and gCol == str(col+1):
            result = True
            message= "The key was found!\nThe door opens and you continue on your epic escape!"
            for char in message:
                    print(char, end='', flush=True)
                    time.sleep(0.05)
        else:
            message= "Unlucky, the key wasnt there!\nTry again."
            for char in message:
                    print(char, end='', flush=True)
                    time.sleep(0.05)

run_puzzle()
