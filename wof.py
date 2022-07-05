from sympy import total_degree
from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }
count = 0
roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""


def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
    #open dictionary file
    rdictf = open(dictionaryloc, 'r')
    rdictfstr = rdictf.read()
    rdictf.close()
    dictionary = rdictfstr.split('\n')
    


def readTurnTxtFile():
    global turntext   
    #read in turn intial turn status "message" from file
    rttf = open(turntextloc, 'r')
    turntext = rttf.read()
    rttf.close()

        
def readFinalRoundTxtFile():
    global finalroundtext   
    #read in turn intial turn status "message" from file
    rfrtf = open(finalRoundTextLoc, 'r')
    finalroundtext = rfrtf.read()
    rfrtf.close()


def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location
    rrstf = open(roundstatusloc, 'r')
    roundstatus = rrstf.read()
    rrstf.close()

def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    rwtf = open(wheeltextloc, 'r')
    wheellist = rwtf.readlines()
    for i in range(len(wheellist)):
        wheellist[i] = str(wheellist[i]).strip().lower()
    rwtf.close()

def getPlayerInfo():
    global players
    # read in player names from command prompt input
    print('Now let us meet who will be playing today!')
    players[0]["name"] = input("Introduce yourself player 1: ")
    players[1]["name"] = input("Introduce yourself player 2: ")
    players[2]["name"] = input("Introduce yourself player 3: ")


def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
    global roundNum
    roundnum = 0
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    global roundWord
    global blankWord

    #choose random word from dictionary
    roundWord = random.choice(dictionary)
    #make a list of the word with underscores instead of letters.
    blankWord = ['_' for i in roundWord]

    return roundWord, blankWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    blankWord = []
    # Set round total for each player = 0
    players[0]["roundtotal"] = 0
    players[1]["roundtotal"] = 0
    players[2]["roundtotal"] = 0
    # Return the starting player number (random)
    initPlayer = random.randint(0,2)
    getWord()
    return initPlayer

def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    global letter

    stillinTurn = True

    # Get random value for wheellist
    spin_value = random.choice(wheellist)
    # Check for bankrupcy, and take action.
    if spin_value == "bankrupt":
        players[playerNum]["roundtotal"] = 0
        print("Oh no! Bankrupt! On to the next player.")
        stillinTurn = False

    # Check for lose turn
    elif spin_value == "loseaturn":
        print("Oh no! Lose A turn! On to the next player.")
        stillinTurn = False


    # Get amount from wheel if not loose turn or bankruptcy
    else:         
        while True:
            letter = input(f"{spin_value}! Guess a consonant: ")
            if letter in vowels:
                print('That is a vowel. We need a consonant')
            else: 
                goodGuess, count = guessletter(letter, playerNum)
                if goodGuess == True:
                    players[playerNum]["roundtotal"] += int(spin_value)
                    stillinTurn = True
                    print(f"{spin_value} added.")

                    break
                else:
                    stillinTurn = False
                    break

    return stillinTurn

def guessletter(letter, playerNum): 
    global players
    global blankWord
    count = 0
    assessment = True
    while assessment == True:
        if letter in roundWord:
            for i in range(len(roundWord)):
                if roundWord[i] ==letter:
                    blankWord[i] = letter
            goodGuess = True
            print(blankWord)  
        else:
            print("That guess is sadly not in the word.")
            goodGuess = False
        assessment = False
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    if players[playerNum]['roundtotal'] >= 250:
        while True:
            vowel = input("Which vowel would you like to buy? ")
            if vowel in vowels:
                guessletter(vowel, playerNum)
                players[playerNum]["roundtotal"] -= int(250)
            goodGuess = True
            break
    else:
        print('Insufficient funds.')
        goodGuess = True

    return goodGuess      
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    guessWord = input("What word would you like to guess? ")
    if guessWord == roundWord:
    # Fill in blankList with all letters, instead of underscores if correct
        for i in range (len(roundWord)):
            if roundWord == guessWord:
                blankWord[i] = guessWord
        print(f"Correct! The word was indeed {roundWord}!")
    # return False ( to indicate the turn will finish)  
    else:
        print("Ah, sadly that is not correct.")
    return False
      
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    readRoundStatusTxtFile()
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal (roundtotal is roundtotal)

    print(turntext.format(name = players[playerNum]["name"], word=blankWord))
    
    stillinTurn = True
    while stillinTurn:
        if '_' not in blankWord:
            stillinTurn = False
            break
        
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        #print for checking
        #print(roundWord)
        choice = input(f"{players[playerNum]['name']} Choose between (S) for Spin, (B)for Buy a vowel, or (G) for Guess the solution: ")

        readFinalRoundTxtFile()

        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    
