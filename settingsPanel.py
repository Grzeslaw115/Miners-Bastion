import pygame
import sys
import menu
from settings import *

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Settings panel")

# Inicjalizacja dźwięku
pygame.mixer.init()
pygame.mixer.music.load("audio/menu/menu.mp3")
pygame.mixer.music.set_volume(VOLUME / 100)
pygame.mixer.music.play(-1)
button_click_sound = pygame.mixer.Sound("audio/menu/button_click.mp3")

class SaveButton():
    def __init__(self, screen):
        self.screen = screen
        self.color = WHITE
        self.hover_color = GRAY
        self.font = pygame.font.Font("fonts/heav.ttf", 48)
        self.text = self.font.render('Zapisz ustawienia', True, BLACK)
        self.rect = self.text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100))

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.hover_color, self.rect.inflate(10, 10), 0, 5)
        else:
            pygame.draw.rect(self.screen, self.color, self.rect.inflate(10, 10), 0, 5)
        self.screen.blit(self.text, self.rect)

    def save_settings(self, volume):
        with open("settings.py", "r") as file:
            settings = file.readlines()

        with open("settings.py", "w") as file:
            for line in settings:
                if "VOLUME" in line:
                    file.write(f"VOLUME = {volume}\n")
                else:
                    file.write(line)

        exec(open("menu.py").read())

class VolumeSlider():
    def __init__(self, screen, current_volume):
        self.screen = screen
        self.start = 100
        self.end = SCREEN_WIDTH - 100
        self.current_value = current_volume
        self.background_color = GRAY
        self.slider_color = WHITE
        self.font = pygame.font.SysFont("Arial", 30)
        self.dragging = False

        self.slider_pos = self.start + (self.current_value / 100) * (self.end - self.start)
        self.slider_rect = pygame.Rect(self.slider_pos, SCREEN_HEIGHT / 2, 20, 20)

    def draw(self):
        pygame.draw.line(self.screen, self.background_color, (self.start, SCREEN_HEIGHT / 2 + 10), (self.end, SCREEN_HEIGHT / 2 + 10), 5)
        pygame.draw.rect(self.screen, self.slider_color, self.slider_rect)

        text_surf = self.font.render(str(self.current_value), True, WHITE)
        text_pos = (self.slider_rect.centerx - text_surf.get_width() / 2, self.slider_rect.top - 30)
        self.screen.blit(text_surf, text_pos)

        name_surf = self.font.render("Glosnosc", True, WHITE)
        name_pos = (self.start + (self.end - self.start) / 2 - name_surf.get_width() / 2, self.slider_rect.top - 60)
        self.screen.blit(name_surf, name_pos)

        if self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            self.slider_pos = mouse_x
            if self.slider_pos < self.start:
                self.slider_pos = self.start
            if self.slider_pos > self.end:
                self.slider_pos = self.end
            self.slider_rect = pygame.Rect(self.slider_pos, SCREEN_HEIGHT / 2, 20, 20)
            current_volume = int((self.slider_pos - self.start) / (self.end - self.start) * 100)
            self.current_value = current_volume
            pygame.mixer.music.set_volume(current_volume / 100)


current_volume = VOLUME
save_button = SaveButton(screen)
volume_slider = VolumeSlider(screen, current_volume)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if save_button.rect.collidepoint(event.pos):
                    button_click_sound.play()
                    save_button.save_settings(current_volume)

                if volume_slider.slider_rect.collidepoint(event.pos):
                    volume_slider.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                volume_slider.dragging = False

                
    screen.fill(BLACK)

    save_button.draw()
    volume_slider.draw()
    pygame.display.flip()