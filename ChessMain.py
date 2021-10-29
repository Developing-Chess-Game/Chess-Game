"""
This is our main driver file. it will handle the user input and displaying the current GameState. 
"""
import pygame as p
import sys
import ChessEngine as ch

WIDTH, HEIGHT = 640, 640
DIMENTION = 8 #the board is 8x8
SQ_SIZE = HEIGHT // DIMENTION
ICON = p.image.load("icon.ico")
MAX_FPS = 15
IMAGES = {}
#this will tell us when we must do a highlight on a selection
HIGHLIGHT = False 

"""
This help us to load the images in a less expensive way than loading every image in the same moment that they
are drawn in the screen. 
"""
#loading images into the IMAGES object
def loadImg():
    #we need the names of each pieces, lets create a list with all them together.
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces: #let's get through all the peaces name
        # Our object <IMAGES> should look like this: 
        # IMAGES = {"name_piece": imagen_of_the_piece}
        IMAGES[piece] = p.transform.scale(p.image.load("img/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

"""
This will store information about the screen and user interface, it will also update the 
Game state(our game board).
"""
def main():
    p.init() #we need to initialize pygame by calling the init method
    clock = p.time.Clock()
    screen = p.display.set_mode((WIDTH, HEIGHT)) #setting the width and height of the screen
    screen.fill("white") #setting the back ground to white
    p.display.set_caption("--Chess Game--") #the text that appears at the top of the screen
    p.display.set_icon(ICON) #setting the icon
    gs = ch.GameState() #getting the acces to the GameState class 
    validMoves = gs.validMoves() #we need to get the list of valid moves
    madeMove = False #the validMove() method is too expensive, we won't call it every frame

    loadImg() #we need to call this once
    sqSelected = () #this will store the mouse location(x, y)
    pClicks = [] #this will be our player clicks, it will store 2 tuples: [(4, 4), (5, 3)] 
    hClick = () #first click for highlights

    while True: #this will execute the game
        for event in p.event.get(): #we need to access to pygame.event
            if event.type == p.QUIT: #this means user click the close icon
                p.quit()
                sys.exit()
            #mouse event
            elif event.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos() #getting the mouse position
                col = pos[0] // SQ_SIZE #this is the column position
                row = pos[1] // SQ_SIZE #this is the row position where the mouse is located
                HIGHLIGHT = True
                hClick = (row, col) #getting the position of the mouse on the first click

                #if the user click 2 times on the piece's position we want to deselect
                if sqSelected == (row, col): #this means the user clicked two times in the same piece
                    sqSelected = () #reset the user clicks
                    pClicks = []
                else: #if the user doesn't click two times on the piece
                    sqSelected = (row, col)
                    pClicks.append(sqSelected)
                
                #we want to move the piece to the second location
                if len(pClicks) == 2: #this means that we most make the move
                    startSq = pClicks[0] #the first click
                    endSq = pClicks[1] #the second click
                    move = ch.Move(startSq, endSq, gs.board) #creating a move Object to store the information of the user clicks
                    if move in validMoves: #if the move is in the validMoves list, so do the move
                        gs.makeMove(move) #making the moves
                        madeMove = True
                        sqSelected = () #resets the user clicks
                        pClicks = []
                    else: #if it's not a valid moves, we want to have the last square selected
                        pClicks = [sqSelected]
            #Handle the key pressed
            if event.type == p.KEYDOWN: #if the user press a key
                if event.key == p.K_f: #if the key is equal to F
                    gs.undoMove() #undo the last move
                    sqSelected = () #reset the user clicks
                    pClicks = []
                    madeMove = True
        
        #every time we do a move, we need to updated the validMove with the current validMoves list
        #because it changes
        if madeMove:
            validMoves = gs.validMoves()
            madeMove = False        
        clock.tick(MAX_FPS)
        graphicInterface(screen, gs)

        #if pClicks at least have 1 element, it means that the first click has been made
        if len(pClicks) > 0:
            if HIGHLIGHT: #if high is true, we must draw the high light
                highLinght(screen, (hClick[0] * SQ_SIZE), (hClick[1] * SQ_SIZE), gs.board) #Draw the highlight
        p.display.update()

"""
This method display all the graphics on the screen
"""
def graphicInterface(screen, gs):
    drawBoard(screen) #this draws the grid of squares on the screen
    drawPieces(screen, gs.board) #this draw the pieces on the top of those squares

#THIS METHOD DRAW THE GRID
def drawBoard(screen):
    #we need two colors on our board, let's store those in a list
    colors = [p.Color("gray"), p.Color(120, 120, 120)]
    for r in range(DIMENTION): #the rows
        for c in range(DIMENTION): #the columns
            color = colors[(r+c)%2] #this helps us to select the right color
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#THIS METHOD DISPLAYS ALL THE PIECES
def drawPieces(screen, board):
    for r in range(DIMENTION): #rows
        for c in range(DIMENTION): #columns
            piece = board[r][c] #we access to each piece in our 2d list
            if piece != "--": #every time that it's not a empty square
                #display the image in the screen
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) 

#THIS METHOD DRAW THE HIGH LIGHT ON THE SELECTED SQUARE
def highLinght(screen, r, c, board):
    color = p.Color(47, 50, 72) # the color
    row = r // SQ_SIZE #row 
    col = c // SQ_SIZE #col
    piece = board[row][col] #getting the piece on the board to load the image on the highlinght
    if piece != "--": #if is not an empty square
        p.draw.rect(screen, color, p.Rect(c, r, SQ_SIZE, SQ_SIZE)) #highlight
        screen.blit(IMAGES[piece], p.Rect(c, r, SQ_SIZE, SQ_SIZE)) #image on the highlight

main()