import pygame
import neat
import time
import os
import random  # Used for random heights of the pipe image

# Total dimensions for the game size
# Constant valiables are capitalized (best-practice)
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Want the bird images in sequence to make animation for easy reference
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

# Load all the images to be 2x bigger
PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png"))
)
BASE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png"))
)
BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png"))
)


# Bird class - Represents Bird Movement
class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25  # Rep. how much the bird will tilt
    ROT_VELOCITY = (
        20  # How much we will rotate on each frame / when bird moves [the background]
    )
    ANIMATION_TIME = 5  # How fast the bird will be "moving" it's wings

    # Represents the starting postion of the bird
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # How much the img is tilted, start @ 0 [bird will be flat]
        self.tick_count = 0  # Physics of bird when action occurs ex: jumping
        self.velocity = 0  # Starting velocity @ 0 [not moving yet]
        self.height = self.y  # ---
        self.img_count = 0  # Keeps track of image that is shown
        self.img = self.IMGS[0]  # Start @ first image from the list

    def jump(self):
        self.velocity = (
            -10.5
        )  # Since pygame screen has the top left  @ (0,0). We need to have a negative number to move upwards on the y-axis
        self.tick_count = 0  # Keep track of when we last jumped [set to 0 b/c we need to know when we are changing directions/velocities for the formula in the next method to work]
        self.height = (
            self.y
        )  # Keeps track of where the bird originally started moving from

    # Ex: When calling the move function and we have multiple birds, we can use this move function to get all the bird objects to move @ the same time (30 frames per sec)
    # while True:
    #     bird.move()

    # This is what we call for every single frame that "moves" our bird
    def move(self):
        self.tick_count += 1  # A frame went by

        # Creates an arc for the bird as it does its jump (ascending to descending)
        d = (
            self.velocity * self.tick_count + 1.5 * self.tick_count**2
        )  # How many pixels we are moving up/down this frame

        if (
            d >= 16
        ):  # If we are moving down more than 16 set the max movement down to be only 16
            d = 16

        # If we are moving upwards, move up a little more (makes movements more clean)
        if d < 0:
            d -= 2

        self.y = self.y + d

        # Dont tilt the bird downwards until the bird reaches the starting y-level of the beggining of the jump
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = (
                    self.MAX_ROTATION
                )  # immediately set the tilt of the bird to be 25 deg
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VELOCITY  # rotate bird 90 deg

    def draw(self, win):
        self.img_count += 1  # shows how many times we have shown 1 image

        # Gets to wings to flap up / down
        # if img count is less than 5 display first image, if img count is less than 10: display 1st bird image and so on, up until less than 16
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # When bird is nosediving we dont want it to flap its wings
        if self.tilt <= -80:
            self.img = self.IMGS[1]  # Goes to the image where the wings are flat
            self.img_count = (
                self.ANIMATION_TIME * 2
            )  # When we jump back up it doesn't skip a frame [goes from nosdive to flat (doesnt skip flat) to up]

        # Rotates image around the center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200  # Space btween pipe
    VEL = 5  # Since bird doesnt move, only objects

    def __init__(self, x):
        self.x = x
        self.height = 0

        # Variable to keep track of top / bottom of pipe, (imgs for top + bottom pipe)
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(
            PIPE_IMAGE, False, True
        )  # flips image for the top pipe
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed = False
        self.set_height()

    def set_height(self):
        # Random height for pipe on top of screen
        self.height = random.randrange(40, 450)

        # In order to find the where the top of the pipe should be
        # We need to figure out the top left position for the image of the pipe
        # So we need the height of the image from the top point to wherever the random val is and subtract
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        # Move the pipe by changing x position based on the velocity given each fram
        self.x -= self.VEL
         
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    # Masks looks @ an image and finds out where the pixels are for more realstic collisions (instead of standard hitboxes)
    # Masks will create a 2d array of rows that have pixels and columns that have pixels 
    def collide(self, bird):
        bird_mask = bird.get_mask()     # get mask to start
        
        # mask for top pipe and for bottom pipe
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        # offset calc -> how far away these masks are from each other
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.top - round(bird.y))

        # Tells pt. of collision btwn bird mast and bottom /top pipe mask
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if t_point or b_point:
            return True
        
        return False

# Explain it later
class Base:
    VEL = 5
    WIDTH = BASE_IMAGE.get_width
    IMG = BASE_IMAGE
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
        def move(self):
            self.x1 -= self.VEL
            self.x2 -= self.VEL
            
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        

# Draw the background image then draw the bird
def draw_window(win, bird):
    win.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the backroung image at top left of screen
    bird.draw(
        win
    )  # Call draw method to handle all the animation / tilting / and drawing the bird
    pygame.display.update()  # Refresh the display


def main():
    bird = Bird(200, 200)  # Calls the bird class & puts it in a starting position
    win = pygame.display.set_mode(
        (WIN_WIDTH, WIN_HEIGHT)
    )  # Creates the window for the game
    clock = pygame.time.Clock()

    run = True  # So that we can start and end the game

    while run:
        clock.tick(30)  # 30 fps
        for event in pygame.event.get():

            # if we press the red x in pygame -> exits the game
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        draw_window(win, bird)  # Call funtion to see our bird

    pygame.quit()  # quit pygmae
    quit()  # also quits program


main()
