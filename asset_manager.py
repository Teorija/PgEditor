import pygame as pg
from const import COLOURS
from ui_elements import *
from utils import load_images
import os

class EditorAssetManager:
    def __init__(self, surface_size, blit_off_y, font) -> None:
        self.surface_size = surface_size
        self.asset_manager_surface = pg.Surface(surface_size).convert()
        self.asset_surface_size = None
        self.asset_surface = None
        self.blit_pos = (0, blit_off_y)
        self.asset_surf_blit_pos = None
        self.scroll_offset = [0,0]
        self.mouse_pos = None
        self.last_frame = None
        self.font = font
        self.assets = {}
        self.ui_elements = {}
        self.current_folder = None
        self.init_assets()
        self.init_ui_elements()

    def init_assets(self) -> None:
        # load asset images
        page_count = 1
        temp_asset_folder = {}
        asset_folder = {}
        cur_pos = [6,6]
        offset = 6

        for folder in os.listdir('assets/editor assets/'):
            folder_path = 'assets/editor assets/' + folder + '/'
            temp_asset_folder[folder] = load_images(folder_path)

            for assets in temp_asset_folder[folder]:
                asset_w = temp_asset_folder[folder][assets][0].get_width()
                asset_h = temp_asset_folder[folder][assets][0].get_height()

                if cur_pos[0] + asset_w + offset > self.asset_surface_size[0]:
                    cur_pos[0] = 6
                    cur_pos[1] += asset_h + offset
                    temp_asset_folder[folder][assets][1].topleft = cur_pos

                if cur_pos[1] + asset_h + offset > self.asset_surface_size[1]:
                    cur_pos[0] = 6
                    cur_pos[1] = 6
                    page_count += 1
                    temp_asset_folder[folder][assets][1].topleft = cur_pos

            self.assets[folder] = asset_folder
            temp_asset_folder = {}

    def init_ui_elements(self) -> None:
        count = 0

        for folder in self.assets:
            self.ui_elements[folder] = TextButton((5*len(folder), 13), (12,3+(count*13)), self.asset_manager_surface, folder, self.font)
            count += 1

        last_elem_pos_y = 3+(count*13)
        self.asset_surface_size = (self.surface_size[0]-12, self.surface_size[1]-last_elem_pos_y-9)
        self.asset_surface = pg.Surface(self.asset_surface_size).convert()
        self.asset_surf_blit_pos = (6, last_elem_pos_y+3)

    def update(self, mouse_data) -> None:
        # wipe surface for next frame
        self.asset_manager_surface.fill(COLOURS['gray 2'])
        self.asset_surface.fill(COLOURS['gray 3'])

        # update mouse position relative to asset manager surface
        self.mouse_pos = (mouse_data['pos'][0], mouse_data['pos'][1]-self.blit_pos[1])

        # handle asset folder selection
        for elem in self.ui_elements:
            # handle collision between button and mouse
            if not self.ui_elements[elem].button_rect.collidepoint(self.mouse_pos):
                self.ui_elements[elem].hovering = 0
                continue

            # handle asset folder hover indication
            self.ui_elements[elem].hovering = 1

            # handle asset folder selectiion indication
            if not mouse_data['l_click']:
                continue

            if not self.current_folder:
                self.current_folder = elem
                self.ui_elements[elem].selected = 1
                continue

            if self.current_folder and self.current_folder == elem:
                self.ui_elements[self.current_folder].selected = 0
                self.current_folder = None
                continue

            if self.current_folder and self.current_folder != elem:
                self.ui_elements[self.current_folder].selected = 0
                self.current_folder = elem
                self.ui_elements[elem].selected = 1
                continue
                    
            # handle asset selection

    def render(self, surface) -> None:
        self.render_ui_elements()
        self.render_assets()
        surface.blit(self.asset_manager_surface, self.blit_pos)

    def render_ui_elements(self) -> None:
        pg.draw.line(self.asset_manager_surface, COLOURS['blue 3'], (6,3), (6,self.asset_surf_blit_pos[1]-9), 1)

        for elem in self.ui_elements:
            self.ui_elements[elem].render()
            if self.ui_elements[elem].selected:
                pg.draw.line(self.asset_manager_surface, COLOURS['red 2'], (6,3), (6,self.ui_elements[elem].text_pos[1]+7), 1)
                pg.draw.line(self.asset_manager_surface, COLOURS['red 2'], (6,self.ui_elements[elem].text_pos[1]+7), (self.ui_elements[elem].text_pos[0],self.ui_elements[elem].text_pos[1]+7), 1)
            else:
                pg.draw.line(self.asset_manager_surface, COLOURS['blue 3'], (6,self.ui_elements[elem].text_pos[1]+7), (self.ui_elements[elem].text_pos[0],self.ui_elements[elem].text_pos[1]+7), 1)


    def render_assets(self) -> None:
        if self.current_folder and len(self.assets[self.current_folder]) > 0:
            assets = self.assets[self.current_folder]
            pos = [6,6]
            offset = 6

            for asset in assets.values():
                asset_w = asset[0].get_width()
                asset_h = asset[0].get_height()
                
                if pos[0] + asset_w + offset > self.asset_surface_size[0]:
                    pos[0] = 6
                    pos[1] += asset_h + offset

                asset[1].topleft = pos
                self.asset_surface.blit(asset[0], pos)
                pos[0] += asset_w + offset

        #pg.draw.line(self.asset_surface, COLOURS['white'], (6,self.asset_surface_size[1]-24), (self.asset_surface_size[0]-6,self.asset_surface_size[1]-24), 1)
        pg.draw.rect(self.asset_surface, COLOURS['white'], (3,self.asset_surface_size[1]-19, 16, 16), 1)
        pg.draw.rect(self.asset_surface, COLOURS['white'], (self.asset_surface_size[0]-19,self.asset_surface_size[1]-19, 16, 16), 1)
        self.asset_manager_surface.blit(self.asset_surface, self.asset_surf_blit_pos)