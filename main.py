import pygame
import sys

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

# Game settings
FPS = 60
CATERPILLAR_SPEED = 5
CATERPILLAR_SIZE = (60, 60)


def initialize_game():
    """Initialize Pygame and create the game window."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("The Busy Baby Butterfly")
    clock = pygame.time.Clock()
    return screen, clock


def load_caterpillar_image():
    """Load and scale the caterpillar image."""
    try:
        image = pygame.image.load("images/caterpillar/caterpillar1.png")
        image = pygame.transform.scale(image, CATERPILLAR_SIZE)
        return image
    except pygame.error as e:
        print(f"Error loading caterpillar image: {e}")
        sys.exit()


def handle_events():
    """Handle Pygame events. Returns False if game should quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def handle_movement(x, y, image_width, image_height):
    """Handle caterpillar movement based on key presses."""
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= CATERPILLAR_SPEED
    if keys[pygame.K_RIGHT]:
        x += CATERPILLAR_SPEED
    if keys[pygame.K_UP]:
        y -= CATERPILLAR_SPEED
    if keys[pygame.K_DOWN]:
        y += CATERPILLAR_SPEED

    # Keep caterpillar within screen bounds
    x = max(0, min(x, WINDOW_WIDTH - image_width))
    y = max(0, min(y, WINDOW_HEIGHT - image_height))

    return x, y


def draw_screen(screen, caterpillar_image, x, y):
    """Draw all game elements to the screen."""
    screen.fill(GREEN)
    screen.blit(caterpillar_image, (x, y))
    pygame.display.flip()


def main():
    """Main game loop."""
    screen, clock = initialize_game()
    caterpillar_image = load_caterpillar_image()

    # Caterpillar starting position
    caterpillar_x = WINDOW_WIDTH // 2
    caterpillar_y = WINDOW_HEIGHT // 2

    # Game loop
    running = True
    while running:
        running = handle_events()

        caterpillar_x, caterpillar_y = handle_movement(
            caterpillar_x,
            caterpillar_y,
            caterpillar_image.get_width(),
            caterpillar_image.get_height()
        )

        draw_screen(screen, caterpillar_image, caterpillar_x, caterpillar_y)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()