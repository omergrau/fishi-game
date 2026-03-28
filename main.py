import asyncio

import pygame

from extras import Player, Fish
from extras.Player import player
from extras.constants import *
from extras.resources import *


class game():
    def __init__(self):
        self.running = None
        self.pause = False
        self.fullscreen = False
        self.pause_pressed = False
        self.images = {}
        self.sounds = {}
        self.load_game_resources()
        self.high_score = 0
        self.game_mode = "game"
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), )
        self.clock = pygame.time.Clock()
        self.fishlist = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.lose_sound_playing = False
        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)

    def setup(self):# setup the game screen and load the game music
        pygame.mixer.music.load(self.sounds["game music"])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("fish eat fish")
        player1: player = Player.player(WIDTH, HEIGHT, self.sounds["eat"], self.images["my fish left"],
                                        self.images["my fish right"])
        self.players.add(player1)
        for _ in range(10):
            self.fishlist.add(Fish.fish(WIDTH, HEIGHT))

    def toggle_fullscreen(self):# toggle the fullscreen from regular to fullscreen and vice versa
        if self.fullscreen:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def update_player(self):# update the player location and check for collision with the enemies
        keys = pygame.key.get_pressed()
        player1 = self.players.sprites()[0]
        player1.move(keys)
        player1.update()

    def update_enemies(self):# update the enemies location and check for collision with the player
        for fish_i in self.fishlist:
            if fish_i.isdisappear():
                self.fishlist.remove(fish_i)
                self.fishlist.add(Fish.fish(WIDTH, HEIGHT))
            else:
                fish_i.update()
            player1 = self.players.sprites()[0]
            if pygame.sprite.collide_mask(player1, fish_i):
                if player1.size > fish_i.size:
                    player1.eating(fish_i.size)
                    self.fishlist.remove(fish_i)
                    self.fishlist.add(Fish.fish(WIDTH, HEIGHT))
                else:
                    self.game_mode = "game over"

    def draw(self):# draw the game screen and the player and enemies
        self.fishlist.draw(self.screen)
        self.players.draw(self.screen)
        self.draw_score()

    def pausef(self, event):# pause the game
        if not self.pause_pressed:
            self.pause = not self.pause
            self.pause_pressed = True

    def update_keyboard_input(self):# check for keyboard input and update the game state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_mode = "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    self.game_mode = "quit"
                if event.key == pygame.K_SPACE:
                    if self.game_mode == "game":
                        self.pausef(event)
                    if self.game_mode == "game over":
                        self.game_mode = "restart"
                if event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    self.toggle_fullscreen()
            else:
                self.pause_pressed = False

    def load_high_score(self):# load the high score from the file
        highscore = load_resource("highscore.txt")
        if os.path.exists(highscore):
            with open(highscore, "r") as f:
                try:
                    self.high_score = max(int(f.readline()),self.players.sprites()[0].score)
                except ValueError:
                    self.high_score= 0
        else:
            self.high_score = 0

    def save_high_score(self):# save the high score to the file
        with open(load_resource("highscore.txt"), "w") as f:
            f.write(str(self.high_score))

    def draw_score(self):# draw the score on the screen
        score_text = self.font.render(f"score: {self.players.sprites()[0].score}", True, self.text_color)
        score_rect = score_text.get_rect()
        score_rect.topleft = ((WIDTH - score_rect.width) // 2, 10)
        self.screen.blit(score_text, score_rect)

    def update_game(self):# update the game state and draw the background
        self.screen.blit(pygame.image.load(self.images["ocean"]).convert(), (0, 0))
        if self.game_mode == "quit":
            self.running = False
        if self.game_mode == "game over":
            text = self.font.render(f"Press SPACE on the keyboard to start the game or esc to Quit", True,
                                    self.text_color)
            text_rect = text.get_rect(center=((WIDTH // 2), HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text = self.font.render(f"your best score is {self.high_score}", True, self.text_color)
            score_rect = text.get_rect(center=((WIDTH // 2), 50))
            self.screen.blit(text, score_rect)
            text = self.font.render(f"press f for full screen", True, self.text_color)
            score_rect = text.get_rect(center=((WIDTH // 2), (HEIGHT // 2) + 80))
            self.screen.blit(text, score_rect)

    def update(self):# update the game state and draw the background
        self.update_player()
        self.update_enemies()
        self.update_keyboard_input()
        self.update_game()

    def game_over_sound(self):# play the game over sound
        pygame.mixer.music.load(self.sounds["lose"])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        self.lose_sound_playing = True

    async def game(self):## main game loop
        self.running = True
        self.setup()
        while self.running:
            self.update_keyboard_input()
            if not self.pause:
                if self.game_mode == "game over" or self.game_mode == "restart":
                    await self.game_over()
                self.update_game()
                if self.game_mode == "game":
                    self.update()
                    self.draw()
                if self.game_mode == "game over":
                    self.load_high_score()
                    self.save_high_score()
                if self.game_mode == "quit":
                    break
                self.clock.tick(FPS)
            pygame.display.flip()
            await asyncio.sleep(0)
        pygame.quit()

    async def game_over(self):## game over screen and restart option for the game
        if not self.lose_sound_playing:
            self.game_over_sound()
        if self.game_mode == "restart":
            self.lose_sound_playing = False
            self.game_mode="game"
            self.__init__()
            await self.game()
        await asyncio.sleep(0)

    def load_game_resources(self):## load the game resources
        self.load_images()
        self.load_sounds()

    def load_images(self):## load the game images
        self.images["my fish left"] = load_resource("../assets/images/my fish left.png")
        self.images["my fish right"] = load_resource("../assets/images/my fish right.png")
        self.images["ocean"] = load_resource("../assets/images/ocean.png")

    def load_sounds(self):## load the game sounds
        self.sounds["game music"] = load_resource("../assets/music/game-music-loop.wav")
        self.sounds["lose"] = load_resource("../assets/music/lose_video-game.wav")
        self.sounds["eat"] = load_resource("../assets/music/plastic-crunch.wav")


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    game1 = game()
    game = asyncio.run(game1.game())