import pygame as pg
from tile import Tile

class Tilemap:
    def __init__(self, map_size, tile_size) -> None:
        self.map_surface = pg.Surface(map_size).convert()
        self.terrain = {}
        self.decorative = {}

    def save_map(self, map_name) -> None:
        pass

    def load_map(self, map_name) -> None:
        pass

    def add_tile(self, pos, layer, tile) -> None:
        self.terrain[layer][pos] = tile

    def remove_tile(self, pos, layer) -> None:
        if pos in self.terrain[layer]:
            self.terrain[layer].pop(pos)

    def update(self) -> None:
        pass

    def render(self, surface) -> None:
        pass