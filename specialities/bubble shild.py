import pygame
import random
from extras import resources
class ShieldBubble(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.size = 36
        self.picturs = "../assets/images/specials/shield bubble.png"
        self.image = pygame.image.load(resources.load_resource(self.picturs)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, width - 50)
        self.rect.y = random.randint(50, height - 50)
        self.spawn_time = pygame.time.get_ticks()
        self.duration_ms = 6000