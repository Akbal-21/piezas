'''Clase respondable de la información '''


class GameState():
    def __init__(self):
        # declaración del tablero donde se muestra en el primer caracter
        # lo que representa en este caso son reyes y la segunda letra el color blanco y negro respectivamente
        # y los -- son espacios en blanco
        self.board = [
            ["wK", "--", "--", "bK"],
            ["--", "--", "--", "--"],
            ["--", "--", "--", "--"],
            ["--", "--", "--", "--"]
        ]
        self.moveFuctions = {"K": self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.starCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    '''regresar pasos'''

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.starCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCapture
            self.whiteToMove = not self.whiteToMove

    '''movimientos checados'''

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    '''Moviemientos posibles'''

    def getAllPossibleMoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn = self.board[i][j][0]
                if (turn == "w" and self.whiteToMove) and (turn == "b" and not self.whiteToMove):
                    piece = self.board[i][j][1]
                    self.moveFuctions[piece](i, j, moves)
        return moves

    def getKingMoves(self, i, j, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColo = "W" if self.whiteToMove else "B"
        for m in knightMoves:
            endRow = i + m[0]
            endCol = j + m[1]
            if 0 <= endRow < 4 and 0 <= endCol < 4:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColo:
                    moves.append(Move((i, j), (endRow, endCol), self.board))


class Move():
    rankToRows = {"1": 3, "2": 2, "3": 1, "4": 0}
    rowsToRank = {v: k for k, v in rankToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSQ, endSQ, board):
        self.startRow = startSQ[0]
        self.starCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.starCol]
        self.pieceCapture = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.starCol * 100 + self.endRow * 10 + self.endCol
        # print(self.moveID)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.starCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRank[r]
