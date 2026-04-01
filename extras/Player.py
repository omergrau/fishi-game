import pygame

from extras import resources


class player(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT, crunch, left_image=0, right_image=0):
        super().__init__()
        self.picturs = [("../assets/images/my fish left.png", "../assets/images/my fish right.png")]
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.score = 0
        self.speed = 0.55
        self.level = -1
        self.slowdownspeed = 0.9
        self.accelartionx = 0
        self.accelartiony = 0
        self.size = 50
        self.dellay = pygame.time.get_ticks()
        self.lastmove = pygame.time.get_ticks()
        self.level_up()
        self.image = self.images[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.eating_music = pygame.mixer.Sound(crunch)
        self.shield = None
        self.shield_cooldown_ms = 2000
        self.shield_cooldown_start = None

    def cooldown_image(self):
        if self.shield_cooldown_start is not None:
            tint_color = (120, 120, 120, 0)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            colored_image = self.image.copy()
            tint_surface = pygame.Surface(colored_image.get_size(), pygame.SRCALPHA)
            tint_surface.fill(tint_color)
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            self.image.set_colorkey((255, 255, 255))
            colored_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            self.image = colored_image


    def update(self, dt):  # dt in seconds
        slowdown = self.slowdownspeed * dt * 20
        idle_time = (pygame.time.get_ticks() - self.lastmove) / 1000
        if self.shield_cooldown_start is not None and pygame.time.get_ticks() - self.shield_cooldown_start > self.shield_cooldown_ms:
            self.shield_cooldown_start = None
            self.shield = None
        if self.accelartiony > 0:
            self.accelartiony -= slowdown
            if self.accelartiony < 0:
                self.accelartiony = 0
        if self.accelartiony < 0:
            self.accelartiony += slowdown
            if self.accelartiony > 0:
                self.accelartiony = 0

        if self.accelartionx > 0:
            self.accelartionx -= slowdown
            if self.accelartionx < 0:
                self.accelartionx = 0
        if self.accelartionx < 0:
            self.accelartionx += slowdown
            if self.accelartionx > 0:
                self.accelartionx = 0

        if abs(self.accelartionx) < 1 and idle_time > 0.1:
            self.accelartionx = 0
        if abs(self.accelartiony) < 1 and idle_time > 0.1:
            self.accelartiony = 0

        self.x += self.accelartionx * dt * 60
        self.y += self.accelartiony * dt * 60

        self.rect.topleft = (int(self.x + self.accelartionx * dt * 60),
                             int(self.y + self.accelartiony * dt * 60))
        self.mask = pygame.mask.from_surface(self.image)
        self.check_borders()
        if self.shield:
            self.shield.update(self.rect.x, self.rect.y,self.size)
        if self.shield_cooldown_start is not None and not self.shield:
            self.cooldown_image()



    def eating(self, size):  # Feeding the fish - increase the player size and score
        self.score += 1
        self.size += size // 20
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_colorkey((255, 255, 255))
        self.mask = pygame.mask.from_surface(self.image)
        self.eating_music.play()
        pygame.mixer.music.set_volume(0.5)

    def level_up(self):  # level up the player - increase the player size and score)(not in use)
        self.level += 1
        self.score = 0
        if len(self.picturs) == self.level:
            self.level -= 1
        image_right = pygame.image.load(resources.load_resource(self.picturs[self.level][1])).convert_alpha()
        self.rect = image_right.get_rect()
        image_right = pygame.transform.scale(image_right, (self.size, self.size))
        self.mask = pygame.mask.from_surface(image_right)
        image_left = pygame.image.load(resources.load_resource(self.picturs[self.level][0])).convert_alpha()
        self.rect = image_left.get_rect()
        image_left = pygame.transform.scale(image_left, (self.size, self.size))
        self.mask = pygame.mask.from_surface(image_left)
        self.images = (image_left, image_right)
        self.image = self.images[1]

    def move(self, keys, dt):
        accel_step = self.speed * dt * 60

        if keys[pygame.K_LEFT]:
            self.lastmove = pygame.time.get_ticks()
            if abs(self.accelartionx) < 5:
                self.accelartionx -= accel_step
            self.image = pygame.transform.scale(self.images[0], (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)

        if keys[pygame.K_RIGHT]:
            self.lastmove = pygame.time.get_ticks()
            if abs(self.accelartionx) < 5:
                self.accelartionx += accel_step
            self.image = pygame.transform.scale(self.images[1], (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)

        if keys[pygame.K_UP]:
            self.lastmove = pygame.time.get_ticks()
            if abs(self.accelartiony) < 5:
                self.accelartiony -= accel_step

        if keys[pygame.K_DOWN]:
            self.lastmove = pygame.time.get_ticks()
            if abs(self.accelartiony) < 5:
                self.accelartiony += accel_step

    def check_borders(
            self):  # check if the player is out of the game borders and set the player location to the other side of the screen
        if self.x < 0:
            self.x = 982
        if self.x > 982:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.y > 736:
            self.y = 736
