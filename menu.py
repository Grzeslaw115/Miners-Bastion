import pygame
from sys import exit
import levelSelection
from settings import *
import settingsPanel

# Initialize the game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Miners' Bastion")
title_font = pygame.font.Font("fonts/heav.ttf", 128)
clock = pygame.time.Clock()

# Music and sounds
pygame.mixer.music.load("audio/menu/menu.mp3")
button_click_sound = pygame.mixer.Sound("audio/menu/button_click.mp3")
pygame.mixer.music.play(-1)
music_on = True

# Texts and images
background = pygame.image.load("graphics/menu/background.png").convert_alpha()
start = pygame.image.load("graphics/menu/start.png").convert_alpha()
start = pygame.transform.scale(start, (start.get_width() * 1/5, start.get_height() * 1/5))
settings = pygame.image.load("graphics/menu/settings.png").convert_alpha()
settings = pygame.transform.scale(settings, (settings.get_width() * 1/5, settings.get_height() * 1/5))
exit_button = pygame.image.load("graphics/menu/exit.png").convert_alpha()
exit_button = pygame.transform.scale(exit_button, (exit_button.get_width() * 1/6, exit_button.get_height() * 1/6))

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
                # Muzyka, docelowo tu beda ustawienia
                if 1024 - settings.get_width() - 10 <= event.pos[0] <= 1024 - 10 and 10 <= event.pos[1] <= 10 + settings.get_height():
                    button_click_sound.play()
                    pygame.mixer.music.stop()
                    settingsPanel.main()
                    exit()

                # Wyjscie z gry
                elif 1024 / 2 - exit_button.get_width() / 2 <= event.pos[0] <= 1024 / 2 + exit_button.get_width() / 2 and 450 <= event.pos[1] <= 450 + exit_button.get_height():
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit()

                # Rozpoczecie gry
                elif 1024 / 2 - start.get_width() / 2 <= event.pos[0] <= 1024 / 2 + start.get_width() / 2 and 300 <= event.pos[1] <= 300 + start.get_height():
                    button_click_sound.play()
                    levelSelection.main()
                    pygame.mixer.music.stop()
                    pygame.quit()
                    exit()

    screen.blit(background, (0, 0))
    screen.blit(start, (1024 / 2 - start.get_width() / 2, 300))
    screen.blit(text_title, (1024 / 2 - text_title.get_width() / 2, background_y))
    screen.blit(settings, (1024 - settings.get_width() - 10, 10))
    screen.blit(exit_button, (1024 / 2 - exit_button.get_width() / 2, 450))

    # Animacja tytułu
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