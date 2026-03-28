import asyncio

import pygame

from extras import Player, Fish, resources
from extras.constants import *
from extras.resources import *


class game():
    def __init__(self):
        self.pause = False
        self.fullscreen = False
        self.pause_pressed = False
        self.images = {}
        self.sounds = {}
        self.load_game_resources()
        self.high_score = 0
        self.score = 0
        self.game_mode = "game"
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), )
        self.clock = pygame.time.Clock()
        self.fishlist = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)
        self.player1=None

    def load_game_resources(self):
        self.load_images()
        self.load_sounds()

    def load_images(self):
        self.images["my fish left"] = load_resource("../assets/images/my fish left.png")
        self.images["my fish right"] = load_resource("../assets/images/my fish right.png")
        self.images["ocean"] = load_resource("../assets/images/ocean.png")

    def load_sounds(self):
        self.sounds["game music"] = load_resource("../assets/music/game-music-loop.wav")
        self.sounds["lose"] = load_resource("../assets/music/lose_video-game.wav")
        self.sounds["eat"] = load_resource("../assets/music/plastic-crunch.wav")

    def setup(self):
        pygame.mixer.music.load(self.sounds["game music"])
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        pygame.display.set_caption("fish eat fish")
        self.player1 = Player.player(WIDTH, HEIGHT, self.sounds["eat"], self.images["my fish left"],self.images["my fish right"])
        self.players.add(self.player1)
        for _ in range(10):
            self.fishlist.add(Fish.fish(WIDTH, HEIGHT))


    def update_player(self):
        keys = pygame.key.get_pressed()
        self.player1.move(keys)
        self.player1.update()

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

    async def play_game(self):
        self.setup()
        self.load_game_resources()
        entry_load = resources.entry_load()
        ocean_image = entry_load[0]
        lose_video_game = entry_load[1]
        self.toggle_fullscreen()
        self.screen.blit(pygame.image.load(ocean_image).convert(), (0, 0))
        self.clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)
        running=True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        await self.game_over(self.player1.score, self.screen, ocean_image, lose_video_game, fullscreen)
                    if event.key == pygame.K_p and not pause_pressed:
                        pause = not pause
                        pause_pressed = True
                    if not event.key == pygame.K_p:
                        pause_pressed = False
                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        self.toggle_fullscreen()
                else:
                    pause_pressed = False
            if not self.pause:
                self.update_player()
                self.update_enemies()
            self.screen.blit(pygame.image.load(resources.entry_load()[0]).convert(), (0, 0))
            players = pygame.sprite.Group()
            players.add(self.player1)
            players.draw(self.screen)
            self.clock.tick(FPS)
            self.fishlist.draw(self.screen)
            score_text = font.render(f"score: {self.player1.score}", True, text_color)
            score_rect = score_text.get_rect()
            score_rect.topleft = ((WIDTH - score_rect.width) // 2, 10)
            self.screen.blit(score_text, score_rect)
            if self.game_mode == "game over":
                await self.game_over(self.player1.score, self.screen, ocean_image, lose_video_game, self.fullscreen)
            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), )

    """def pause(pause,pause_pressed):
            if pause_pressed not pause:# pause pressed on the first time
                return True
            elif not pause_pressed:# continue the game
                pause=False
                pause_pressed = True
            if not keys[pygame.K_p]:
                pause_pressed=False"""

    def load_high_score(self):
        highscore = resources.load_resource("highscore.txt")
        if os.path.exists(highscore):
            with open(highscore, "r") as f:
                try:
                    return int(f.readline())
                except ValueError:
                    return 0
        else:
            return 0

    def save_high_score(score):
        with open(resources.load_resource("highscore.txt"), "w") as f:
            f.write(str(score))

    async def game_over(self,ocean_image, lose_video_game):
        if self.score > self.load_high_score():
            self.save_high_score(self.score)
        high_score = self.load_high_score()
        self.toggle_fullscreen()
        self.screen.blit(pygame.image.load(ocean_image).convert(), (0, 0))
        pygame.display.set_caption("fish eat fish")
        running = True
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load(lose_video_game)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        self.game_mode="game"
                        self.fishlist=pygame.sprite.Group()
                        await(self.play_game())

            text = font.render(f"Press SPACE on the keyboard to start the game or esc to Quit", True, text_color)
            text_rect = text.get_rect(center=((WIDTH // 2), HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text = font.render(f"your best score is {high_score}", True, text_color)
            score_rect = text.get_rect(center=((WIDTH // 2), 50))
            self.screen.blit(text, score_rect)
            text = font.render(f"press f for full screen or p to pause the game", True, text_color)
            score_rect = text.get_rect(center=((WIDTH // 2), (HEIGHT // 2) + 80))
            self.screen.blit(text, score_rect)
            pygame.display.flip()
            await asyncio.sleep(0)
            self.clock.tick(FPS)


pygame.init()
pygame.mixer.init()
pygame.font.init()
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    game1 = game()
    game = asyncio.run(game1.play_game())
