import pygame as pg
from tile import Tile
import json
from const import COLOURS

# To Do
# update tilemap to include more asset types, e.g. entities, lights, particles, etc...

class Tilemap:
    def __init__(self, map_size, tile_size) -> None:
        self.map_name = None
        self.map_size = map_size
        self.tile_size = tile_size
        self.terrain = {}
        self.decorative = {}

    def save_map(self, map_name, map_size, tile_size, layer_count) -> None:
        map_data = {
            'map name': map_name,
            'map size': map_size,
            'tile size': tile_size,
            'layers': layer_count,
            'terrain': {},
            'decorative': {}
        }

        for layer in self.terrain:
            map_data['terrain'][layer] = {}
            for tile_pos in self.terrain[layer]:
                map_data['terrain'][layer][str(tile_pos)] = self.terrain[layer][tile_pos].get_name()

        for layer in self.decorative:
            map_data['decorative'][layer] = {}
            for tile_pos in self.decorative[layer]:
                map_data['decorative'][layer][str(tile_pos)] = self.decorative[layer][tile_pos].get_name()

        with open('assets/maps/'+map_name+'.json', 'w') as f:
            json.dump(map_data, f, indent=4)

    def load_map(self, map_name) -> None:
        with open('assets/maps/'+map_name, 'r') as f:
            map_data = json.load(f)

        self.map_name = map_data['map name']
        self.map_size = map_data['map size']
        self.tile_size = map_data['tile size']
        layer_count = map_data['layers']

        for layer in map_data['terrain']:
            self.terrain[int(layer)] = {}
            for tile_pos in map_data['terrain'][layer]:
                img = pg.image.load('assets/editor assets/terrain/'+map_data['terrain'][layer][tile_pos]+'.png').convert_alpha()
                img.set_colorkey(COLOURS['transparent black'])
                self.terrain[int(layer)][eval(tile_pos)] = Tile('terrain', eval(tile_pos), map_data['terrain'][layer][tile_pos], img, self.tile_size)

        for layer in map_data['decorative']:
            self.decorative[int(layer)] = {}
            for tile_pos in map_data['decorative'][layer]:
                img = pg.image.load('assets/editor assets/decorative/'+map_data['decorative'][layer][tile_pos]+'.png').convert_alpha()
                img.set_colorkey(COLOURS['transparent black'])
                self.decorative[int(layer)][eval(tile_pos)] = Tile('decorative', eval(tile_pos), map_data['decorative'][layer][tile_pos], img, self.tile_size)

        return (self.map_name, self.map_size, self.tile_size, layer_count)

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