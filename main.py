import pygame
import sys
from model import Caterpillar, spawn_food, check_collisions

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


def initialize_game():
    """Initialize Pygame and create the game window."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("The Busy Baby Butterfly")
    clock = pygame.time.Clock()
    return screen, clock


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


def draw_screen(screen, caterpillar, food_items):
    """Draw all game elements to the screen."""
    screen.fill(GREEN)

    # Draw all food items
    for food in food_items:
        food.draw(screen)

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
    caterpillar = Caterpillar(
        WINDOW_WIDTH // 2,
        WINDOW_HEIGHT // 2,
        CATERPILLAR_SPEED,
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )

    # Spawn initial food
    food_items = spawn_food(5, WINDOW_WIDTH, WINDOW_HEIGHT, "leaf")
    score = 0

    # Game loop
    running = True
    while running:
        running = handle_events()

        caterpillar.handle_movement()

        # Check for collisions with food
        eaten = check_collisions(caterpillar, food_items)
        for food in eaten:
            food_items.remove(food)
            score += 1
            # Spawn new food to replace eaten one
            new_food = spawn_food(1, WINDOW_WIDTH, WINDOW_HEIGHT, "leaf")
            food_items.extend(new_food)

        draw_screen(screen, caterpillar, food_items)

        # Draw score
        draw_text(screen, f"Score: {score}", 36, WHITE, 70, 30, center=False)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()