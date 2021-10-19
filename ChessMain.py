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