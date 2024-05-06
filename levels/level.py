import pygame as pg
import sys
import json
from .world import World
from .turret import Turret
from settingsLoader import load_settings
import constants as c
from button import Button
from .enemy import Enemy
from spells.slowSpell import SlowSpell
from spells.damageSpell import DamageSpell
from PointsLoader import save_score
import random

settings = load_settings()
SCREEN_WIDTH = settings['SCREEN_WIDTH']
SCREEN_HEIGHT = settings['SCREEN_HEIGHT']

def load_level(level, callback):

    def create_turret():
        x_coord, y_coord = mouse_pos[0] // c.TILE_SIZE, mouse_pos[1] // c.TILE_SIZE
        turret_places = c.turret_places

        mouse_tile_num = (y_coord * c.COLUMNS) + x_coord

        if world.tile_map[mouse_tile_num] in turret_places[level]:
            # Check if turret is already there
            is_space_free = True
            for turret in turret_group:
                if x_coord == turret.tile_x and y_coord == turret.tile_y:
                    is_space_free = False
                    break

            if is_space_free and world.money >= turret_info[which_turret][1]:
                new_turret = Turret(*turret_info[which_turret], x_coord, y_coord, world, screen = screen, play_sound = settings['SOUND_EFFECTS'])
                new_turret.build_turret(screen, enemy_group, turret_group)
                turret_group.add(new_turret)
                world.money -= turret_info[which_turret][1]

    def select_turret():
        x_coord, y_coord = mouse_pos[0] // c.TILE_SIZE, mouse_pos[1] // c.TILE_SIZE
        for turret in turret_group:
            if turret.tile_x == x_coord and turret.tile_y == y_coord:
                return turret

    def unselect_turret():
        for turret in turret_group:
            if turret.selected:
                for button in turret.upgrade_panel.buttons:
                    button.is_clicked()
            turret.selected = False

    def draw_money_and_points():
        text_font = pg.font.SysFont("Consolas", 30, bold = True)
        txt_points = text_font.render("POINTS: " + str(world.points), True, "black")
        txt_money = text_font.render("MONEY: " + str(world.money), True, "black")
        screen.blit(txt_points, (1040, 35))
        screen.blit(txt_money, (1040, 65))

    def spawn_enemies(current_time, last_enemy_spawn, enemy_group, world, how_many_spawned):
        if current_time - last_enemy_spawn > 5000: # Spawn enemy every 5 seconds
            how_many_spawned += 1 # Increase the number of spawned enemies, to increase the speed of the next one
            enemy_random = random.randint(0, 1) # Randomize enemy type
            
            if enemy_random == 0: # Integrate enemy
                new_enemy = Enemy(world.waypoints, integrate_image, speed=2 + how_many_spawned * 0.1, sprite_sheet=integrate_sheet)
            else: # Haskell enemy
                new_enemy = Enemy(world.waypoints, haskell_image, speed=4, sprite_sheet=haskell_sheet, health=30 + how_many_spawned * 0.15, money_per_kill=50)
            enemy_group.add(new_enemy)
            last_enemy_spawn = current_time

        return last_enemy_spawn, how_many_spawned

    # Initialize the game
    pg.init()
    clock = pg.time.Clock()

    # Set the screen size
    screen = pg.display.set_mode((1024 + c.SIDE_PANEL, 1024))

    placing_turrets = False
    game_over = False
    selected_turret = None

    show_spell_range = False
    current_spell = None
    spell_position = None

    # Animations
    turret1_sheet = pg.image.load("graphics/turrets/turret1_animation.png").convert_alpha()
    turret2_sheet = pg.image.load("graphics/turrets/turret2_animation.png").convert_alpha()
    integrate_sheet = pg.image.load("graphics/enemies/animacjaIntegrate1.png").convert_alpha()
    haskell_sheet = pg.image.load("graphics/enemies/animacjaHaskell1.png").convert_alpha()
    build_turret1_animation_sheet = pg.image.load("graphics/turrets/build_turret1_animation.png").convert_alpha()
    build_turret2_animation_sheet = pg.image.load("graphics/turrets/build_turret2_animation.png").convert_alpha()

    # Images
    map_image = pg.image.load("graphics/maps/" + level + ".png").convert_alpha()
    turret_button_image = pg.image.load("graphics/buttons/turret1_button.png").convert_alpha()
    turret2_button_image = pg.image.load("graphics/buttons/turret2_button.png").convert_alpha()
    cancel_button_image = pg.image.load("graphics/buttons/cancel_button.png").convert_alpha()
    cursor_turret = pg.image.load("graphics/turrets/turret1.png").convert_alpha()
    cursor_turret2 = pg.image.load("graphics/turrets/turret2.png").convert_alpha()
    slow_spell_button_image = pg.image.load("graphics/buttons/slowSpell_button.png").convert_alpha()
    damage_spell_button_image = pg.image.load("graphics/buttons/damageSpell_button.png").convert_alpha()
    integrate_image = pg.image.load("graphics/enemies/integrate.png").convert_alpha()
    integrate_image = pg.transform.scale(integrate_image, (integrate_image.get_width(), integrate_image.get_height()))
    haskell_image = pg.image.load("graphics/enemies/haskell.png").convert_alpha()
    haskell_image = pg.transform.scale(haskell_image, (haskell_image.get_width(), haskell_image.get_height()))
    back_to_menu_img = pg.image.load("graphics/menu/backToMenuButton.png").convert_alpha()

    # Load json data for level
    with open('levels/'+level+'.tmj') as infile:
        world_data = json.load(infile)

    # Create world
    world = World(world_data, map_image)
    world.process_data(level)

    # Enemies parameters
    last_enemy_spawn = 0
    how_many_spawned = 0

    # Create groups
    enemy_group = pg.sprite.Group()
    turret_group = pg.sprite.Group()

    # Create buttons
    turret1_button = Button(1024, 120, turret_button_image)
    turret2_button = Button(1024, 220, turret2_button_image)
    back_button = Button(1240, 25, back_to_menu_img)
    restartButton = Button(SCREEN_WIDTH / 2, 500, None, "Retake a year", action=lambda: load_level(level, callback), font_size=60)

    turret_buttons = [turret1_button, turret2_button]

    spell_buttons = {
    slowSpell_button := Button(1024, 320, slow_spell_button_image),
    damageSpell_button := Button(1024, 420, damage_spell_button_image)}

    cancel_button = Button(1024, 924, cancel_button_image)

    cursors = [cursor_turret, cursor_turret2]
    which_turret_buying = [False, False]
    which_turret = None
    turret_info = [(turret1_sheet, 200, 25, build_turret1_animation_sheet), (turret2_sheet, 500, 50, build_turret2_animation_sheet)]  # Animation sheet, cost, damage, build animation

    # Create spells
    slow_spell = SlowSpell(100, 5, 50, 5)
    damage_spell = DamageSpell(150, 5, 50, 5)

    while True:
        if game_over:
            break
        screen.fill("black")

        pg.draw.rect(screen, "white", (1024, 0, 300, 120))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()

                if back_button.rect.collidepoint(event.pos):
                    save_score(world.points)
                    callback()
                    return

                if mouse_pos[0] < SCREEN_WIDTH and mouse_pos[1] < SCREEN_HEIGHT:
                    # Spell casting
                    if show_spell_range and world.money >= current_spell.cost:
                        current_spell.cast(spell_position[0], spell_position[1], enemy_group, pg.time.get_ticks())
                        show_spell_range = False
                        world.money -= current_spell.cost

                    if placing_turrets:
                        create_turret()
                    else:
                        unselect_turret()
                        selected_turret = select_turret()

        current_time = pg.time.get_ticks()
        # We spawn a new enemy every 5 seconds and increase the speed every 10 seconds
        last_enemy_spawn, how_many_spawned = spawn_enemies(current_time, last_enemy_spawn, enemy_group, world, how_many_spawned)

        turret_group.update(enemy_group)
        if selected_turret:
            selected_turret.selected = True

        # Draw
        world.draw(screen)
        draw_money_and_points()
        back_button.draw(screen)

        for turret in turret_group:
            turret.draw(screen)

        for enemy in enemy_group:
            enemy.update()
            enemy.draw(screen)
            if enemy.current_waypoint_index == len(world.waypoints):
                game_over = True
            if enemy.health <= 0 and not enemy.isDead:
                world.money += enemy.money_per_kill
                world.points += enemy.points_per_kill
                enemy.isDead = True
            for spell in list(enemy.spelledWith):
                if current_time - enemy.spelledWith[spell] >= spell.duration * 1000:
                    spell.restore_effect(enemy)

        for i, turret_button in enumerate(turret_buttons):
            turret_button.draw(screen)
            if turret_button.is_clicked():
                if show_spell_range:
                    show_spell_range = False
                which_turret_buying = [False for _ in range(len(which_turret_buying))]
                which_turret_buying[i] = True
                placing_turrets = True
                which_turret = i
            if which_turret_buying[i]:
                cancel_button.draw(screen)
                cursor_rect = cursors[i].get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= 1024:
                    screen.blit(cursors[i], cursor_rect)
                if cancel_button.is_clicked():
                    which_turret_buying = [False for _ in range(len(which_turret_buying))]
                    placing_turrets = False
                    which_turret = None
                    show_spell_range = False

        for spell_button in spell_buttons:
            spell_button.draw(screen)
            if spell_button.is_clicked():
                which_turret_buying = [False for _ in range(len(which_turret_buying))]
                placing_turrets = False
                which_turret = None
                placing_turrets = False

                if spell_button == slowSpell_button:  # Slow spell
                    current_spell = slow_spell
                elif spell_button == damageSpell_button:  # Damage spell
                    current_spell = damage_spell

                if current_spell.can_cast() and world.money >= current_spell.cost:
                    show_spell_range = True
                spell_position = pg.mouse.get_pos()

        if show_spell_range:
            spell_position = pg.mouse.get_pos()
            current_spell.draw_range(screen, spell_position[0], spell_position[1])
            current_spell.draw_description(screen, pg.font.SysFont("Consolas", 20), 0, 0)
 
        # Drawing cooldowns
        slow_spell.draw_cooldown(screen, 1224, 370)
        damage_spell.draw_cooldown(screen, 1224, 470)

        clock.tick(60)
        pg.display.update()

    # Game over screen
    save_score(world.points)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if restartButton.rect.collidepoint(mouse_pos):
                    load_level(level, callback)
                    return

        screen.fill((0, 0, 0))
        restartButton.draw(screen)
        pg.display.update()
        clock.tick(60)