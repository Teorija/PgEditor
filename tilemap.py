import pygame as pg
from tile import Tile

class Tilemap:
    def __init__(self, map_size) -> None:
        self.map_surface = pg.Surface(map_size).convert()
        self.terrain = {}
        self.decorative = {}