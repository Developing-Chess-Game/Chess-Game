"""
This class will store all the information of the current state of the chess game. It will also determinate the valid 
moves at the current state. it will also keep a move log to use it to make undo moves.
"""

"""
This class will store information about the game state
"""
class GameState():
    def __init__(self):
        #our boar is a 2d list, each element has 2 caracters
        #the first one means the color, it can be b(black) or w(white)
        #the second one means the type of the piece, it can be R(Rook), N(knight), B(bishop), P(pawn), Q(queen) and K(king)
        #the "--" caracter means a white square with no pieces
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
        self.whiteToMove = True
        self.moveLog = []


"""
This class is used to store information about the moves
"""
class Move():
    #map keys to values
    #keys: values
    #we want to obtain the chess notation in every move
    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4,
        "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {
        "a": 0, "b": 1, "c": 2, "d": 3,
        "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        #this variables keep tracks of what piece have been moved, and the capture of what the pieces new
        #location is
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
    
    #THIS METHOD GET THE CHESS NOTATION OF THE FIRST POSITION AND THE LAST POSITION AND RETURN THE STRING
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    #THIS METHOD GET THE CHESS NOTATION BUT JUST OF ONE POSTITION AND RETURN THE STRING
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r] 