import dataStorage as DS
import computerWordChecker as CWC
import humanChecker as HC
import player
import extraValue as EV
import boardKeeper as BK
import letterBag as LB
import helper
from tkinter import *

# all of the big classes
boardKeeper = BK.boardKeeper()
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


def run(width=1000, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(
            0, 0, data.width, data.height, fill='white', width=0)
        x.redrawAll(canvas)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
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

        elif True:  # x.data.computerTurn:
            # case of computer turn
            t1 = (trnctr % 2) == 1
            trnctr += 1
            print(trnctr)

            x.data.message1 = "It's the computer's turn"
            x.data.message2 = 'Waiting for the computer...'
            x.data.message3 = ''
            redrawAllWrapper(canvas, data)

            occupied = set(boardKeeper.refreshOccupied())
            attachments = set(boardKeeper.refreshAttachments())

            computerCheck.changeLetterHand(
                (computerPlayer if t1 else humanPlayer).letterHand)
            computerCheck.getLetterCombos()
            workingCombos = computerCheck.getDirectedCombos(
                boardKeeper.board, occupied, attachments, dictionary)
            maxCombo = EV.maxComboValue(workingCombos, boardKeeper.board)
            if maxCombo[0] != -1:
                x.refreshSpecialTiles(
                    EV.tripleWord, EV.doubleWord, EV.doubleLetter, EV.tripleLetter)
                boardKeeper.changeBoard(maxCombo[1], maxCombo[2])
                x.computerChangeBoard(
                    boardKeeper.board, maxCombo[1], maxCombo[2])
                (computerPlayer if t1 else humanPlayer).addPoints(maxCombo[0])
                x.changeScore(
                    (computerPlayer if t1 else humanPlayer).points, t1)
                (computerPlayer if t1 else humanPlayer).playFromHand(
                    maxCombo[1])
                removedLetters = letterBag.removeLetters(len(maxCombo[1]))
                x.changeLetterBagSize(len(letterBag.letterBag))
                (computerPlayer if t1 else humanPlayer).addToHand(removedLetters)
                data.message1 = "Score: " + \
                    str(maxCombo[0]) + ", Letters used: " + str(maxCombo[1])

                x.changeLetterHand(
                    (computerPlayer if t1 else humanPlayer).letterHand)
            else:
                x.data.message1 = 'The computer was forced to pass.'
                letters = (computerPlayer if t1 else humanPlayer).letterHand
                (computerPlayer if t1 else humanPlayer).playFromHand(letters)
                removedLetters = letterBag.removeLetters(7)
                (computerPlayer if t1 else humanPlayer).addToHand(removedLetters)
                letterBag.letterBag += letters
                x.changeLetterHand(
                    (computerPlayer if t1 else humanPlayer).letterHand)
            # x.data.computerTurn = !x.data.data
            # x.data.humanTurn = False

            if len((computerPlayer if t1 else humanPlayer).letterHand) == 0:
                x.data.endOfGame == True    # reached end of game

        else:
            x.data.message1 = "It's the human's turn"
            x.data.message2 = 'Click on a blue box.'
            x.data.humanTurn = True
            x.data.computerTurn = False

        redrawAllWrapper(canvas, data)

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
    x.refreshSpecialTiles(EV.tripleWord, EV.doubleWord,
                          EV.doubleLetter, EV.tripleLetter)
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
    while not x.data.endOfGame:
        root.mainloop()  # blocks until window is closed
    print("bye!")


run(1000, 600)
