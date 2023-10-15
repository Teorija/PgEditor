import pygame as pg
from tile import Tile

class Tilemap:
    def __init__(self, map_size) -> None:
        self.map_surface = pg.Surface(map_size).convert()
        self.terrain = {}
        self.decorative = {}

    def save_map(self, map_name) -> None:
        pass

    def load_map(self, map_name) -> None:
        pass

    def add_tile(self, pos) -> None:
        pass

    def remove_tile(self, pos) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self, surface) -> None:
        pass