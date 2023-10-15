from tilemap import Tilemap
import pygame as pg
from const import COLOURS
import json

class EditorMapManager:
    def __init__(self, surface_size, blit_off_x, blit_off_y, font) -> None:
        self.surface_size = surface_size
        self.map_surface = pg.Surface(surface_size).convert()
        self.hud_surface = pg.Surface(surface_size).convert()
        self.hud_surface.set_colorkey(COLOURS['transparent black'])
        self.blit_pos = (blit_off_x, blit_off_y)
        self.last_frame = None
        self.font = font
        
        # map variables
        self.scroll_speed = 9
        self.scroll_offset = [0,0]
        self.display_grid = 0

        # hud variables
        self.hud_render_status = 1
        self.current_asset = None
        self.current_layer = 0
        self.layer_count = 0
        self.current_tool = 'none'
        self.tile_pos = None
        
    def update(self, mouse_data, keyboard_data, asset_manager_data) -> None:
        # update asset manager data
        self.current_asset = asset_manager_data['current asset']

        # update hud
        self.update_hud()

        # update hud
        self.update_map(keyboard_data)

    def update_hud(self) -> None:
        # wipe surface for new frame
        self.hud_surface.fill(COLOURS['transparent black'])

    def update_map(self, keyboard_data) -> None:
        # wipe surface for new frame
        self.map_surface.fill(COLOURS['blue 3'])

        # handle keyboard input updates
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
        current_tool_text = 'tool selected : ' + str(self.current_tool)
        current_tool_text_center = self.font.get_center(current_tool_text)
        self.font.write(self.hud_surface, current_tool_text, [self.surface_size[0] - (current_tool_text_center[0]*2) - 6, 3], shadow=1)

        current_layer_text = 'layer ' + str(self.current_layer) + '/' + str(self.layer_count)
        current_layer_text_center = self.font.get_center(current_layer_text)
        self.font.write(self.hud_surface, current_layer_text, [self.surface_size[0] - (current_layer_text_center[0]*2) - 6, 15], shadow=1)

        # render current selected asset
        if self.current_asset:
            self.font.write(self.hud_surface, self.current_asset[0], [6,3], shadow=1)
            self.hud_surface.blit(self.current_asset[1][0], (6, 18))
        else:
            self.font.write(self.hud_surface, 'no asset selected', [6,3], shadow=1)

        # render hud to main surface
        surface.blit(self.hud_surface, self.blit_pos)

    def render_map(self, surface) -> None:
        # render map to main surface
        surface.blit(self.map_surface, (self.blit_pos[0]+self.scroll_offset[0], self.blit_pos[1]+self.scroll_offset[1]))
