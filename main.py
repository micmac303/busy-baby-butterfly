import pygame
import sys

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
DARK_GREEN = (20, 80, 20)
LIGHT_YELLOW = (255, 255, 200)

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


class Caterpillar:
    """Represents the player's caterpillar."""

    def __init__(self, x, y):
        """Initialize the caterpillar at the given position."""
        self.x = x
        self.y = y
        self.speed = CATERPILLAR_SPEED
        self.image = self.load_image()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def load_image(self):
        """Load and scale the caterpillar image."""
        try:
            image = pygame.image.load("images/caterpillar/caterpillar1.png")
            image = pygame.transform.scale(image, CATERPILLAR_SIZE)
            return image
        except pygame.error as e:
            print(f"Error loading caterpillar image: {e}")
            sys.exit()

    def handle_movement(self):
        """Update position based on key presses."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Keep caterpillar within screen bounds
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))
        self.y = max(0, min(self.y, WINDOW_HEIGHT - self.height))

    def draw(self, screen):
        """Draw the caterpillar on the screen."""
        screen.blit(self.image, (self.x, self.y))


def handle_events():
    """Handle Pygame events. Returns False if game should quit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
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


def draw_screen(screen, caterpillar):
    """Draw all game elements to the screen."""
    screen.fill(GREEN)
    caterpillar.draw(screen)
    pygame.display.flip()


def draw_text(screen, text, size, color, x, y, center=True):
    """Draw text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def show_start_screen(screen, clock):
    """Display the start screen and wait for Enter key."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Draw start screen
        screen.fill(DARK_GREEN)

        # Title
        draw_text(screen, "The Busy Baby Butterfly!", 72, LIGHT_YELLOW,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)

        # Instructions
        draw_text(screen, "Use ARROW KEYS to move", 36, WHITE,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        draw_text(screen, "Eat to grow and become a butterfly!", 36, WHITE,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)

        # Start prompt
        draw_text(screen, "Press ENTER to start", 42, LIGHT_YELLOW,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3 + 50)
        draw_text(screen, "Press ESC to quit", 28, WHITE,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3 + 100)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    """Main game loop."""
    screen, clock = initialize_game()

    # Show start screen
    show_start_screen(screen, clock)

    # Create caterpillar at center of screen
    caterpillar = Caterpillar(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    # Game loop
    running = True
    while running:
        running = handle_events()

        caterpillar.handle_movement()

        draw_screen(screen, caterpillar)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()