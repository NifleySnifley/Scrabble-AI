BOARDSIZE = 21


class boardKeeper():

    def __init__(self):
        # 21x21
        self.board = "-" * (BOARDSIZE*BOARDSIZE)
        self.spaceOccupations = {}

    def changeBoard(self, letterCombo, spaceCombo, player):
        for (letter, space) in zip(letterCombo, spaceCombo):
            self.spaceOccupations[space] = player
            self.board = self.board[:space] + letter + self.board[space+1:]

    def printBoard(self):
        ''' Prints the board with either an error or a passing statement '''
        board = self.board
        print('Here is the current board situation.')
        for row in range(int(len(board)//BOARDSIZE)):
            # print(row, end = ' ')  ## for future extension
            for column in range(BOARDSIZE):
                print(board[BOARDSIZE*row + column], end=' ')
            print('')

    def refreshOccupied(self):
        ''' Get locations occupied by a letter '''
        board = self.board
        occupied = []
        for spot in range(len(board)):
            if board[spot] not in '-23@#':
                occupied.append(spot)
        return occupied

    def refreshAttachments(self):
        ''' Finds every place where a word could start (called attachments) given a board '''
        board = self.board
        attachments = set([])

        for i in range(len(board)):
            if board[i] not in '-23@#':
                row = i//BOARDSIZE
                column = i % BOARDSIZE
                # space directions
                down = (row-1)*BOARDSIZE + column
                up = (row+1)*BOARDSIZE + column
                left = row*BOARDSIZE + column-1
                right = row*BOARDSIZE + column+1

                # attachments are added
                if (row != 0) and (board[down] in '-23@#') and (down not in attachments):
                    attachments.add(down)
                if (row != (BOARDSIZE-1)) and (board[up] in '-23@#') and (up not in attachments):
                    attachments.add(up)
                if (column != 0) and (board[left] in '-23@#') and (left not in attachments):
                    attachments.add(left)
                if (column != (BOARDSIZE-1)) and (board[right] in '-23@#') and (right not in attachments):
                    attachments.add(right)

        if len(attachments) == 0:
            attachments.add((BOARDSIZE*BOARDSIZE) // 2)

        return attachments
