import pygame as pg
import sys
import json
from .world import World


def main():
    # Initialize the game
    pg.init()
    clock = pg.time.Clock()


    # Set the screen size
    screen = pg.display.set_mode((1024, 1024))

    # Images
    enemy_image = pg.image.load("graphics/enemies/integrate.png").convert_alpha()
    map_image = pg.image.load("graphics/maps/level2.png").convert_alpha()

    # Load json data for level
    with open('levels/level2.tmj') as file:
        world_data = json.load(file)

    # Create world
    world = World(world_data, map_image)
    world.process_data()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        world.draw(screen)

        clock.tick(60)
        pg.display.update()