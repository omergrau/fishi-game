import random

import pygame

from extras import resources


class ShieldBubble(pygame.sprite.Sprite):
    def __init__(self, width, height, size):
        super().__init__()
        self.size = size * 80 / 50
        self.picturs = "../assets/images/special/shield bubble.png"
        self.image = pygame.image.load(resources.load_resource(self.picturs)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size + 20, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, width - 50)
        self.rect.y = random.randint(50, height - 50)
        self.spawn_time = pygame.time.get_ticks()
        self.duration_ms = 6000

    def update(self, x, y, size):
        self.size = size * 80 / 50
        self.image = pygame.transform.scale(self.image, (1.25*self.size, self.size))
        self.rect.x = x - 0.3 * self.size
        self.rect.y = y - 0.1 * self.size
