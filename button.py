import pygame as pg
from settingsLoader import load_settings

class Button():
    def __init__(self, x, y, image, text=None, action=None, show_rect = False, font_size=30, description=""):
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
        self.font_size = font_size
        self.description = description

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
                settings = load_settings()
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
            font = pg.font.Font(None, self.font_size)
            text = font.render(self.text, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
            
        if self.show_rect:
            pg.draw.rect(surface, (255, 255, 255), self.rect, 2)

    def is_mouse_over(self):
        pos = pg.mouse.get_pos()
        return self.rect.collidepoint(pos)

    def draw_description(self, surface):
        if self.description:
            font = pg.font.Font(None, 30)
            text = font.render(self.description, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))

            # Background rectangle settings
            bg_rect = pg.Rect(text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10)

            rect_surface = pg.Surface((bg_rect.width, bg_rect.height))
            rect_surface.set_alpha(128) 
            rect_surface.fill((50, 50, 50))

            # If the description would be drawn off-screen, move it accordingly
            if text_rect.right > surface.get_width():
                text_rect.x = surface.get_width() - text_rect.width
                bg_rect.x = text_rect.x - abs(bg_rect.width - text_rect.width) - 10
            if text_rect.left < 0:
                text_rect.x = 0
                bg_rect.x = 0


            surface.blit(rect_surface, bg_rect.topleft)
            surface.blit(text, text_rect)
