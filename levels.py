import pygame
import random
from globals import *

class Map_Level:
    def __init__(self, width, height, house_count):
        super().__init__()
        self.width = width
        self.height = height
        self.houses = pygame.sprite.Group()
        self.preloaded_houses = []  # Store preloaded houses
        self.generate_random_houses(house_count)

    def generate_random_houses(self, num_houses):
        attempts = 0
        while len(self.houses) < num_houses and attempts < 1000:
            width = random.randint(150, 300)
            height = random.randint(150, 300)
            x = random.randint(0, self.width - width)
            y = random.randint(0, self.height - height)
            entrance_side = random.choice(['top', 'bottom', 'left', 'right'])

            new_house = House(x, y, width, height, entrance_side)
            if (not self.check_overlap(new_house) and 
                self.check_distance(new_house)):
                self.houses.add(new_house)
                self.preloaded_houses.append(new_house)
            attempts += 1
        self.houses = pygame.sprite.Group(self.preloaded_houses)

    def check_overlap(self, new_house):
        for house in self.preloaded_houses:
            if new_house.rect.colliderect(house.rect):
                return True
        return False

    def check_distance(self, new_house):
        min_distance = 50  # Minimum distance between houses
        for house in self.preloaded_houses:
            if new_house.rect.colliderect(house.rect.inflate(min_distance * 2, min_distance * 2)):
                return False
        return True

    def draw_map(self, display, camera_offset):
        for house in self.houses:
            house.draw_house(display, camera_offset)

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, entrance_side):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.entrance_side = entrance_side
        self.entrance_rect = self.get_entrance()
        self.walls = self.get_walls()

    def get_entrance(self):
        if self.entrance_side == 'top':
            return pygame.Rect(self.rect.x + self.rect.width // 4, self.rect.y,
                               self.rect.width // 2, 10)
        elif self.entrance_side == 'bottom':
            return pygame.Rect(self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height - 10,
                               self.rect.width // 2, 10)
        elif self.entrance_side == 'right':
            return pygame.Rect(self.rect.x, self.rect.y + self.rect.height // 4,
                               10, self.rect.height // 2)
        elif self.entrance_side == 'left':
            return pygame.Rect(self.rect.x + self.rect.width - 10, self.rect.y + self.rect.height // 4,
                               10, self.rect.height // 2)

    def get_walls(self):
        walls = []
        walls.append(pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 10))  # Top wall
        walls.append(pygame.Rect(self.rect.x, self.rect.y, 10, self.rect.height))  # Left wall
        walls.append(pygame.Rect(self.rect.x + self.rect.width - 10, self.rect.y, 10, self.rect.height))  # Right wall
        walls.append(pygame.Rect(self.rect.x, self.rect.y + self.rect.height - 10, self.rect.width, 10))  # Bottom wall
        return walls

    def draw_house(self, display, camera_offset):
        pygame.draw.rect(display, GREEN, self.rect.move(camera_offset), width=10)
        pygame.draw.rect(display, BLACK, self.entrance_rect.move(camera_offset))