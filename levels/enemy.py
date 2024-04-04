import pygame as pg
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, path, image, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.path = path
        self.current_waypoint_index = 0
        self.rect.center = self.path[self.current_waypoint_index]
        self.speed = speed

    def update(self):
        if self.current_waypoint_index < len(self.path):
            current_waypoint = self.path[self.current_waypoint_index]

            direction = (current_waypoint[0] - self.rect.centerx, current_waypoint[1] - self.rect.centery)
            distance = math.sqrt(direction[0]**2 + direction[1]**2)

            if distance > 0:
                direction = (direction[0] / distance, direction[1] / distance)

            self.rect.centerx += direction[0] * self.speed
            self.rect.centery += direction[1] * self.speed
            
            if distance <= self.speed:
                self.current_waypoint_index += 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)