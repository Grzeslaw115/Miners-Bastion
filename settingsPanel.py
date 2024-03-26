import pygame
import sys
from settingsLoader import *
import json

def main(callback):
    # Initialize Pygame
    pygame.init()

    settings = load_settings()
    local_sound_effects = settings['SOUND_EFFECTS']
    current_volume = settings['VOLUME']

    screen = pygame.display.set_mode((settings['SCREEN_WIDTH'], settings['SCREEN_HEIGHT']))
    pygame.display.set_caption("Settings panel")

    # Initialize Pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load("audio/menu/menu.mp3")
    pygame.mixer.music.set_volume(current_volume / 100)
    pygame.mixer.music.play(-1)
    button_click_sound = pygame.mixer.Sound("audio/menu/button_click.mp3")

    class Button():
        def __init__(self, screen, text, height = settings['SCREEN_HEIGHT'] - 100):
            self.screen = screen
            self.color = settings['WHITE']
            self.hover_color = settings['GRAY']
            self.font = pygame.font.Font("fonts/heav.ttf", 48)
            self.text = self.font.render(text, True, settings['BLACK'])
            self.rect = self.text.get_rect(center=(settings['SCREEN_WIDTH'] / 2, height))

        def draw(self):
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.hover_color, self.rect.inflate(10, 10), 0, 5)
            else:
                pygame.draw.rect(self.screen, self.color, self.rect.inflate(10, 10), 0, 5)
            self.screen.blit(self.text, self.rect)

    class VolumeSlider():
        def __init__(self, screen, current_volume):
            self.screen = screen
            self.start = 100
            self.end = settings['SCREEN_WIDTH'] - 100
            self.current_value = current_volume
            self.background_color = settings['GRAY']
            self.slider_color = settings['WHITE']
            self.font = pygame.font.SysFont("Arial", 30)
            self.dragging = False

            self.slider_pos = self.start + (self.current_value / 100) * (self.end - self.start)
            self.slider_rect = pygame.Rect(self.slider_pos, settings['SCREEN_HEIGHT'] / 2, 20, 20)

        def draw(self):
            pygame.draw.line(self.screen, self.background_color, (self.start, settings['SCREEN_HEIGHT'] / 2 + 10), (self.end, settings['SCREEN_HEIGHT'] / 2 + 10), 5)
            pygame.draw.rect(self.screen, self.slider_color, self.slider_rect)

            text_surf = self.font.render(str(self.current_value), True, settings['WHITE'])
            text_pos = (self.slider_rect.centerx - text_surf.get_width() / 2, self.slider_rect.top - 30)
            self.screen.blit(text_surf, text_pos)

            name_surf = self.font.render("Glosnosc", True, settings['WHITE'])
            name_pos = (self.start + (self.end - self.start) / 2 - name_surf.get_width() / 2, self.slider_rect.top - 60)
            self.screen.blit(name_surf, name_pos)

            if self.dragging:
                mouse_x, _ = pygame.mouse.get_pos()
                self.slider_pos = mouse_x
                if self.slider_pos < self.start:
                    self.slider_pos = self.start
                if self.slider_pos > self.end:
                    self.slider_pos = self.end
                self.slider_rect = pygame.Rect(self.slider_pos, settings['SCREEN_HEIGHT'] / 2, 20, 20)
                current_volume = int((self.slider_pos - self.start) / (self.end - self.start) * 100)
                self.current_value = current_volume
                pygame.mixer.music.set_volume(current_volume / 100)

    class SoundEffectsCheckbox():
        def __init__(self, screen):
            self.screen = screen
            self.color = settings['WHITE']
            self.hover_color = settings['GRAY']
            self.font = pygame.font.Font("fonts/heav.ttf", 48)
            self.update_text()
            self.rect = self.text.get_rect(center=(settings['SCREEN_WIDTH'] / 2, settings['SCREEN_HEIGHT'] - 200))

        def update_text(self):
            if local_sound_effects:
                self.text = self.font.render('Wylacz efekty dzwiekowe', True, settings['BLACK'])
            else:
                self.text = self.font.render('Wlacz efekty dzwiekowe', True, settings['BLACK'])

        def draw(self):
            self.update_text()
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.hover_color, self.rect.inflate(10, 10), 0, 5)
            else:
                pygame.draw.rect(self.screen, self.color, self.rect.inflate(10, 10), 0, 5)
            self.screen.blit(self.text, self.rect)

    save_button = Button(screen, 'Zapisz')
    volume_slider = VolumeSlider(screen, current_volume)
    sound_effects_checkbox = SoundEffectsCheckbox(screen)
    reset_button = Button(screen, 'Przywroc domyslne', 50)

    while True:

        settings = load_settings()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if save_button.rect.collidepoint(event.pos):
                        if local_sound_effects:
                            button_click_sound.play()
                        save_settings(current_volume, local_sound_effects)
                        callback()
                        return

                    if volume_slider.slider_rect.collidepoint(event.pos):
                        volume_slider.dragging = True

                    if sound_effects_checkbox.rect.collidepoint(event.pos):
                        local_sound_effects = not local_sound_effects
                        if local_sound_effects:
                            button_click_sound.play()

                    if reset_button.rect.collidepoint(event.pos):
                        if local_sound_effects:
                            button_click_sound.play()
                        reset_to_default()
                        callback()
                        return

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    volume_slider.dragging = False


        screen.fill(settings['BLACK'])

        save_button.draw()
        volume_slider.draw()
        reset_button.draw()
        sound_effects_checkbox.draw()

        pygame.display.flip()
        current_volume = volume_slider.current_value