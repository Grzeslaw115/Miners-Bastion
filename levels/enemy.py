import pygame as pg
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, path, image, speed, sprite_sheet, health = 100, money_per_kill = 100):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.path = path
        self.current_waypoint_index = 0
        self.rect.center = self.path[self.current_waypoint_index]
        self.speed = speed
        self.health = health
        self.max_health = health
        self.money_per_kill = money_per_kill
        self.sprite_sheet = sprite_sheet
        self.isDead = False
        self.current_dead_animation_index = 0
        self.update_flag = False
        self.isSpelled = False

    def update(self):
        if self.current_waypoint_index < len(self.path) and not self.isDead:
            current_waypoint = self.path[self.current_waypoint_index]

            direction = (current_waypoint[0] - self.rect.centerx, current_waypoint[1] - self.rect.centery)
            distance = math.sqrt(direction[0]**2 + direction[1]**2)

            if distance > 0:
                direction = (direction[0] / distance, direction[1] / distance)

            self.rect.centerx += direction[0] * self.speed
            self.rect.centery += direction[1] * self.speed
            
            if distance <= self.speed:
                self.current_waypoint_index += 1

        elif self.isDead:
            self.update_flag = not self.update_flag
            if self.update_flag:
                self.current_dead_animation_index += 1

                if self.current_dead_animation_index >= 8:
                    self.kill()
                    return

                frame_width = self.sprite_sheet.get_width() // 8
                frame_height = self.sprite_sheet.get_height()
                frame_rect = pg.Rect(self.current_dead_animation_index * frame_width, 0, frame_width, frame_height)
                self.image = self.sprite_sheet.subsurface(frame_rect)

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

    def spell(self, spell):
        self.isSpelled = True
        self.lastSpelled = pg.time.get_ticks()
        spell.apply_effect(self)
        self.duration = spell.duration
        self.spelledWith = spell