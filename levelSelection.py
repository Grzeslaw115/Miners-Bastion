import pygame
import sys
from levels import level1, level2, level3


def main(callback):
    # Initialize the game
    pygame.init()
    clock = pygame.time.Clock()

    # Images and sounds
    level1img = pygame.image.load("graphics/levelSelection/level1.png").convert_alpha()
    level2img = pygame.image.load("graphics/levelSelection/level2.png").convert_alpha()
    level3img = pygame.image.load("graphics/levelSelection/level3.png").convert_alpha()
    button_click_sound = pygame.mixer.Sound("audio/menu/button_click.mp3")

    # Set the screen size
    screen = pygame.display.set_mode((1024, 1024))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 64 <= event.pos[0] <= 64 + level1img.get_width() and 1024 / 2 - level1img.get_height() / 2 <= event.pos[1] <= 1024 / 2 + level1img.get_height() / 2:
                    button_click_sound.play()
                    level1.main()

                elif 128 + level1img.get_width() <= event.pos[0] <= 128 + 2 * level1img.get_width() and 1024 / 2 - level2img.get_height() / 2 <= event.pos[1] <= 1024 / 2 + level2img.get_height() / 2:
                    button_click_sound.play()
                    level2.main()

                elif 192 + 2 * level2img.get_width() <= event.pos[0] <= 192 + 3 * level2img.get_width() and 1024 / 2 - level2img.get_height() / 2 <= event.pos[1] <= 1024 / 2 + level2img.get_height() / 2:
                    button_click_sound.play()
                    level3.main()

        screen.blit(level1img, (64, 1024 / 2 - level1img.get_height() / 2))
        screen.blit(level2img, (128 + level1img.get_width(), 1024 / 2 - level2img.get_height() / 2))
        screen.blit(level3img, (192 + 2 * level2img.get_width(), 1024 / 2 - level1img.get_height() / 2))

        clock.tick(60)
        pygame.display.update()