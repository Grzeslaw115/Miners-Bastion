import pygame
import sys

def main():
    # Initialize the game
    pygame.init()
    clock = pygame.time.Clock()

    sample_text = pygame.font.Font(None, 128).render("Tu beda jakies levele", True, 'yellow')

    # Set the screen size
    screen = pygame.display.set_mode((1024, 1024))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(sample_text, (1024 / 2 - sample_text.get_width() / 2, 1024 / 2 - sample_text.get_height() / 2))

        clock.tick(60)
        pygame.display.update()