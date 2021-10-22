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
        
        #Dictionary to create a data structure with all the pieces' methods
        self.moveMethods = {
            "R": self.rookMoves, "N": self.knightMoves, "B": self.bishopMoves,
            "Q": self.queenMoves, "K": self.kingMoves, "P": self.pawnMoves}
        self.whiteToMove = True
        self.moveLog = []
    
    #THIS METHOD WILL DO THE MOVE VISIBLE IN THE SCREEN
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" #the start move will be an empty square because the piece is moved
        self.board[move.endRow][move.endCol] = move.pieceMoved #we need to display the image in the new location
        self.moveLog.append(move) #we will use this movelog to keep track of all the move
        self.whiteToMove = not self.whiteToMove #switch turn between players
    
    #THIS METHOD WILL UNDO THE LAST MOVE
    def undoMove(self):
        if len(self.moveLog) != 0: #checking if there is at least one move to undo.
            move = self.moveLog.pop() #we removed the last move and assign it to the <move> variable
            self.board[move.startRow][move.startCol] = move.pieceMoved #setting the start Square to how it was before the move
            self.board[move.endRow][move.endCol] = move.pieceCaptured #setting end square to how it was before the move
            self.whiteToMove = not self.whiteToMove #switch the player's turn
    
    #THIS WILL GET ALL THE VALID MOVES WITH CHECK(THE KING)
    def validMoves(self):
        return self.allPosiblesMoves() #Generating all the posibles moves
    
    #THIS WILL GET ALL POSIBLES MOVE WITHOUT CHECK THE KING
    def allPosiblesMoves(self):
        moves = [] #It stores the posibles moves
        for r in range(len(self.board)): #All the rows in the board
            for c in range(len(self.board[r])): #All the columns in the board
                piece_color = self.board[r][c][0] #This is gonna be equal to the first caracter of each element
                if (piece_color == "w" and self.whiteToMove) or (piece_color == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1] #This obtain the piece type
                    self.moveMethods[piece](r, c, moves) #Calling the moveMethods
        return moves #We return the list of posibles moves
    
    #THIS GETS THE POSIBLES MOVES TO --PAWN-- PIECE
    def pawnMoves(self, r, c, moves):
        pass


    #THIS GETS THE POSIBLES MOVES TO --ROOK-- PIECE
    def rookMoves(self, r, c, moves):
        pass


    #THIS GETS THE POSIBLES MOVES TO --BISHOP-- PIECE
    def bishopMoves(self, r, c, moves):
        pass


    #THIS GETS THE POSIBLES MOVES TO --QUEEN-- PIECE
    def queenMoves(self, r, c, moves):
        pass


    #THIS GETS THE POSIBLES MOVES TO --KNIGHT-- PIECES
    def knightMoves(self, r, c, moves):
        pass


    #THIS GETS THE POSIBLES MOVES TO --KING-- PIECE
    def kingMoves(self, r, c, moves):
        pass


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
        #Start square
        self.startRow = startSq[0]
        self.startCol = startSq[1]

        #End square
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol] #this keep track of what piece was moved
        self.pieceCaptured = board[self.endRow][self.endCol] #this captured the piece that was in the last square
        self.ID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol #we need this to compare 2 moves
    
    #THIS METHOD GET THE CHESS NOTATION OF THE FIRST POSITION AND THE LAST POSITION AND RETURN THE STRING
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    #We need to do this because we are not allow to compare 2 objects
    #OVERRIDING THE EQUAL OPERATOR
    def __eq__(self, o):
        if isinstance(o, Move): #we need to check if it's instance of an move object
            return (self.ID == o.ID) #Comparing the ID to know if they are the same
        return False

    
    #THIS METHOD GET THE CHESS NOTATION BUT JUST OF ONE POSTITION AND RETURN THE STRING
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r] 