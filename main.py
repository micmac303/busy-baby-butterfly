import pygame
import sys
from model import Caterpillar, spawn_food, check_collisions, LEVELS, get_caterpillar_size

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


def show_level_start_screen(screen, clock, level_config):
    """Display the story text before starting a level."""
    waiting = True
    start_time = pygame.time.get_ticks()
    min_wait_time = 2000  # Minimum 2 seconds to read

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Only allow skipping after minimum time
                if pygame.time.get_ticks() - start_time > min_wait_time:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        waiting = False

        # Auto-advance after 4 seconds
        if pygame.time.get_ticks() - start_time > 4000:
            waiting = False

        # Draw story screen
        screen.fill(DARK_GREEN)

        # Day name
        draw_text(screen, level_config['name'], 64, LIGHT_YELLOW,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)

        # Story text
        draw_text(screen, level_config['story_text'], 36, WHITE,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Hint
        if pygame.time.get_ticks() - start_time > min_wait_time:
            draw_text(screen, "Press any key to continue...", 24, LIGHT_YELLOW,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 // 4)

        pygame.display.flip()
        clock.tick(FPS)


def show_level_complete_screen(screen, clock, level_num, level_config):
    """Display level complete screen with story message."""
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
                    waiting = False

        # Draw completion screen
        screen.fill(DARK_GREEN)

        # Special message for Saturday (stomachache)
        if level_num == 6:
            draw_text(screen, "Oh no!", 64, (255, 100, 100),
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
            draw_text(screen, level_config['message'], 42, WHITE,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        # Special message for Sunday (feels better)
        elif level_num == 7:
            draw_text(screen, "Ahh, much better!", 64, LIGHT_YELLOW,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
            draw_text(screen, "Now he was a big, fat caterpillar!", 38, WHITE,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            draw_text(screen, "Time to build a cocoon...", 32, LIGHT_YELLOW,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
        else:
            # Regular completion
            draw_text(screen, level_config['message'], 48, WHITE,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Continue prompt
        if level_num < 7:
            draw_text(screen, "Press any key to continue", 32, LIGHT_YELLOW,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 // 4)
        else:
            draw_text(screen, "Press any key for the transformation!", 32, LIGHT_YELLOW,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 // 4)

        pygame.display.flip()
        clock.tick(FPS)


def show_butterfly_ending(screen, clock):
    """Show the final butterfly transformation."""
    # Load images
    try:
        cocoon_img = pygame.image.load("images/caterpillar/cocoon.png")
        cocoon_img = pygame.transform.scale(cocoon_img, (180, 180))
        butterfly_img = pygame.image.load("images/caterpillar/butterfly.png")
        butterfly_img = pygame.transform.scale(butterfly_img, (250, 250))
    except pygame.error as e:
        print(f"Error loading transformation images: {e}")
        # Fallback to emojis if images not found
        cocoon_img = None
        butterfly_img = None

    # Cocoon phase
    waiting = True
    cocoon_time = pygame.time.get_ticks()
    cocoon_duration = 3000  # 3 seconds

    while waiting and pygame.time.get_ticks() - cocoon_time < cocoon_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(DARK_GREEN)

        # Draw cocoon
        if cocoon_img:
            cocoon_rect = cocoon_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            screen.blit(cocoon_img, cocoon_rect)

        draw_text(screen, "Building a cocoon...", 48, WHITE,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150)
        draw_text(screen, "Resting for two weeks...", 36, LIGHT_YELLOW,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 130)

        # Simple animation - pulsing dots
        dots = "." * ((pygame.time.get_ticks() // 500) % 4)
        draw_text(screen, f"zzz{dots}", 32, WHITE,
                  WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 170)

        pygame.display.flip()
        clock.tick(FPS)

    # Butterfly emergence - with fade in effect
    waiting = True
    emergence_time = pygame.time.get_ticks()
    fade_duration = 1000  # 1 second fade

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

        # Calculate fade alpha (0 to 255)
        elapsed = pygame.time.get_ticks() - emergence_time
        alpha = min(255, int((elapsed / fade_duration) * 255))

        # Sky blue background
        screen.fill((135, 206, 250))

        # Draw butterfly with fade effect
        if butterfly_img and elapsed < fade_duration:
            # Create a copy with alpha for fade effect
            faded_butterfly = butterfly_img.copy()
            faded_butterfly.set_alpha(alpha)
            butterfly_rect = faded_butterfly.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            screen.blit(faded_butterfly, butterfly_rect)
        elif butterfly_img:
            # Fully visible
            butterfly_rect = butterfly_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            screen.blit(butterfly_img, butterfly_rect)
        else:
            # Fallback emoji
            draw_text(screen, "🦋", 120, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80)

        # Text appears after fade
        if elapsed > fade_duration:
            draw_text(screen, "He was a beautiful butterfly!", 52, (255, 215, 0),
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 140)
            draw_text(screen, "The End", 42, WHITE,
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 200)
            draw_text(screen, "Press any key to exit", 28, (200, 200, 200),
                      WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 250)

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

        # Show story text before level starts
        show_level_start_screen(screen, clock, level_config)

        # Get caterpillar size for this level (grows each level!)
        caterpillar_size = get_caterpillar_size(current_level)

        # Create caterpillar at center of screen
        caterpillar = Caterpillar(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            CATERPILLAR_SPEED,
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            caterpillar_size
        )

        # Spawn food for this level
        food_items = spawn_food(
            level_config["num_food"],
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            level_config["food_types"]
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
                score += 1

            # Check if level goal is reached
            if level_score >= level_config["goal"]:
                level_running = False
                show_level_complete_screen(screen, clock, current_level, level_config)
                current_level += 1

            # Draw everything
            draw_screen(screen, caterpillar, food_items)

            # Draw level info
            draw_text(screen, f"{level_config['name']}", 32, WHITE,
                      WINDOW_WIDTH // 2, 20, center=True)
            draw_text(screen, f"Eaten: {level_score}/{level_config['goal']}", 28, WHITE,
                      70, 50, center=False)

            pygame.display.flip()
            clock.tick(FPS)

    # Show butterfly ending after completing all levels
    if current_level > 7:
        show_butterfly_ending(screen, clock)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
