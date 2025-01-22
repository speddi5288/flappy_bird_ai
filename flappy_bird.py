import pygame
import neat
import time
import os
import random   # Used for random heights of the pipe image

# Total dimensions for the game size
# Constant valiables are capitalized (best-practice)
WIN_WIDTH = 600
WIN_HEIGHT = 800

# Want the bird images in sequence to make animation for easy reference
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

# Load all the images to be 2x bigger
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


# Bird class - Represents Bird Movement
class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25   # Rep. how much the bird will tilt
    ROT_VELOCITY = 20   # How much we will rotate on each frame / when bird moves [the background]
    ANIMATION_TIME = 5  # How fast the bird will be "moving" it's wings
    
    # Represents the starting postion of the bird
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0               # How much the img is tilted, start @ 0 [bird will be flat]
        self.tick_count = 0         # Physics of bird when action occurs ex: jumping
        self.velocity = 0                # Starting velocity @ 0 [not moving yet]
        self.height = self.y        # ---
        self.img_count = 0          # Keeps track of image that is shown
        self.img = self.IMGS[0]     # Start @ first image from the list
        
    def jump(self):
        self.velocity = -10.5       # Since pygame screen has the top left  @ (0,0). We need to have a negative number to move upwards on the y-axis
        self.tick_count = 0         # Keep track of when we last jumped [set to 0 b/c we need to know when we are changing directions/velocities for the formula in the next method to work] 
        self.height = self.y        # Keeps track of where the bird originally started moving from
    
    # This is what we call for every single frame that "moves" our bird
    def move(self):
        
        

# Ex: When calling the move function and we have multiple birds, we can use this move function to get all the bird objects to move @ the same time (30 frames per sec)
# while True:
#     bird.move()
         