import pygame as pg
import constants as c

class World():
    def __init__(self, data, map_image):
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.tile_map = []
        self.money = c.STARTING_MONEY

    def process_data(self):
        # Extract waypoints
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]


            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data):
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")

            self.waypoints.append((temp_x + 832, temp_y)) # UWAGA! reczne przesuniecie punktow dla level1, trzeba to zmienic

    def draw(self, surface):
        surface.blit(self.image, (0, 0))
