"""
This is our main driver file. it will handle the user input and displaying the current GameState. 
"""
import pygame as p
import sys
import ChessEngine as ch

WIDTH, HEIGHT = 640, 640
DIMENTION = 8 #the board is 8x8
SQ_SIZE = DIMENTION // HEIGHT
ICON = p.image.load("icon.ico")
MAX_FPS = 15
IMAGES = {}

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
    screen = p.display.set_mode((WIDTH, HEIGHT)) #setting the width and height of the screen
    screen.fill("white") #setting the back ground to white
    p.display.set_caption("--Chess Game--") #the text that appears at the top of the screen
    p.display.set_icon(ICON) #setting the icon
    gs = ch.GameState() #getting the acces to the GameState class 
    loadImg() #we need to call this once

    while True: #this will execute the game
        for event in p.event.get(): #we need to access to pygame.event
            if event.type == p.QUIT: #this means user click the close icon
                p.quit()
                sys.exit()      
        p.display.update()
main()