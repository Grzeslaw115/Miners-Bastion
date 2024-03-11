import pygame
from sys import exit

# Initialize the game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1024, 1024))
pygame.display.set_caption("Miners' Bastion")
title_font = pygame.font.Font("fonts/heav.ttf", 128)
clock = pygame.time.Clock()

# Load media
pygame.mixer.music.load("audio/menu.mp3")
pygame.mixer.music.play(-1)
music_on = True

background = pygame.image.load("graphics/menu/background.png").convert()
music = pygame.image.load("graphics/menu/music_on.png").convert_alpha()
text_title = title_font.render("Miners' Bastion", True, 'yellow')

background_y = 800
moving_up = True

# Main loop
while True:

    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 1024 - music.get_width() - 10 <= event.pos[0] <= 1024 - 10 and 10 <= event.pos[1] <= 10 + music.get_height():
                    if music_on:
                        music = pygame.image.load("graphics/menu/music_off.png").convert_alpha()
                        pygame.mixer.music.stop()
                        music_on = False
                    else:
                        music = pygame.image.load("graphics/menu/music_on.png").convert_alpha()
                        pygame.mixer.music.play(-1)
                        music_on = True

    screen.blit(background, (0, 0))
    screen.blit(text_title, (1024 / 2 - text_title.get_width() / 2, background_y))
    screen.blit(music, (1024 - music.get_width() - 10, 10))

    if moving_up:
        background_y -= 60 * dt
        if background_y <= 800:
            moving_up = False
    else:
        background_y += 60 * dt
        if background_y >= 850:
            moving_up = True

    pygame.display.update()
    clock.tick(60)