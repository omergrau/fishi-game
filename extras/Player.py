import pygame
from extras import resources


class player(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT,crunch,left_image=0,right_image=0):
        super().__init__()
        self.picturs = [("../assets/images/my fish left.png","../assets/images/my fish right.png")]
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.score = 0
        self.speed = 0.3
        self.level = -1
        self.slowdownspeed = 0.5
        self.accelartionx = 0
        self.accelartiony = 0
        self.size = 50
        self.dellay = pygame.time.get_ticks()
        self.lastmove = pygame.time.get_ticks()
        self.level_up()
        self.image = self.images[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.eating_music = pygame.mixer.Sound(crunch)



    def update(self):# update the player location and check for collision with the game borders 
        if pygame.time.get_ticks() - self.dellay > 5:
            if self.accelartiony > 0:
                self.accelartiony -= self.slowdownspeed
            if self.accelartiony < 0:
                self.accelartiony += self.slowdownspeed
            if self.accelartionx > 0:
                self.accelartionx -= self.slowdownspeed
            if self.accelartionx < 0:
                self.accelartionx += self.slowdownspeed
            self.dellay = pygame.time.get_ticks()
        if abs(self.accelartionx) < 1 and  pygame.time.get_ticks() - self.lastmove > 100:
            self.accelartionx = 0
        if abs(self.accelartiony) < 1 and  pygame.time.get_ticks() - self.lastmove > 100:
            self.accelartiony = 0
        self.x += self.accelartionx
        self.y += self.accelartiony
        self.rect.topleft = (self.x + self.accelartionx, self.y + self.accelartiony)
        self.mask = pygame.mask.from_surface(self.image)
        self.check_borders()

    def eating(self,size):# Feeding the fish - increase the player size and score
        self.score += 1
        self.size += size // 20
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey((255, 255, 255))
        self.mask = pygame.mask.from_surface(self.image)
        self.eating_music.play()
        pygame.mixer.music.set_volume(0.5)

    def level_up(self):# level up the player - increase the player size and score)(not in use)
        self.level += 1
        self.score=0
        if len(self.picturs) == self.level:
            self.level-=1
        image_right = pygame.image.load(resources.load_resource(self.picturs[self.level][1])).convert_alpha()
        self.rect = image_right.get_rect()
        image_right = pygame.transform.scale(image_right, (self.size, self.size))
        self.mask = pygame.mask.from_surface(image_right)
        image_left = pygame.image.load(resources.load_resource(self.picturs[self.level][0])).convert_alpha()
        self.rect = image_left.get_rect()
        image_left = pygame.transform.scale(image_left, (self.size, self.size))
        self.mask = pygame.mask.from_surface(image_left)
        self.images = (image_left, image_right)
        self.image= self.images[1]

    def move(self, keys):# move the player based on the keys pressed
        if keys[pygame.K_LEFT]:
            self.lastmove = pygame.time.get_ticks()
            if abs(self.accelartionx) < 5:

                if pygame.time.get_ticks() - self.dellay > 15:
                    self.dellay = pygame.time.get_ticks()
                    self.accelartionx -= self.speed
            self.x += self.speed
            self.image = pygame.transform.scale(self.images[0], (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)
        if keys[pygame.K_RIGHT]:
            self.lastmove = pygame.time.get_ticks()
            self.image = self.images[1]
            if abs(self.accelartionx) < 5:
                if pygame.time.get_ticks() - self.dellay > 15:
                    self.dellay = pygame.time.get_ticks()
                    self.accelartionx += self.speed
            self.x += self.speed
            self.image = pygame.transform.scale(self.images[1], (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)
        if keys[pygame.K_UP]:
            self.lastmove = pygame.time.get_ticks()
            if abs(self.accelartiony) < 5:
                if pygame.time.get_ticks() - self.dellay > 15:
                    self.dellay = pygame.time.get_ticks()
                    self.accelartiony -= self.speed
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.lastmove = pygame.time.get_ticks()
            if abs(self.accelartiony) < 5:
                if pygame.time.get_ticks() - self.dellay > 15:
                    self.dellay = pygame.time.get_ticks()
                    self.accelartiony += self.speed
            self.y += self.speed

    def check_borders(self):# check if the player is out of the game borders and set the player location to the other side of the screen
        if self.x < 0:
            self.x = 982
        if self.x > 982:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.y > 736:
            self.y = 736



