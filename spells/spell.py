import pygame as pg

# Base class for other spells
class Spell():
    def __init__(self, name, cost, range, duration, cooldown):
        self.name = name
        self.cost = cost
        self.range = range
        self.duration = duration
        self.cooldown = cooldown
        self.last_cast = 0

    def cast(self, x, y, enemies, current_time):
        if current_time - self.last_cast > self.cooldown:
            self.last_cast = current_time
            for enemy in enemies:
                if self.is_in_range(x, y, enemy) and not enemy.isSpelled:
                    enemy.spell(self)

    def apply_effect(self, enemy):
        pass

    def restore_effect(self, enemy):
        pass

    def draw_range(self, surface, x, y):
        pg.draw.circle(surface, (255, 0, 0), (x, y), self.range, 1)

    def is_in_range(self, x, y, enemy):
        return ( (x - enemy.rect.center[0]) ** 2 + (y - enemy.rect.center[1]) ** 2 ) ** 0.5 <= self.range