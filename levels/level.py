import pygame as pg
import sys
import json
from .world import World
from .turret import Turret
from settingsLoader import load_settings
import constants as c
from button import Button
from .enemy import Enemy

settings = load_settings()
SCREEN_WIDTH = settings['SCREEN_WIDTH']
SCREEN_HEIGHT = settings['SCREEN_HEIGHT']




class RestartButton():
    def __init__(self, x, y, text, level):
        self.x = x
        self.y = y
        self.text = text
        self.level = level

    def draw(self, screen):
        font = pg.font.Font(None, 74)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y))

    def check_click(self, mouse_x, mouse_y):
        if self.x < mouse_x < self.x + 200 and self.y < mouse_y < self.y + 50:
            self.action()

    def action(self):
        load_level(self.level)

def load_level(level):

    def create_turret():
        x_coord, y_coord = mouse_pos[0] // c.TILE_SIZE, mouse_pos[1] // c.TILE_SIZE
        turret_places = {}
        turret_places["level1"] = [95, 148, 145, 7, 10]
        turret_places["level2"] = [115, 165, 168, 30, 27]
        turret_places["level3"] = [667, 579, 582, 717, 720]

        mouse_tile_num = (y_coord * c.COLUMNS) + x_coord

        if world.tile_map[mouse_tile_num] in turret_places[level]:
            # Check if turret is already there
            is_space_free = True
            for turret in turret_group:
                if x_coord == turret.tile_x and y_coord == turret.tile_y:
                    is_space_free = False
                    break

            if is_space_free:
                new_turret = Turret(turret_sheet, x_coord, y_coord)
                turret_group.add(new_turret)


    # Initialize the game
    pg.init()
    clock = pg.time.Clock()

    # Set the screen size
    screen = pg.display.set_mode((1024 + c.SIDE_PANEL, 1024))

    placing_turrets = False
    game_over = False

    # Animations
    turret_sheet = pg.image.load("graphics/turrets/turret1_animation.png").convert_alpha()


    # Images
    map_image = pg.image.load("graphics/maps/" + level + ".png").convert_alpha()
    turret_image = pg.image.load("graphics/turrets/turret1.png").convert_alpha()
    turret_button_image = pg.image.load("graphics/buttons/turret1_button.png").convert_alpha()
    cancel_button_image = pg.image.load("graphics/buttons/cancel_button.png").convert_alpha()
    cursor_turret = pg.image.load("graphics/turrets/turret1.png").convert_alpha()
    enemy_image = pg.image.load("graphics/enemies/integrate.png").convert_alpha()
    enemy_image = pg.transform.scale(enemy_image, (enemy_image.get_width() * 1/8, enemy_image.get_height() * 1/8))

    # Load json data for level
    with open('levels/'+level+'.tmj') as infile:
        world_data = json.load(infile)

    # Create world
    world = World(world_data, map_image)
    world.process_data()

    # Enemies parameters
    last_enemy_spawn = 0
    last_speed_change = 0
    last_enemy_speed = 2
    first_enemy = Enemy(world.waypoints, enemy_image, last_enemy_speed)

    # Create groups
    enemy_group = pg.sprite.Group()
    enemy_group.add(first_enemy)
    turret_group = pg.sprite.Group()

    # Create buttons
    turret_button = Button(1024, 120, turret_button_image, True)
    cancel_button = Button(1024, 924, cancel_button_image, True)

    while True:
        if game_over:
            break
        screen.fill("black")


        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
                        if placing_turrets:
                            create_turret()

        current_time = pg.time.get_ticks()
        # We spawn a new enemy every 5 seconds and increase the speed every 10 seconds
        if current_time - last_enemy_spawn > 5000:
            last_enemy_spawn = current_time
            new_enemy = Enemy(world.waypoints, enemy_image, last_enemy_speed)
            enemy_group.add(new_enemy)
        if current_time - last_enemy_spawn > 10000:
            last_enemy_speed += 0.1
            last_speed_change = current_time

        turret_group.update()


        # Draw
        world.draw(screen)
        turret_group.draw(screen)
        for enemy in enemy_group:
            enemy.update()
            enemy.draw(screen)
            if enemy.current_waypoint_index == len(world.waypoints):
                game_over = True
            if enemy.health <= 0:
                enemy_group.remove(enemy)

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

    # Game over screen

    restartButton = RestartButton(512, 512, "Restart", level)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                restartButton.check_click(mouse_pos[0], mouse_pos[1])

        screen.fill((0, 0, 0))
        font = pg.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(text, (512, 400))
        restartButton.draw(screen)
        pg.display.update()
        clock.tick(60)