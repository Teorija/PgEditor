from tilemap import Tilemap
import pygame as pg
from const import COLOURS
import json

class EditorMapManager:
    def __init__(self, surface_size, map_size, blit_off_x, blit_off_y, font) -> None:
        self.surface_size = surface_size
        self.map_surface = pg.Surface(surface_size).convert()
        self.hud_surface = pg.Surface(surface_size).convert()
        self.hud_surface.set_colorkey(COLOURS['transparent black'])
        self.blit_pos = (blit_off_x, blit_off_y)
        self.last_frame = None
        self.font = font
        
        # map variables
        self.tile_size = 16
        self.map_size = [map_size[0]//self.tile_size, map_size[1]//self.tile_size]
        self.map = Tilemap(self.map_size, self.tile_size)
        self.zoom_scale = 1
        self.reset_offset = 0
        self.scroll_speed = 3
        self.scroll_offset = [0,0]
        self.display_grid = 0
        self.mouse_pos = None

        # hud variables
        self.hud_render_status = 1
        self.current_asset = None
        self.current_layer = 0
        self.layer_count = 0
        self.current_tool = 'none'
        self.mouse_pos = None
        
    def update(self, mouse_data, keyboard_data, asset_manager_data, toolbar_data) -> None:
        # update mouse data
        self.mouse_pos = mouse_data['pos']

        # update asset manager data
        self.current_asset = asset_manager_data['current asset']

        # update hud
        self.update_hud(toolbar_data)

        # update hud
        self.update_map(mouse_data, keyboard_data, toolbar_data)

    def update_hud(self, toolbar_data) -> None:
        # wipe surface for new frame
        self.hud_surface.fill(COLOURS['transparent black'])

        # update hud variables
        self.current_layer = toolbar_data['current layer']
        self.layer_count = toolbar_data['layer count']

    def update_map(self, mouse_data, keyboard_data, toolbar_data) -> None:
        # wipe surface for new frame
        self.map_surface.fill(COLOURS['red 2'])

        # handle grid display
        if self.display_grid != toolbar_data['grid status']:
            self.display_grid = toolbar_data['grid status']

        # handle map pos reset
        if toolbar_data['reset status']:
            self.scroll_offset = [0,0]

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
        mouse_pos_text = str(self.mouse_pos)
        mouse_pos_text_center = self.font.get_center(mouse_pos_text)
        self.font.write(self.hud_surface, str(self.mouse_pos), [self.surface_size[0] - (mouse_pos_text_center[0]*2) - 6, 3], shadow=1)

        current_layer_text = 'layer ' + str(self.current_layer) + '/' + str(self.layer_count)
        current_layer_text_center = self.font.get_center(current_layer_text)
        self.font.write(self.hud_surface, current_layer_text, [self.surface_size[0] - (current_layer_text_center[0]*2) - 6, 18], shadow=1)

        # render current selected asset
        if self.current_asset:
            self.font.write(self.hud_surface, self.current_asset[0], [6,3], shadow=1)
            self.hud_surface.blit(self.current_asset[1][0], (6, 18))
        else:
            self.font.write(self.hud_surface, 'no asset selected', [6,3], shadow=1)

        # render hud to main surface
        surface.blit(self.hud_surface, self.blit_pos)

    def render_map(self, surface) -> None:
        # render grid
        if self.display_grid:
            self.render_grid()

        # render map to main surface
        surface.blit(pg.transform.scale_by(self.map_surface, self.zoom_scale), (self.blit_pos[0]+self.scroll_offset[0], self.blit_pos[1]+self.scroll_offset[1]))

    def render_grid(self) -> None:
        rows = self.map_size[1]
        cols = self.map_size[0]
        
        for row in range(1, rows):
            pg.draw.line(self.map_surface, COLOURS['black'], (0, row*self.tile_size), (cols*self.tile_size, row*self.tile_size))
            for col in range(1, cols):
                pg.draw.line(self.map_surface, COLOURS['black'], (col*self.tile_size, 0), (col*self.tile_size, rows*self.tile_size))