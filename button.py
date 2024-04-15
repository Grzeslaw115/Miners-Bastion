import pygame as pg
from settingsLoader import load_settings

settings = load_settings()

class Button():
    def __init__(self, x, y, image, text=None, action=None, show_rect = False):
        self.image = image
        if self.image:
            self.rect = self.image.get_rect()
        else:
            self.rect = pg.Rect(x, y, 200, 50)
        self.rect.topleft = (x, y)
        self.clicked = False
        self.text = text
        self.action = action
        self.show_rect = show_rect

    def is_clicked(self):
        is_clicked = False
        # Mouse position
        pos = pg.mouse.get_pos()

        # Mouse over and clicked
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked is False:
                is_clicked = True
                self.clicked = True
                if self.action:
                    self.action()
                    self.clicked = False
                if settings['SOUND_EFFECTS']:
                    pg.mixer.Sound('assets/audio/menu/button_click.mp3').play()

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return is_clicked

    def draw(self, surface):
        # Draw
        if self.image:
            surface.blit(self.image, self.rect)
        if self.text:
            font = pg.font.Font(None, 30)
            text = font.render(self.text, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
            
        if self.show_rect:
            pg.draw.rect(surface, (255, 255, 255), self.rect, 2)