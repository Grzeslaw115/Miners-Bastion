import pygame as pg
import sys
import json
from .world import World


def load_level(level):
    # Initialize the game
    pg.init()
    clock = pg.time.Clock()


    # Set the screen size
    screen = pg.display.set_mode((1024, 1024))

    # Images
    enemy_image = pg.image.load("graphics/enemies/integrate.png").convert_alpha()
    map_image = pg.image.load("graphics/maps/" + level + ".png").convert_alpha()

    # Load json data for level
    with open('levels/'+level+'.tmj') as infile:
        world_data = json.load(infile)

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