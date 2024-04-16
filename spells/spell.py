import pygame as pg
import math

# Base class for other spells
class Spell():
    def __init__(self, name, cost, range, duration, cooldown):
        self.name = name
        self.cost = cost
        self.range = range
        self.duration = duration
        self.cooldown = cooldown * 1000
        self.last_cast = pg.time.get_ticks()

    def can_cast(self):
        return (pg.time.get_ticks() - self.last_cast) >= self.cooldown

    def cast(self, x, y, enemies, current_time):
        self.last_cast = current_time
        for enemy in enemies:
            if self.is_in_range(x, y, enemy) and not enemy.isSpelled:
                enemy.spell(self)

    def draw_cooldown(self, screen, x, y):
        cooldown = self.cooldown / 1000
        current_time = pg.time.get_ticks()
        time_since_last_cast = current_time - self.last_cast
        time_left = cooldown - time_since_last_cast / 1000

        if time_left > 0:
            pg.draw.rect(screen, (0, 0, 0), (x - 25, y + 30, 50, 10))
            pg.draw.rect(screen, (255, 0, 0), (x - 25, y + 30, 50 * (time_left / cooldown), 10))

    def apply_effect(self, enemy):
        pass

    def restore_effect(self, enemy):
        pass

    def draw_range(self, surface, x, y):
        pg.draw.circle(surface, (255, 0, 0), (x, y), self.range, 1)

    def is_in_range(self, x, y, enemy):
        return ( (x - enemy.rect.center[0]) ** 2 + (y - enemy.rect.center[1]) ** 2 ) ** 0.5 <= self.range