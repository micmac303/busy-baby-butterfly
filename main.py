import pygame
import sys

# Initialize Pygame
pygame.init()

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Busy Baby Butterfly")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color
    screen.fill(GREEN)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()