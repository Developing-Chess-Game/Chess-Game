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
