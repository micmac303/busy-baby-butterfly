import pygame
import sys
import random

# Constants for entity sizes
CATERPILLAR_SIZE = (60, 60)
FOOD_SIZE = (40, 40)

# Level configurations
LEVELS = {
    1: {
        "name": "Learning to Munch",
        "food_types": ["leaf"],
        "num_food": 5,
        "goal": 10,
        "message": "Eat 10 leaves to grow!"
    },
    2: {
        "name": "Growing Bigger",
        "food_types": ["leaf"],
        "num_food": 7,
        "goal": 15,
        "message": "Eat 15 leaves to continue growing!"
    },
    3: {
        "name": "Almost There",
        "food_types": ["leaf"],
        "num_food": 10,
        "goal": 20,
        "message": "Eat 20 leaves to transform!"
    }
}


class Caterpillar:
    """Represents the player's caterpillar."""

    def __init__(self, x, y, speed, window_width, window_height):
        """Initialize the caterpillar at the given position."""
        self.x = x
        self.y = y
        self.speed = speed
        self.window_width = window_width
        self.window_height = window_height
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
        self.x = max(0, min(self.x, self.window_width - self.width))
        self.y = max(0, min(self.y, self.window_height - self.height))

    def draw(self, screen):
        """Draw the caterpillar on the screen."""
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """Return the caterpillar's collision rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Food:
    """Represents a food item for the caterpillar to eat."""

    def __init__(self, x, y, food_type="leaf"):
        """Initialize food at the given position."""
        self.x = x
        self.y = y
        self.food_type = food_type
        self.image = self.load_image()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def load_image(self):
        """Load and scale the food image."""
        try:
            image = pygame.image.load(f"images/food/{self.food_type}.png")
            image = pygame.transform.scale(image, FOOD_SIZE)
            return image
        except pygame.error as e:
            print(f"Error loading food image: {e}")
            sys.exit()

    def draw(self, screen):
        """Draw the food on the screen."""
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """Return the food's collision rectangle."""
        return pygame.Rect(self.x, self.y, self.width, self.height)


# Game logic functions

def spawn_food(num_items, window_width, window_height, food_type="leaf"):
    """Spawn food items at random positions."""
    food_items = []
    for _ in range(num_items):
        x = random.randint(0, window_width - FOOD_SIZE[0])
        y = random.randint(0, window_height - FOOD_SIZE[1])
        food_items.append(Food(x, y, food_type))
    return food_items


def check_collisions(caterpillar, food_items):
    """Check if caterpillar collides with any food. Returns list of eaten food."""
    eaten = []
    caterpillar_rect = caterpillar.get_rect()

    for food in food_items:
        if caterpillar_rect.colliderect(food.get_rect()):
            eaten.append(food)

    return eaten