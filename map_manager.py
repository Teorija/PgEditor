from tilemap import Tilemap
import pygame as pg
from const import COLOURS

class EditorMapManager:
    def __init__(self, surface_size, blit_off_x, blit_off_y) -> None:
        self.map_surface = pg.Surface(surface_size).convert()
        self.hud_surface = pg.Surface(surface_size).convert()
        self.hud_surface.set_colorkey(COLOURS['transparent black'])
        self.blit_pos = (blit_off_x, blit_off_y)
        self.last_frame = None
        
        # map variables
        self.scroll_speed = 3
        self.scroll_offset = [0,0]
        self.display_grid = 0

        # hud variables
        self.current_asset = None
        self.current_layer = 0
        self.tile_pos = None
        
    def update(self, keyboard_data) -> None:
        # wipe surface for new frame
        self.map_surface.fill(COLOURS['blue 3'])

        # handle keyboard input updates
        if keyboard_data['arrow keys']['left']:
            self.scroll_offset[0] -= 1*self.scroll_speed
        if keyboard_data['arrow keys']['right']:
            self.scroll_offset[0] += 1*self.scroll_speed
        if keyboard_data['arrow keys']['up']:
            self.scroll_offset[1] -= 1*self.scroll_speed
        if keyboard_data['arrow keys']['down']:
            self.scroll_offset[1] += 1*self.scroll_speed

    def render(self, surface) -> None:
        surface.blit(self.map_surface, (self.blit_pos[0]+self.scroll_offset[0], self.blit_pos[1]+self.scroll_offset[1]))
        surface.blit(self.hud_surface, self.blit_pos)