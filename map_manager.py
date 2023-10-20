from tilemap import Tilemap
import pygame as pg
from const import COLOURS
import json
import numpy as np

class EditorMapManager:
    def __init__(self, surface_size, map_size, blit_off_x, blit_off_y, font) -> None:
        self.surface_size = surface_size
        self.map_surface = pg.Surface(map_size).convert()
        self.hud_surface = pg.Surface(surface_size).convert()
        self.hud_surface.set_colorkey(COLOURS['transparent black'])
        self.blit_pos = (blit_off_x, blit_off_y)
        self.last_frame = None
        self.font = font
        
        # map variables
        self.tile_size = 16
        self.map_size = [map_size[0]//self.tile_size, map_size[1]//self.tile_size]
        self.map = Tilemap(self.map_surface, self.map_size, self.tile_size)
        self.zoom_scale = 1
        self.reset_offset = 0
        self.scroll_speed = 3
        self.scroll_offset = [0,0]
        self.display_grid = 0
        self.mouse_in_bounds = 0
        self.mouse_pos = None
        self.asset_preview_pos = None
        self.drawing = 0
        self.erasing = 0

        # hud variables
        self.hud_render_status = 1
        self.current_folder = None
        self.current_asset = None
        self.current_layer = 0
        self.layer_count = 0
        
    def update(self, mouse_data, keyboard_data, asset_manager_data, toolbar_data) -> None:
        # update mouse data
        mouse_x = np.clip(((mouse_data['pos'][0] - self.blit_pos[0] - self.scroll_offset[0])/self.zoom_scale)//16, 0, self.map_size[0]-1)
        mouse_y = np.clip(((mouse_data['pos'][1] - self.blit_pos[1] - self.scroll_offset[1])/self.zoom_scale)//16, 0, self.map_size[1]-1)
        self.mouse_pos = (mouse_x, mouse_y)

        # update toolbar data
        self.current_layer = toolbar_data['current layer']
        self.layer_count = toolbar_data['layer count']
        self.drawing = toolbar_data['drawing']
        self.erasing = toolbar_data['erasing']

        # update asset manager data
        self.current_asset = asset_manager_data['current asset']
        self.current_folder = asset_manager_data['current folder']

        # update hud
        self.update_hud()

        # update hud
        self.update_map(mouse_data, keyboard_data, toolbar_data)

    def update_hud(self) -> None:
        # wipe surface for new frame
        self.hud_surface.fill(COLOURS['transparent black'])

    def update_map(self, mouse_data, keyboard_data, toolbar_data) -> None:
        # wipe surface for new frame
        self.map_surface.fill(COLOURS['red 2'])

        # handle mouse position for drawing/erasing features
        if mouse_data['pos'][0] > self.blit_pos[0] and mouse_data['pos'][1] > self.blit_pos[1]:
            self.mouse_in_bounds = 1

            # handle asset preview
            if self.current_asset:
                if self.current_folder == 'terrain':
                    self.asset_preview_pos = ((mouse_data['pos'][0] - self.blit_pos[0] - self.scroll_offset[0] - self.current_asset[1][0].get_width()/2)/self.zoom_scale,
                                           (mouse_data['pos'][1] - self.blit_pos[1] - self.scroll_offset[1] - self.current_asset[1][0].get_height()/2)/self.zoom_scale)
                if self.current_folder == 'decorative':
                    self.asset_preview_pos = ((mouse_data['pos'][0] - self.blit_pos[0] - self.scroll_offset[0])/self.zoom_scale,
                                           (mouse_data['pos'][1] - self.blit_pos[1] - self.scroll_offset[1])/self.zoom_scale)

            # handle map drawing
            if toolbar_data['drawing'] and mouse_data['l_clicking'] and self.current_layer != 0 and self.current_asset:
                self.map.add_tile(self.mouse_pos, self.current_layer, self.current_folder, self.current_asset[0], self.current_asset[1][0].copy())
            
            # handle map erasing
            if toolbar_data['erasing'] and mouse_data['l_clicking'] and self.current_layer != 0:
                self.map.remove_tile(self.mouse_pos, self.current_layer)
        else:
            self.mouse_in_bounds = 0

        # handle grid display
        if self.display_grid != toolbar_data['grid status']:
            self.display_grid = toolbar_data['grid status']

        # handle map pos reset
        if toolbar_data['reset status']:
            self.scroll_offset = [0,0]

        # handle map clear
        if toolbar_data['clear status']:
            self.map.clear_map()

        # handle new layer added
        if toolbar_data['new layer status']:
            self.map.add_layer(self.layer_count)

        # handle layer deletion
        if toolbar_data['delete layer status']:
            self.map.remove_layer(self.current_layer, self.layer_count)

        # handle map zoom in and out
        if self.zoom_scale != toolbar_data['zoom scale']:
            self.zoom_scale = toolbar_data['zoom scale']

        # handle map scrolling
        if not toolbar_data['drag state']:
            return
        
        if keyboard_data['arrow keys']['left']:
            self.scroll_offset[0] += 1*self.scroll_speed
        if keyboard_data['arrow keys']['right']:
            self.scroll_offset[0] -= 1*self.scroll_speed
        if keyboard_data['arrow keys']['up']:
            self.scroll_offset[1] += 1*self.scroll_speed
        if keyboard_data['arrow keys']['down']:
            self.scroll_offset[1] -= 1*self.scroll_speed

    def render(self, surface) -> None:
        # render map
        self.render_map(surface)

        # render hud
        self.render_hud(surface)

    def render_hud(self, surface) -> None:
        if not self.hud_render_status:
            return

        # render hud map elements
        current_layer_text = 'layer ' + str(self.current_layer) + '/' + str(self.layer_count)
        current_layer_text_center = self.font.get_center(current_layer_text)
        self.font.write(self.hud_surface, current_layer_text, [self.surface_size[0] - (current_layer_text_center[0]*2) - 6, 15], shadow=1)

        mouse_pos_text = '(x, y) : (' + str(self.mouse_pos[0]) + ', ' + str(self.mouse_pos[1]) + ')'
        mouse_pos_text_center = self.font.get_center(mouse_pos_text)
        self.font.write(self.hud_surface, mouse_pos_text, [self.surface_size[0] - (mouse_pos_text_center[0]*2) - 6, 3], shadow=1)

        # render current selected asset
        if self.current_asset:
            self.font.write(self.hud_surface, self.current_asset[0], [6,3], shadow=1)
            asset_copy = self.current_asset[1][0].copy()
            asset_copy.set_alpha(255)
            self.hud_surface.blit(asset_copy, (6, 18))
        else:
            self.font.write(self.hud_surface, 'no asset selected', [6,3], shadow=1)

        # render hud to main surface
        surface.blit(self.hud_surface, self.blit_pos)

    def render_map(self, surface) -> None:
        # render grid
        if self.display_grid:
            self.render_grid()

        self.map.render(self.map_surface, self.current_layer)

        # render asset preview
        if self.current_asset and self.asset_preview_pos and self.drawing and self.mouse_in_bounds:
            asset_copy = self.current_asset[1][0].copy()
            asset_copy.set_alpha(150)
            self.map_surface.blit(self.current_asset[1][0], self.asset_preview_pos)

        # render map to main surface
        surface.blit(pg.transform.scale_by(self.map_surface, self.zoom_scale), (self.blit_pos[0]+self.scroll_offset[0], self.blit_pos[1]+self.scroll_offset[1]))

    def render_grid(self) -> None:
        rows = self.map_size[1]
        cols = self.map_size[0]
        
        for row in range(1, rows):
            pg.draw.line(self.map_surface, COLOURS['black'], (0, row*self.tile_size), (cols*self.tile_size, row*self.tile_size))
            for col in range(1, cols):
                pg.draw.line(self.map_surface, COLOURS['black'], (col*self.tile_size, 0), (col*self.tile_size, rows*self.tile_size))