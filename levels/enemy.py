import pygame as pg
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, path, image, speed, health = 100):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.path = path
        self.current_waypoint_index = 0
        self.rect.center = self.path[self.current_waypoint_index]
        self.speed = speed
        self.health = health
        self.max_health = health
        self.money_per_kill = 100

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

    def draw_health(self, surface):
        health_bar_width = self.rect.width
        health_bar_height = 5
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y - health_bar_height

        pg.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pg.draw.rect(surface, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width * (self.health / self.max_health), health_bar_height))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_health(surface)