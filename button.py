import pygame as pg

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        is_clicked = False
        # Mouse position
        pos = pg.mouse.get_pos()

        # Mouse over and clicked
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked is False:
                is_clicked = True
                self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw
        surface.blit(self.image, self.rect)

        return is_clicked