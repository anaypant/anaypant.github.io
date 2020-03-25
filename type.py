# This is my computer algorithm
start = input("Hello there. Do you want to try my computer algorithm? (Y or N) - ")
if (start == "Y"):
    print("Okay, get ready!")
    import random

    guessNum = 0
    comNum = random.randint(1, 100)
    myNum = input(
        "Okay. I will select a random number from 1 to 100. Then, you may take a guess. If my number is higher than "
        "yours, I will return 'Higher'. However, if my number is lower than your number, I will send 'Lower'. Are you "
        "ready to start ? (Y or N) -  ")
    if (myNum == "Y"):
        while True:
            ask = input("Okay. I have selected my number. Which number will you choose?")
            ask = int(ask)
            if ask < comNum:
                print("Sorry, my number is higher than your number.")
                guessNum = guessNum + 1
            elif (ask > comNum):
                print("Sorry, my number is smaller than your number.")
                guessNum = guessNum + 1
            else:
                print("Correct ! Thanks for Playing!")
                break
