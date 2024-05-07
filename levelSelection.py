import pygame
import sys
from levels import level
from button import Button
from settingsLoader import load_settings


settings = load_settings()

# Screen setup
SCREEN_WIDTH = settings['SCREEN_WIDTH']
SCREEN_HEIGHT = settings['SCREEN_HEIGHT']


def main(callback):
    # Initialize the game
    pygame.init()
    clock = pygame.time.Clock()

    # Images and sounds
    level1img = pygame.image.load("graphics/levelSelection/level1.png").convert_alpha()
    level2img = pygame.image.load("graphics/levelSelection/level2.png").convert_alpha()
    level3img = pygame.image.load("graphics/levelSelection/level3.png").convert_alpha()
    button_click_sound = pygame.mixer.Sound("assets/audio/menu/button_click.mp3")
    back_to_menu_img = pygame.image.load("graphics/menu/backToMenuButton.png").convert_alpha()

    # Set the screen size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    back_button = Button(10, 10, back_to_menu_img)
    level1_button = Button(64, 1024 / 2 - level1img.get_height() / 2, level1img)
    level2_button = Button(128 + level1img.get_width(), 1024 / 2 - level2img.get_height() / 2, level2img)
    level3_button = Button(192 + 2 * level2img.get_width(), 1024 / 2 - level1img.get_height() / 2, level3img)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button.rect.collidepoint(event.pos):
                    settings = load_settings()
                    if settings['SOUND_EFFECTS']:
                        button_click_sound.play()
                    level.load_level("level1", callback)
                elif level2_button.rect.collidepoint(event.pos):
                    settings = load_settings()
                    if settings['SOUND_EFFECTS']:
                        button_click_sound.play()
                    level.load_level("level2", callback)
                elif level3_button.rect.collidepoint(event.pos):
                    settings = load_settings()
                    if settings['SOUND_EFFECTS']:
                        button_click_sound.play()
                    level.load_level("level3", callback)

                elif back_button.rect.collidepoint(event.pos):
                    settings = load_settings()
                    if settings['SOUND_EFFECTS']:
                        button_click_sound.play()
                    callback()
                    return


        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)
        back_button.draw(screen)

        clock.tick(60)
        pygame.display.update()