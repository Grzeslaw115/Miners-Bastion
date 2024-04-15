import pygame as pg
import constants as c
import math
from button import Button

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, cost, damage, build_animation_sheet, tile_x, tile_y, world, screen = None):
        pg.sprite.Sprite.__init__(self)
        self.range = 150
        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None
        self.upgrade_panel = UpgradePanel(self, screen)
        self.world = world
        self.build_animation_sheet = build_animation_sheet

        self.cost = cost
        self.damage = damage

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        self.angle = 90
        self.org_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.update_range_visual()  # Initialize the range visualization

    def load_images(self):
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            tmp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(tmp_img)
        return animation_list

    def update(self, enemy_group):
        self.aim(enemy_group)
        if self.target:
            self.play_animation()
        else:
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)

    def play_animation(self):
        self.org_image = self.animation_list[self.frame_index]
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % c.ANIMATION_STEPS
            if self.frame_index == 0:
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def draw(self, surface):
        self.image = pg.transform.rotate(self.org_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
            self.upgrade_panel.draw()

    def update_range_visual(self):
        # Create range circle
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "gray100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def pick_target(self, enemy_group):
        for target in enemy_group:
            x_dist = target.rect.centerx - self.x
            y_dist = target.rect.centery - self.y
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                self.target = target
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                target.health -= self.damage

    def aim(self, enemy_group):
        for target in enemy_group:
            x_dist = target.rect.centerx - self.x
            y_dist = target.rect.centery - self.y
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))

    def build_turret(self, surface, enemy_group, turret_group):
        frame_duration = 150  # Duration of each frame in milliseconds (250ms = 1/4 second)
        total_duration = 1200  # Total duration of animation in milliseconds (2 seconds)
        num_frames = 8  # Total number of frames in the sprite sheet

        frame_width = self.build_animation_sheet.get_width() // num_frames
        frame_height = self.build_animation_sheet.get_height()

        frame_index = 0
        current_time = 0

        # Save the original image and set the current image to the first frame
        original_image = self.image
        self.image = self.build_animation_sheet.subsurface(0, 0, frame_width, frame_height)

        clock = pg.time.Clock()

        while current_time < total_duration:
            current_frame_time = pg.time.get_ticks()

            # Display the current frame at the turret's position
            self.world.draw(surface)
            for enemy in enemy_group:
                enemy.draw(surface)
            for turret in turret_group:
                turret.draw(surface)
            surface.blit(self.image, self.rect)


            # Update the display
            pg.display.flip()

            # Wait for the remaining time of the frame
            pg.time.delay(frame_duration)

            current_time += pg.time.get_ticks() - current_frame_time
            frame_index = (frame_index + 1) % num_frames

            # Update the current frame
            self.image = self.build_animation_sheet.subsurface(frame_index * frame_width, 0, frame_width, frame_height)

        # Restore the original image after the animation finishes
        self.image = original_image

class UpgradePanel:
    def __init__(self, turret, surface):
        self.turret = turret
        self.buttons = [
            Button(0, 0, None, "Increase damage", self.upgrade_damage, True),
            Button(0, 50, None, "Increase range", self.upgrade_range, True),
            Button(0, 100, None, "Sell turret", self.sell_turret, True)
        ]
        self.surface = surface

    def draw(self):
        for button in self.buttons:
            button.draw(self.surface)

    def upgrade_damage(self):
        if self.turret.world.money >= 50:
            self.turret.world.money -= 50
            self.turret.damage += 10

    def upgrade_range(self):
        if self.turret.world.money >= 75:
            self.turret.world.money -= 75
            self.turret.range += 15
            self.turret.update_range_visual()

    def sell_turret(self):
        self.turret.kill()
        self.turret.world.money += self.turret.cost // 2 # Zwracam polowe kosztu