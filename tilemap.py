import pygame as pg
from tile import Tile
import json

class Tilemap:
    def __init__(self, map_size, tile_size) -> None:
        self.map_size = map_size
        self.tile_size = tile_size
        self.map_surface = pg.Surface(map_size).convert()
        self.terrain = {}

    def save_map(self, map_name) -> None:
        pass

    def load_map(self, map_name) -> None:
        pass

    def add_layer(self, layer) -> None:
        self.terrain[layer] = {}

    def add_tile(self, pos, layer, type, tile_name, tile_img) -> None:
        if pos[0] < 0 or pos[0] > self.map_size[0] or pos[1] < 0 or pos[1] > self.map_size[1]:
            return
        
        if type == 'terrain':
            self.terrain[layer][pos] = Tile(type, pos, tile_name, tile_img, self.tile_size)

    def remove_layer(self, layer, total_layers) -> None:
        current_layer = layer + 1

        if current_layer in self.terrain:
            if current_layer == total_layers + 1:
                self.terrain.pop(current_layer)
                return
            
            for i in range(current_layer+1, total_layers+1):
                self.terrain[i-1] = self.terrain.pop(i)
            
    def remove_tile(self, pos, layer) -> None:
        if pos in self.terrain[layer]:
            self.terrain[layer].pop(pos)

    def update(self) -> None:
        pass

    def render(self, surface, layer=0) -> None:
        print(self.terrain)
        for layer in self.terrain:
            for tile_pos in self.terrain[layer]:
                surface.blit(self.terrain[layer][tile_pos].get_image(), self.terrain[layer][tile_pos].get_pos())

    def clear_map(self) -> None:
        self.terain = {}