import threading
import dataStorage as DS
import computerWordChecker as CWC
import humanChecker as HC
import player
import extraValue as EV
import boardKeeper as BK
import letterBag as LB
import helper
from tkinter import *
import pyautogui
import playsound
import colorsys


from dataStorage import boardKeeper

# all of the big classes
humanPlayer = player.player()
computerPlayer = player.player()
humanCheck = HC.humanChecker()
computerCheck = CWC.computerWordChecker()
letterBag = LB.letterBag()

# make the dictionary
doc = open('scrabbleDictionary.txt', 'r')
document = doc.read().lower()
dictionary = set(document.split('\n'))
doc.close()

trnctr = 0

def background_moozic():
    while True:
        print("EEE")
        playsound.playsound("If I Had A Chicken.mp3")

def run(width=1920, height=1080):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(
            0, 0, data.width, data.height, fill='white', width=0)
        x.redrawAll(canvas)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        # column = ((event.x - x.data.squareLeft) // x.data.squareSize)
        # if (column > (BK.BOARDSIZE-1) or column < 0):
        #     # if outside of board, column is only used for the board
        #     column = BK.BOARDSIZE*BK.BOARDSIZE
        # row = ((event.y - x.data.squareTop) // x.data.squareSize)
        # spot = row*BK.BOARDSIZE + column
        # print(str(spot) + ',')
        # return

        global trnctr
        if x.data.endOfGame:
            # end of game scenario
            x.data.message1 = "Game Over!!!"
            if humanPlayer.points > computerPlayer.points:
                x.data.message2 = 'Human player wins!'
            elif humanPlayer.points < computerPlayer.points:
                x.data.message2 = 'Computer player wins ...'
            else:
                x.data.message2 = "It's a tie"

        else:
            # case of computer turn
            t1 = (trnctr % 2) == 1
            trnctr += 1

            p = computerPlayer if t1 else humanPlayer

            x.data.message3 = ''
            # redrawAllWrapper(canvas, data)

            occupied = set(boardKeeper.refreshOccupied())
            attachments = set(boardKeeper.refreshAttachments())

            computerCheck.changeLetterHand(
                p.letterHand)
            computerCheck.getLetterCombos()
            workingCombos = computerCheck.getDirectedCombos(
                boardKeeper.board, occupied, attachments, dictionary)
            maxCombo = EV.maxComboValue(workingCombos, boardKeeper.board)
            if maxCombo[0] != -1:
                playsound.playsound("place.mp3")
                x.refreshSpecialTiles(
                    EV.tripleWord, EV.doubleWord, EV.quadWord, EV.doubleLetter, EV.tripleLetter, EV.quadLetter)
                boardKeeper.changeBoard(
                    maxCombo[1], maxCombo[2], 1 if t1 else 0)
                x.computerChangeBoard(
                    boardKeeper.board, maxCombo[1], maxCombo[2])
                p.addPoints(maxCombo[0])
                x.changeScore(
                    p.points, t1)
                p.playFromHand(
                    maxCombo[1])
                removedLetters = letterBag.removeLetters(len(maxCombo[1]))
                x.changeLetterBagSize(len(letterBag.letterBag))
                p.addToHand(removedLetters)
                data.message1 = f"Computer #{(trnctr&1) + 1} - " + " Letters used: " + str(maxCombo[1])
                data.message2 = f"Earned: {maxCombo[0]}, Total Score: {p.points}";
                x.changeLetterHand(
                    p.letterHand)
            else:
                x.data.message1 = 'The computer was forced to pass.'
                letters = p.letterHand
                p.playFromHand(letters)
                removedLetters = letterBag.removeLetters(7)
                p.addToHand(removedLetters)
                letterBag.letterBag += letters
                x.changeLetterHand(
                    p.letterHand)
            # x.data.computerTurn = !x.data.data
            # x.data.humanTurn = False
            
            print(data.message1 + ", " + data.message2)

            if len(p.letterHand) == 0:
                x.data.endOfGame == True    # reached end of game

        redrawAllWrapper(canvas, data)
        # Keep playing (yes I know doing this recursively is STUPID, but its easy and fun)
        mousePressedWrapper(event, canvas, data)

    def keyPressedWrapper(event, canvas, data):
        x.keyPressed(event)
        redrawAllWrapper(canvas, data)

    # Initialize data
    class Struct(object):
        pass
    data = Struct()
    data.width = width
    data.height = height
    data.endOfGame = False
    x = DS.dataStorage(data)
    # initialize special tiles in dataStorage
    x.refreshSpecialTiles(EV.tripleWord, EV.doubleWord, EV.quadWord,
                          EV.doubleLetter, EV.tripleLetter, EV.quadLetter)
    # creates hands for both players
    removedLetters = letterBag.removeLetters(7)
    humanPlayer.addToHand(removedLetters)
    x.data.letterHand = humanPlayer.letterHand
    removedLetters = letterBag.removeLetters(7)
    computerPlayer.addToHand(removedLetters)
    # initialize size of letterbag in datastorage
    x.changeLetterBagSize(len(letterBag.letterBag))
    # create the root and the canvas
    root = Tk()
    frame = Frame(root)
    canvas = Canvas(root, width=x.data.width, height=x.data.height)
    canvas.pack()
    # set up events
    redrawAllWrapper(canvas, x.data)    # this is to show the interface
    root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas, x.data))
    root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, x.data))
    # and launch the app
    
    threading.Thread(target=background_moozic, daemon=True).start()
    playsound.playsound("dump.mp3")
    while not x.data.endOfGame:
        # mousePressedWrapper(None, canvas, x.data)
        pyautogui.click(root.winfo_x() + 100, root.winfo_y() + 100)
        root.mainloop()  # blocks until window is closed
    print("bye!")


run(1000, 600)
