from extras import Player, Fish,resources
import os
import sys
from extras.resources import *
import asyncio
import pygame
from extras import Player, Fish
from extras.constants import *
from extras.resources import *


def level_up(player):
    if player.score == 50:
        player.level_up()


def toggle_fullscreen(fullscreen,WIDTH,HEIGHT):
    if fullscreen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), )
    return screen


"""def pause(pause,pause_pressed):
        if pause_pressed not pause:# pause pressed on the first time
            return True
        elif not pause_pressed:# continue the game
            pause=False
            pause_pressed = True
        if not keys[pygame.K_p]:
            pause_pressed=False"""


def load_high_score():
    highscore=resources.load_resource("highscore.txt")
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


async def play_game(running=True,fullscreen=False):
    pause=False
    pause_pressed=False
    entry_load = resources.entry_load()
    ocean_image=entry_load[0]
    lose_video_game=entry_load[1]
    main_game_music=entry_load[2]
    crunch=entry_load[3]
    pygame.mixer.music.load(main_game_music)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    screen = toggle_fullscreen(fullscreen,WIDTH, HEIGHT,)
    screen.blit(pygame.image.load(ocean_image).convert(), (0, 0))
    pygame.display.set_caption("fish eat fish")
    clock = pygame.time.Clock()
    fishlist = pygame.sprite.Group()
    for _ in range(10):
        fishlist.add(Fish.fish(WIDTH, HEIGHT))
    player1 = Player.player(WIDTH, HEIGHT,crunch)
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    await game_over(player1.score, screen, ocean_image, lose_video_game, fullscreen)
                if event.key == pygame.K_p and not pause_pressed:
                    pause= not pause
                    pause_pressed=True
                if not event.key == pygame.K_p:
                    pause_pressed = False
                if event.key == pygame.K_f:
                    fullscreen=not fullscreen
                    screen = toggle_fullscreen(fullscreen,WIDTH, HEIGHT,)
            else:
                pause_pressed = False
        if not pause:
            keys = pygame.key.get_pressed()
            player1.move(keys)
            player1.update()
            level_up(player1)
            for fish_i in fishlist:
                if player1.level != fish_i.level:
                    fish_i.level=player1.level
                if fish_i.isdisappear():
                    fishlist.remove(fish_i)
                    fishlist.add(Fish.fish(WIDTH, HEIGHT))
                else:
                    fish_i.update()
                if pygame.sprite.collide_mask(player1, fish_i):
                    if player1.size > fish_i.size:
                        player1.eating(fish_i.size)
                        fishlist.remove(fish_i)
                        fishlist.add(Fish.fish(WIDTH, HEIGHT))
                    else:
                        running = False
                        await game_over(player1.score,screen,ocean_image,lose_video_game,fullscreen)

        screen.blit(pygame.image.load(resources.entry_load()[0]).convert(), (0, 0))
        players = pygame.sprite.Group()
        players.add(player1)
        players.draw(screen)
        clock.tick(FPS)
        fishlist.draw(screen)

        score_text = font.render(f"score: {player1.score}", True, text_color)
        score_rect = score_text.get_rect()
        score_rect.topleft = ((WIDTH - score_rect.width) // 2, 10)
        screen.blit(score_text, score_rect)
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


async def game_over(score, screen,ocean_image,lose_video_game,fullscreen):
    if score > load_high_score():
        save_high_score(score)
    high_score = load_high_score()
    WIDTH = 982
    HEIGHT = 736
    FPS = 60
    toggle_fullscreen(fullscreen,WIDTH, HEIGHT)
    screen.blit(pygame.image.load(ocean_image).convert(), (0, 0))
    pygame.display.set_caption("fish eat fish")
    running = True
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    clock = pygame.time.Clock()
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
                    await(play_game(True,fullscreen))

        text = font.render(f"Press SPACE on the keyboard to start the game or esc to Quit", True, text_color)
        text_rect = text.get_rect(center=((WIDTH // 2), HEIGHT // 2))
        screen.blit(text, text_rect)
        text = font.render(f"your best score is {high_score}", True, text_color)
        score_rect = text.get_rect(center=((WIDTH // 2), 50))
        screen.blit(text, score_rect)
        text = font.render(f"press f for full screen or p to pause the game", True, text_color)
        score_rect = text.get_rect(center=((WIDTH // 2),(HEIGHT // 2)+80))
        screen.blit(text, score_rect)
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(FPS)


pygame.init()
pygame.mixer.init()
pygame.font.init()

if __name__ == "__main__":
    game = asyncio.run(play_game(True))