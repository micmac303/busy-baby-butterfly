import pygame
import sys
import random

# Constants for entity sizes
CATERPILLAR_SIZE = (60, 60)
FOOD_SIZE = (40, 40)

# Level configurations - Following "The Very Hungry Caterpillar" story
LEVELS = {
    1: {
        "name": "Monday",
        "story_text": "On Monday, he ate through one apple.",
        "food_types": ["apple"],
        "num_food": 1,
        "goal": 1,
        "message": "But he was still hungry."
    },
    2: {
        "name": "Tuesday",
        "story_text": "On Tuesday, he ate through two pears.",
        "food_types": ["pear"],
        "num_food": 2,
        "goal": 2,
        "message": "But he was still hungry."
    },
    3: {
        "name": "Wednesday",
        "story_text": "On Wednesday, he ate through three plums.",
        "food_types": ["plum"],
        "num_food": 3,
        "goal": 3,
        "message": "But he was still hungry."
    },
    4: {
        "name": "Thursday",
        "story_text": "On Thursday, he ate through four strawberries.",
        "food_types": ["strawberry"],
        "num_food": 4,
        "goal": 4,
        "message": "But he was still hungry."
    },
    5: {
        "name": "Friday",
        "story_text": "On Friday, he ate through five oranges.",
        "food_types": ["orange"],
        "num_food": 5,
        "goal": 5,
        "message": "But he was still hungry."
    },
    6: {
        "name": "Saturday",
        "story_text": "On Saturday, he ate through all sorts of things...",
        "food_types": ["cake", "icecream", "pickle", "cheese", "salami",
                       "lollipop", "pie", "sausage", "cupcake", "watermelon"],
        "num_food": 10,
        "goal": 10,
        "message": "That night he had a stomachache!"
    },
    7: {
        "name": "Sunday",
        "story_text": "On Sunday, he ate through one nice green leaf.",
        "food_types": ["leaf"],
        "num_food": 1,
        "goal": 1,
        "message": "And he felt much better!"
    }
}


class Caterpillar:
    """Represents the player's caterpillar."""

    def __init__(self, x, y, speed, window_width, window_height, size=CATERPILLAR_SIZE):
        """Initialize the caterpillar at the given position."""
        self.x = x
        self.y = y
        self.speed = speed
        self.window_width = window_width
        self.window_height = window_height
        self.size = size
        self.image = self.load_image()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def load_image(self):
        """Load and scale the caterpillar image."""
        try:
            image = pygame.image.load("images/caterpillar/caterpillar1.png")
            image = pygame.transform.scale(image, self.size)
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

def spawn_food(num_items, window_width, window_height, food_types):
    """Spawn food items at random positions. Can handle multiple food types."""
    food_items = []

    # If we have multiple food types (like Saturday), spawn one of each
    if isinstance(food_types, list) and len(food_types) > 1:
        for food_type in food_types:
            x = random.randint(0, window_width - FOOD_SIZE[0])
            y = random.randint(0, window_height - FOOD_SIZE[1])
            food_items.append(Food(x, y, food_type))
    else:
        # Single food type, spawn the specified number
        # Extract the food type string from the list
        food_type = food_types[0] if isinstance(food_types, list) else food_types
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


def get_caterpillar_size(level_num):
    """Return the caterpillar size for a given level."""
    # Progressive growth from Monday (level 1) to Sunday (level 7)
    # Start: 64x64, End: 110x110 (big and fat!)
    base_size = 64
    growth_per_level = 8  # Grows 8 pixels per level
    size = base_size + (level_num - 1) * growth_per_level
    return (size, size)
