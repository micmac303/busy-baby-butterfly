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

# Load caterpillar image
try:
    caterpillar_image = pygame.image.load("images/caterpillar/caterpillar1.png")
    # Scale image if needed (adjust size as you prefer)
    caterpillar_image = pygame.transform.scale(caterpillar_image, (60, 60))
except pygame.error as e:
    print(f"Error loading caterpillar image: {e}")
    sys.exit()

# Caterpillar position and movement speed
caterpillar_x = WINDOW_WIDTH // 2
caterpillar_y = WINDOW_HEIGHT // 2
caterpillar_speed = 5

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        caterpillar_x -= caterpillar_speed
    if keys[pygame.K_RIGHT]:
        caterpillar_x += caterpillar_speed
    if keys[pygame.K_UP]:
        caterpillar_y -= caterpillar_speed
    if keys[pygame.K_DOWN]:
        caterpillar_y += caterpillar_speed

    # Keep caterpillar within screen bounds
    caterpillar_x = max(0, min(caterpillar_x, WINDOW_WIDTH - caterpillar_image.get_width()))
    caterpillar_y = max(0, min(caterpillar_y, WINDOW_HEIGHT - caterpillar_image.get_height()))

    # Fill the screen with a color
    screen.fill(GREEN)

    # Draw the caterpillar
    screen.blit(caterpillar_image, (caterpillar_x, caterpillar_y))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()