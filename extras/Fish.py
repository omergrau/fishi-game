import pygame
import random
from extras import resources
class fish(pygame.sprite.Sprite):#enemy fish class
    def __init__(self, WIDTH, HEIGHT):
        super().__init__()
        Rrandomcolor = random.randint(0, 255)
        Grandomcolor = random.randint(0, 255)
        tint_color = (Rrandomcolor, Grandomcolor, 0, 255)
        self.picturs = [("../assets/images/my fish left.png", "../assets/images/my fish right.png")]
        self.size = random.random() * 200
        self.x = random.choice((-199,WIDTH))
        self.y = random.randint(0, HEIGHT-50)
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.level=0
        self.speed = random.randint(1, 6)
        if self.x ==-199:
            self.direction = 1
        else:
            self.direction = -1

        if self.direction == 1:
            self.image = pygame.image.load(resources.load_resource(self.picturs[self.level][1])).convert_alpha()
        else:
            self.image = pygame.image.load(resources.load_resource(self.picturs[self.level][0])).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        colored_image = self.image.copy()
        tint_surface = pygame.Surface(colored_image.get_size(), pygame.SRCALPHA)
        tint_surface.fill(tint_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.image.set_colorkey((255, 255, 255))
        colored_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.image = colored_image

    def check_borders(self):#check if the fish is out of the screen and reset its position
        if self.x < 0:
            self.x = 982
        if self.x > 982:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.y > 736:
            self.y = 736

    def update(self):# update the fish location and check for collision with the game borders
        self.x += self.speed * self.direction
        self.rect.topleft = (self.x, self.y)

    def isdisappear(self):## check if the fish is out of the screen
        if self.x < -200 or self.x > self.WIDTH:
            return True
    def level_up(self,level):## level up the fish - increase the fish size and score)(not in use)
        self.level += 1

