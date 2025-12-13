import pygame
import sys
from model import Caterpillar, spawn_food, check_collisions, LEVELS

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


def show_level_complete_screen(screen, clock, level_num):
    """Display level complete screen and wait for any key."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    # Any other key proceeds to next level
                    waiting = False

        # Draw level complete screen
        screen.fill(DARK_GREEN)

        # Congratulations message
        draw_text(screen, f"Level {level_num} Complete!", 64, LIGHT_YELLOW,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)

        draw_text(screen, "Great job munching!", 42, WHITE,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Check if there's a next level
        if level_num + 1 in LEVELS:
            next_level = LEVELS[level_num + 1]
            draw_text(screen, f"Next: {next_level['name']}", 36, WHITE,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
            draw_text(screen, next_level['message'], 32, LIGHT_YELLOW,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)

            draw_text(screen, "Press any key to continue", 38, WHITE,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3 + 50)
        else:
            # Game complete!
            draw_text(screen, "You've completed all levels!", 42, LIGHT_YELLOW,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
            draw_text(screen, "Press any key to exit", 38, WHITE,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT * 2 // 3 + 50)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    """Main game loop."""
    screen, clock = initialize_game()

    # Show start screen
    show_start_screen(screen, clock)

    # Game state
    current_level = 1
    score = 0

    # Game loop - continues across levels
    running = True
    while running and current_level in LEVELS:
        # Get current level configuration
        level_config = LEVELS[current_level]

        # Create caterpillar at center of screen
        caterpillar = Caterpillar(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            CATERPILLAR_SPEED,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
        )

        # Spawn food for this level
        food_items = spawn_food(
            level_config["num_food"],
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            level_config["food_types"][0]  # Use first food type for now
        )

        # Reset score for this level
        level_score = 0

        # Level loop
        level_running = True
        while level_running and running:
            running = handle_events()

            caterpillar.handle_movement()

            # Check for collisions with food
            eaten = check_collisions(caterpillar, food_items)
            for food in eaten:
                food_items.remove(food)
                level_score += 1
                score += 1  # Total score across all levels

                # Spawn new food to replace eaten one
                new_food = spawn_food(
                    1,
                    WINDOW_WIDTH,
                    WINDOW_HEIGHT,
                    level_config["food_types"][0]
                )
                food_items.extend(new_food)

            # Check if level goal is reached
            if level_score >= level_config["goal"]:
                level_running = False  # Exit level loop
                show_level_complete_screen(screen, clock, current_level)
                current_level += 1  # Move to next level

            # Draw everything
            draw_screen(screen, caterpillar, food_items)

            # Draw level info and score
            draw_text(screen, f"Level {current_level}: {level_config['name']}", 32, WHITE,
                      WINDOW_WIDTH // 2, 20, center=True)
            draw_text(screen, f"Goal: {level_score}/{level_config['goal']}", 28, WHITE,
                      70, 50, center=False)
            draw_text(screen, f"Total Score: {score}", 28, WHITE,
                      70, 80, center=False)

            pygame.display.flip()
            clock.tick(FPS)

    # Game completed or quit
    if current_level not in LEVELS:
        # All levels completed - show final screen
        show_level_complete_screen(screen, clock, current_level - 1)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()