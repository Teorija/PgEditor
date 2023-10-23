import pygame as pg
from tile import Tile
import json

class Tilemap:
    def __init__(self, map_size, tile_size) -> None:
        self.map_size = map_size
        self.tile_size = tile_size
        self.terrain = {}
        self.decorative = {}

    def save_map(self, map_name) -> None:
        pass

    def load_map(self, map_name) -> None:
        pass

    def add_layer(self, layer) -> None:
        self.terrain[layer] = {}
        self.decorative[layer] = {}

    def add_tile(self, pos, layer, type, tile_name, tile_img) -> None:
        if pos[0] < 0 or pos[0] > self.map_size[0] or pos[1] < 0 or pos[1] > self.map_size[1]:
            return
        
        if type == 'terrain':
            if pos in self.terrain[layer] and self.terrain[layer][pos].get_name() == tile_name:
                return

            self.terrain[layer][pos] = Tile(type, pos, tile_name, tile_img, self.tile_size)

        if type == 'decorative':
            if pos in self.decorative[layer] and self.decorative[layer][pos].get_name() == tile_name:
                return

            self.decorative[layer][pos] = Tile(type, pos, tile_name, tile_img, self.tile_size)

    def remove_layer(self, current_layer, total_layers) -> None:
        current_layer = current_layer + 1
        total_layers = total_layers + 1

        if current_layer in self.terrain:
            self.terrain.pop(current_layer)
            self.decorative.pop(current_layer)

            if current_layer == total_layers:
                return
            
            for i in range(current_layer+1, total_layers+1):
                self.terrain[i-1] = self.terrain.pop(i)
                self.decorative[i-1] = self.decorative.pop(i)

    def remove_tile(self, pos, layer) -> None:
        if pos in self.terrain[layer]:
            self.terrain[layer].pop(pos)

        if pos in self.decorative[layer]:
            self.decorative[layer].pop(pos)

    def render(self, surface, current_layer=0) -> None:
        self.render_decorative(surface, current_layer)
        self.render_terrain(surface, current_layer)

    def render_terrain(self, surface, current_layer) -> None:
        for layer in self.terrain:
            for tile_pos in self.terrain[layer]:
                if current_layer == 0:
                    self.terrain[layer][tile_pos].get_image().set_alpha(255)
                elif layer == current_layer:
                    self.terrain[layer][tile_pos].get_image().set_alpha(255)
                else:
                    self.terrain[layer][tile_pos].get_image().set_alpha(150)

                surface.blit(self.terrain[layer][tile_pos].get_image(), self.terrain[layer][tile_pos].get_pos())

    def render_decorative(self, surface, current_layer) -> None:
        for layer in self.decorative:
            for tile_pos in self.decorative[layer]:
                if current_layer == 0:
                    self.decorative[layer][tile_pos].get_image().set_alpha(255)
                elif layer == current_layer:
                    self.decorative[layer][tile_pos].get_image().set_alpha(255)
                else:
                    self.decorative[layer][tile_pos].get_image().set_alpha(150)

                surface.blit(self.decorative[layer][tile_pos].get_image(), self.decorative[layer][tile_pos].get_pos())

    def clear_map(self) -> None:
        self.terrain.clear()
        self.decorative.clear()