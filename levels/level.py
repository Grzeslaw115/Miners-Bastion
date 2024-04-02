import pygame as pg
import sys
import json
from .world import World
from .turret import Turret
from settingsLoader import load_settings
import constants as c
from button import Button

settings = load_settings()
SCREEN_WIDTH = settings['SCREEN_WIDTH']
SCREEN_HEIGHT = settings['SCREEN_HEIGHT']


def create_turret(mouse_pos, turret_image, turret_group, world):
    x_coord, y_coord = mouse_pos[0] // c.TILE_SIZE, mouse_pos[1] // c.TILE_SIZE

    mouse_tile_num = (y_coord * c.COLUMNS) + x_coord

    if world.tile_map[mouse_tile_num] in [95, 148, 145, 7, 10]:
        # Check if turret is already there
        is_space_free = True
        for turret in turret_group:
            if x_coord == turret.tile_x and y_coord == turret.tile_y:
                is_space_free = False
                break

        if is_space_free:
            new_turret = Turret(turret_image, x_coord, y_coord)
            turret_group.add(new_turret)


def load_level(level):
    # Initialize the game
    pg.init()
    clock = pg.time.Clock()

    # Set the screen size
    screen = pg.display.set_mode((1024 + c.SIDE_PANEL, 1024))

    placing_turrets = False


    # Images
    enemy_image = pg.image.load("graphics/enemies/integrate.png").convert_alpha()
    map_image = pg.image.load("graphics/maps/" + level + ".png").convert_alpha()
    turret_image = pg.image.load("graphics/turrets/towerDefense_tile249.png").convert_alpha()
    turret_button_image = pg.image.load("graphics/buttons/turret1_button.png").convert_alpha()
    cancel_button_image = pg.image.load("graphics/buttons/cancel_button.png").convert_alpha()
    cursor_turret = pg.image.load("graphics/turrets/towerDefense_tile249.png").convert_alpha()

    # Load json data for level
    with open('levels/'+level+'.tmj') as infile:
        world_data = json.load(infile)

    # Create world
    world = World(world_data, map_image)
    world.process_data()

    # Create groups
    turret_group = pg.sprite.Group()

    # Create buttons
    turret_button = Button(1024, 120, turret_button_image, True)
    cancel_button = Button(1024, 924, cancel_button_image, True)



    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
                    if placing_turrets:
                        create_turret(mouse_pos, turret_image, turret_group, world)

        screen.fill("black")

        # Draw
        world.draw(screen)
        turret_group.draw(screen)

        if turret_button.draw(screen):
            placing_turrets = True

        if placing_turrets:
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] <= 1024:
                screen.blit(cursor_turret, cursor_rect)

            if cancel_button.draw(screen):
                placing_turrets = False

        clock.tick(60)
        pg.display.update()