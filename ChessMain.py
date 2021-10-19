"""
This is our main driver file. it will handle the user input and displaying the current GameState. 
"""
import pygame as p
import sys
import ChessEngine

WIDTH, HEIGHT = 640, 640
DIMENTION = 8 #the board is 8x8
SQ_SIZE = DIMENTION // HEIGHT
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