def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    global roundNum
    roundNum  += 1
    readRoundStatusTxtFile()
    print(f'This is round Number {roundNum}')
      
    initPlayer = wofRoundSetup()
    activePlayer = initPlayer

    roundInProgress = True
    while roundInProgress == True:

        if '_' not in blankWord:
            roundInProgress = False
            break
        #Begin the current players turn
        wofTurn(initPlayer)
        initPlayer +=1
        if initPlayer > 2:
            initPlayer = 0
    #updating totals
    print(roundstatus.format(word = roundWord,))
    players[activePlayer]["gametotal"] += players[activePlayer]["roundtotal"]

    
def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    global players
    mostMoney = 0
    freebies = {"R", "S", "T", "L", "N", "E"}
    
    # Find highest gametotal player.  They are playing.
    for item in players.keys():
        cash = players[item]["gametotal"]
        if cash > mostMoney:
            mostMoney = cash
            winner = item


    # Print out instructions for that player and who the player is.
    print(finalroundtext.format(name=players[winner]['name'], winnings=players[winner]['gametotal']))
    print(f"""Congratulaitons to our winner {players[winner]['name']}!
    R, S, T,L, N, E will all be revealed for free.
    You will also be able to guess 3 consonants, and 1 additional vowel.
    This is for an additional $50,000!
    """)


    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    roundWord, blankWord = getWord()


    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    for i in freebies:
        guessletter(i.lower(), winner)
    print(f"Here is what we have so far: {blankWord}")

    #print for checking
    #print(roundWord)


    # Gather 3 consonants and 1 vowel and use the guessletter function to see if they are in the word
    for i in range(3):
        guessed_consonants = []
        while True:
            consonant = input(f"Please enter consonant number {i + 1}: ").lower()
            if consonant.isalpha == False or len(consonant) != 1:
                print('That is not a singular consonant. Try Again.')
            elif consonant in vowels:
                print('That is a vowel. We are currently taking consonants. Try Again')
            elif consonant in blankWord:
                print('That letter has already been displayed. Try again.')
            elif consonant in guessed_consonants:
                print('You have already guessed this consonant. Try again.')
            else:
                guessletter(consonant, winner)
                guessed_consonants.append(consonant)
                break
    
    while True:
        vowel = input('And the final vowel: ').lower()
        if vowel.isalpha == False or len(vowel) != 1:
            print('That is not a singular vowel. Try Again.')
        elif vowel not in vowels:
            print('That is not a vowel. Try Again.')
        elif vowel in blankWord:
            print('That vowel is already displayed. Try Again.')
        else:
            guessletter(vowel, winner)
            break
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    print(f"Let us see what we have on the board so far! {blankWord}")
    # Get user to guess word
    final_round_guess = input('Time to guess the final word. What do you think it is?: ')
    # If they do, add finalprize and gametotal and print out that the player won
    if final_round_guess == roundWord:
        players[winner]['gametotal'] += 50000
        print(f"You got it! You are walking away from this game with $ {players[winner]['gametotal']}  ! Congratulations!")

    else:
        print(f"Unfortunately that is not correct. You will still be going home with $ {players[winner]['gametotal']}")

def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
