import pygame
import asyncio
from pygame import MOUSEMOTION
#from pygame.examples.sprite_texture import clock

from extras import Player, Fish,resources
import os
import sys
from resources import entry_load
from constants import*


class game():
    def __init__(self):
        self.pause = False
        self.fullscreen=False
        self.pause_pressed = False
        self.entry_resources = entry_load()#load the game resources // (ocean_image,lose_video_,gamemain_game_music
        lose_video_game = self.entry_resources[1]
        self.high_score = 0
        self.game_mode = "game"
        pygame.mixer.music.load(self.entry_resources[2])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),)
        self.screen.blit(pygame.image.load(self.entry_resources[0]).convert(), (0, 0))
        pygame.display.set_caption("fish eat fish")
        self.clock = pygame.time.Clock()
        self.fishlist = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.player1 = Player.player(WIDTH, HEIGHT,self.entry_resources[3])
        self.players.add(self.player1)
        for _ in range(10):
            self.fishlist.add(Fish.fish(WIDTH, HEIGHT))

        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)


    def toggle_fullscreen(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))


    def update_player(self):
            keys = pygame.key.get_pressed()
            self.player1.move(keys)
            self.player1.update()
            """self.level_up(player1)"""


    def update_enemies(self):
        for fish_i in self.fishlist:
            if fish_i.isdisappear():
                self.fishlist.remove(fish_i)
                self.fishlist.add(Fish.fish(WIDTH, HEIGHT))
            else:
                fish_i.update()
            if pygame.sprite.collide_mask(self.player1, fish_i):
                if self.player1.size > fish_i.size:
                    self.player1.eating(fish_i.size)
                    self.fishlist.remove(fish_i)
                    self.fishlist.add(Fish.fish(WIDTH, HEIGHT))
                else:
                    self.game_mode = "game over"


    def draw(self):
        self.fishlist.draw(self.screen)
        self.players.draw(self.screen)


    def update_keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_mode="quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    self.game_mode="quit"
                if event.key == pygame.K_p and not pause_pressed:
                    pause = not pause
                    pause_pressed = True
                if not event.key == pygame.K_p:
                    pause_pressed = False
                if event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    self.toggle_fullscreen()
                if self.game_mode == "game over":
                    if event.key == pygame.K_SPACE:
                        self.game_mode = "game"
            else:
                pause_pressed = False


    def update_game(self):
        self.screen.blit(pygame.image.load(self.entry_resources[0]).convert(), (0, 0))
        if self.game_mode == "quit":
            self.running = False
        if self.game_mode == "game over":
            text = self.font.render(f"Press SPACE on the keyboard to start the game or esc to Quit", True, self.text_color)
            text_rect = text.get_rect(center=((WIDTH // 2), HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text = self.font.render(f"your best score is {self.high_score}", True, self.text_color)
            score_rect = text.get_rect(center=((WIDTH // 2), 50))
            self.screen.blit(text, score_rect)
            text = self.font.render(f"press f for full screen or p to pause the game", True, self.text_color)
            score_rect = text.get_rect(center=((WIDTH // 2), (HEIGHT // 2) + 80))
            self.screen.blit(text, score_rect)


    def update(self):

        self.update_player()
        self.update_enemies()
        self.update_keyboard_input()


    async def game(self):
        self.running = True
        while self.running:
            self.update_game()
            if self.game_mode=="game":
                self.update()
                self.draw()
            if self.game_mode == "game over":
                self.game_over()

            self.clock.tick(FPS)
            pygame.display.flip()
            await asyncio.sleep(0)
            print(self.game_mode)
        print("exit game")
        pygame.quit()


    def game_over(self):
        pass


    def load_game_resources(self):
        self.load_images()
        self.load_sounds()


    def load_images(self):
        pass


    def load_sounds(self):
        pass



if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    game1 = game()
    game = asyncio.run(game1.game())