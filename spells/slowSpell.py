from spells.spell import Spell
import pygame as pg

class SlowSpell(Spell):
    def __init__(self, range, duration, cost, cooldown):
        super().__init__("Slow", cost, range, duration, cooldown)
        self.description = f"Costs {self.cost} Slows down enemies for {self.duration} seconds"

    def apply_effect(self, enemy):
        enemy.speed = enemy.speed / 2
        enemy.isSpelled = True

    def restore_effect(self, enemy):
        enemy.speed = enemy.speed * 2
        enemy.spelledWith.pop(self)