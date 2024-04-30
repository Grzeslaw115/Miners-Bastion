from spells.spell import Spell
import pygame as pg
from time import sleep
import threading

class DamageSpell(Spell):
    def __init__(self, range, duration, cost, cooldown):
        super().__init__("Damage", cost, range, duration, cooldown)
        self.description = f"Costs {self.cost} Deals 10 damage per second for {self.duration} seconds"

    def apply_effect(self, enemy):
        effect_thread = threading.Thread(target=self.effect_thread, args=(enemy,))
        effect_thread.start()

    def effect_thread(self, enemy):
        for _ in range(5):
            enemy.health -= 10
            sleep(1)
            if enemy.health <= 0:
                enemy.kill()

    def restore_effect(self, enemy):
        enemy.spelledWith.pop(self)