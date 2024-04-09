import pygame as pg
import constants as c

class World():
    def __init__(self, data, map_image):
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.tile_map = []
        self.money = c.STARTING_MONEY

    def process_data(self, level):
        # Extract waypoints
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]


            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data, level)

    def process_waypoints(self, data, level):
        # Chryste panie
        for point in data:
            if level == "level1":
                temp_x = point.get("x") + 832
                temp_y = point.get("y")
            
            if level == "level2":
                temp_x = point.get("x")
                temp_y = point.get("y") + 192

            if level == "level3":
                temp_x = point.get("x") - 64
                temp_y = point.get("y") + 960 

            self.waypoints.append((temp_x, temp_y)) 

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
