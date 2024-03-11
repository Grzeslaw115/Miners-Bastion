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

background = pygame.image.load("graphics/menu/background.png").convert()
text_title = title_font.render("Miners' Bastion", True, 'purple')

background_y = 800
last_change = 0

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))
    screen.blit(text_title, (1024 / 2 - text_title.get_width() / 2, background_y))

    if last_change == 0:
        background_y -= 15
        last_change = 1
        pygame.time.wait(500)
    else:
        background_y += 15
        last_change = 0
        pygame.time.wait(500)

    pygame.display.update()
    clock.tick(60)