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
        #kings' location
        self.wK = (7, 4) #white king's location
        self.bK = (0, 4) #black king's location

        self.checkmate = False
        self.stalemate = False         
    
    #THIS METHOD WILL DO THE MOVE VISIBLE IN THE SCREEN
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" #the start move will be an empty square because the piece is moved
        self.board[move.endRow][move.endCol] = move.pieceMoved #we need to display the image in the new location
        self.moveLog.append(move) #we will use this movelog to keep track of all the move
        #if a pawn piece arrive to the enemy's king's row it can become into a queen piece
        if self.whiteToMove: #white pawns
            if move.pieceMoved == "wP" and move.endRow == 0: #if the pawn arrive to the opposite king's row
                self.board[move.endRow][move.endCol] = "wQ"  #it becomes itself into a Queen piece
        else: #black's pawns
            if move.pieceMoved == "bP" and move.endRow == 7: #if the pawn arrive to the opposite king's row
                self.board[move.endRow][move.endCol] = "bQ" #it becomes itself into a Queen piece
        self.whiteToMove = not self.whiteToMove #switch turn between players

        #Update the king's location
        if move.pieceMoved == "wK": #if white king was moved
            self.wK = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":#if black king was moved
            self.bK = (move.endRow, move.endCol)
    
    #THIS METHOD WILL UNDO THE LAST MOVE
    def undoMove(self):
        if len(self.moveLog) != 0: #checking if there is at least one move to undo.
            move = self.moveLog.pop() #we removed the last move and assign it to the <move> variable
            self.board[move.startRow][move.startCol] = move.pieceMoved #setting the start Square to how it was before the move
            self.board[move.endRow][move.endCol] = move.pieceCaptured #setting end square to how it was before the move
            self.whiteToMove = not self.whiteToMove #switch the player's turn

            #Update the king's location
            if move.pieceMoved == "wK": #if white king part of a undo moved
                self.wK = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK": #if white king part of a undo moved
                self.bK = (move.startRow, move.startCol)
    
    #THIS WILL GET ALL THE VALID MOVES WITH CHECK(THE KING)
    def validMoves(self):
        #Getting all the posibles moves
        moves = self.allPosiblesMoves()
        #for each move in moves list, make the move
        #we are going to delete elements from moves list, so we need to iterate it backwards to evoid bugs
        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i]) #making the move
            self.whiteToMove = not self.whiteToMove #switching the turn back because the makeMove() method switch turns
            #check if our king is in check
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove #switching the turn 
            self.undoMove()                         #to undo the move
        
        #checking if the king is in checkmate or the game will end with a stalemate
        if len(moves) == 0:
            if self.inCheck(): #if is in check, we want our checkmate variable to be True
                self.checkmate = True
            else: #else we want our stalemate variable to be True
                self.stalemate = True

        return moves
    
    #THIS METHOD IS GOING TO RETURN TRUE OR FALSE, IT DEPENDS IF THE KING IS IN CHECK
    def inCheck(self):
        if self.whiteToMove: #white's turn 
            return self.sqUnderAttack(self.wK[0], self.wK[1])
        else: #black's turn
            return self.sqUnderAttack(self.bK[0], self.bK[1])
    
    def sqUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switching the turn to get the opposite moves
        oppMoves = self.allPosiblesMoves() #opposite moves
        self.whiteToMove = not self.whiteToMove #switching back

        #we need to access to those moves
        for move in oppMoves:
            #if any oppMove attack our king, we need to return True, otherwise return False
            if move.endRow == r and move.endCol == c:
                return True
        return False

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
        if self.whiteToMove: # white player's turn
            if self.board[r-1][c] == "--": #If the square in front of the piece is empty add the move to moves
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #the pawns can move 2 squares in the first move     
                    moves.append(Move((r, c), (r-2, c), self.board))

            #PAWN CAPTURES
            #pawn can capture to ether left or right by moving diagonally
            if (c-1 >= 0): #Overpassing the left edge of the screen is not allow
                if self.board[r-1][c-1][0] == 'b': #left capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))

            if (c+1 <= 7): #we don't want to overpass the right edge of the screen 
                if self.board[r-1][c+1][0] == 'b': #right capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            

        else: #black player's turn
            if self.board[r+1][c] == "--": #if the square in front of the piece is empty, add that move to moves  
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #the pawns can move 2 squares in the first move     
                    moves.append(Move((r, c), (r+2, c), self.board))
            
            #PAWN CAPTURES
            #pawn can capture to ether left or right by moving diagonally
            if (c-1) >= 0: #overpassing the left edge is not allow
                if self.board[r+1][c-1][0] == "w": #left capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            
            if (c+1) <= 7: #overpassing the right edge is not allow
                if self.board[r+1][c+1][0] == "w": #right capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))


    #THIS GETS THE POSIBLES MOVES TO --ROOK-- PIECE
    def rookMoves(self, r, c, moves):
        move_dir = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        eColor = "b" if self.whiteToMove else "w" #enemy color
        for d in move_dir: #getting all the move direction
            for i in range(1, 8): 
                endRow = r + d[0] * i #getting the row position of the last square
                endCol = c + d[1] * i #getting the col position of the last square
                if 0 <= endRow < 8 and 0 <= endCol < 8: #Checking our board's edges
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty sq is a valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == eColor: #enemy piece is a valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break #we want to stop our adding moves once we find a enemy piece along the way
                    else: #frienly piece is not a valid move
                        break
                else: #endRow and endCol are out the board
                    break


    #THIS GETS THE POSIBLES MOVES TO --BISHOP-- PIECE
    def bishopMoves(self, r, c, moves):
        #bishop can move diagonaly
        #diagonally right direction, backward and forward
        #diagonally left drection, backward and forward
        move_dir = ((-1, -1), (-1, 1), (1, -1), (1, 1))  
        eColor = "b" if self.whiteToMove else "w" #enemy color
        for d in move_dir: #getting all the move direction
            for i in range(1, 8): 
                endRow = r + d[0] * i #getting the row position of the last square
                endCol = c + d[1] * i #getting the col position of the last square
                if 0 <= endRow < 8 and 0 <= endCol < 8: #Checking our board's edges
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty sq is a valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == eColor: #enemy piece is a valid move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break #we want to stop our adding moves once we find a enemy piece along the way
                    else: #frienly piece is not a valid move
                        break
                else: #endRow and endCol are out the board
                    break


    #THIS GETS THE POSIBLES MOVES TO --QUEEN-- PIECE
    def queenMoves(self, r, c, moves):
        #The queen is a combination of rook and bishop moves
        self.rookMoves(r, c, moves) #getting the rook moves
        self.bishopMoves(r, c, moves) #getting the bishop moves


    #THIS GETS THE POSIBLES MOVES TO --KNIGHT-- PIECES
    def knightMoves(self, r, c, moves):
        #the Knight can moves in whatever direction but doing an L move
        knightMoves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (1, -2), (-1, -2), (2, -1), (2, 1)) 
        friendsColor = "w" if self.whiteToMove else "b" #the friends color
        for m in knightMoves: #getting all the moves of the knight
            endRow = r + m[0] #the end rows
            endCol = c + m[1] #the end column
            if 0 <= endRow < 8 and 0 <= endCol < 8:#Checking our board's edges
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != friendsColor: #it means that every move that is an empty or enemy piece will be a valid move
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    #THIS GETS THE POSIBLES MOVES TO --KING-- PIECE
    def kingMoves(self, r, c, moves):
        #the king can move in whatever direction, but only one step
        kingMoves = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
        friendsColor = "w" if self.whiteToMove else "b" #the friends color
        for i in range(8): #getting all the moves of the king
            endRow = r + kingMoves[i][0] #the end rows
            endCol = c + kingMoves[i][1] #the end column
            if 0 <= endRow < 8 and 0 <= endCol < 8:#Checking our board's edges
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != friendsColor: #it means that every move that is an empty or enemy piece will be a valid move
                    moves.append(Move((r, c), (endRow, endCol), self.board))



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