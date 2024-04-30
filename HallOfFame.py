import pygame
import json
from button import Button
from settingsLoader import load_settings

pygame.init()
pygame.mixer.init()

# Load settings
settings = load_settings()
SCREEN_WIDTH = settings['SCREEN_WIDTH']
SCREEN_HEIGHT = settings['SCREEN_HEIGHT']
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hall of Fame")

# Load fonts
font = pygame.font.Font(None, 36)

button_click_sound = pygame.mixer.Sound("assets/audio/menu/button_click.mp3")

back_to_menu_img = pygame.image.load("graphics/menu/backToMenuButton.png").convert_alpha()

def main(callback):
    screen = pygame.display.set_mode((1024, 1024))

    #Play hall of fame music
    if settings['SOUND_EFFECTS']:
        pygame.mixer.Sound("assets/audio/hallOfFame/hall_of_fame.mp3").play()

    # Load and parse scores
    try:
        with open("scoreHistory.json", "r") as infile:
            scores = json.load(infile)
    except FileNotFoundError:
        scores = {}

    # Sort scores by points
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Render scores
    y = 100
    for i, (player, score) in enumerate(sorted_scores):
        text = font.render(f"{i+1}. {player}: {score}", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH / 4, y))
        y += 40

    # Button to return to main menu
    back_button = Button(10, 10, back_to_menu_img, action=lambda: pygame.quit())
    back_button.draw(screen)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.rect.collidepoint(event.pos):
                        button_click_sound.play()
                        callback()
                        return

        pygame.display.update()
