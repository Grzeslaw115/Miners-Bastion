from spells.spell import Spell
import pygame as pg

class SlowSpell(Spell):
    def __init__(self, range, duration, cost, cooldown):
        super().__init__("Slow", cost, range, duration, cooldown)

    def apply_effect(self, enemy):
        enemy.speed = enemy.speed / 2
        enemy.isSpelled = True

    def restore_effect(self, enemy):
        enemy.speed = enemy.speed * 2
        enemy.isSpelled = False