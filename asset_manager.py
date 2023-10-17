import pygame as pg
from const import COLOURS
from ui_elements import *
from utils import load_images
import os

class EditorAssetManager:
    def __init__(self, surface_size, blit_off_y, font) -> None:
        # main surface variables
        self.surface_size = surface_size
        self.asset_manager_surface = pg.Surface(surface_size).convert()
        self.blit_pos = (0, blit_off_y)

        # asset surface variables
        self.asset_surf_y = (len([folder for folder in os.listdir('assets/editor assets/')])*13) + 3
        self.asset_surface_size = (self.surface_size[0]-12, self.surface_size[1]-20-self.asset_surf_y)
        self.asset_surface = pg.Surface(self.asset_surface_size).convert()
        self.asset_surf_blit_pos = (6, self.asset_surf_y+3)

        # general variables
        self.mouse_pos = None
        self.font = font
        self.current_page = 1
        self.current_folder = None
        self.current_asset = None
        self.current_asset_outline = None

        # general elements
        self.ui_icons = load_images('assets/icons/asset manager/')
        self.assets = {}
        self.ui_elements = {}
        self.init_assets()
        self.init_ui_elements()

    def init_assets(self) -> None:
        # load asset images
        page_count = 1
        asset_folder = {}
        asset_folder_pages = {}
        asset_folder_page = {}
        cur_pos = [6,6]
        offset = 6

        for folder in os.listdir('assets/editor assets/'):
            folder_path = 'assets/editor assets/' + folder + '/'
            asset_folder[folder] = load_images(folder_path)
            self.assets[folder] = {}

            for asset in asset_folder[folder]:
                asset_w = asset_folder[folder][asset][0].get_width()
                asset_h = asset_folder[folder][asset][0].get_height()

                if cur_pos[0] + asset_w + offset > self.asset_surface_size[0]:
                    cur_pos[0] = 6
                    cur_pos[1] += asset_h + offset

                if cur_pos[1] + asset_h + offset > self.asset_surface_size[1]:
                    cur_pos = [6,6]
                    asset_folder_pages['page ' + str(page_count)] = asset_folder_page
                    asset_folder_page = {}
                    page_count += 1

                asset_folder_page[asset] = asset_folder[folder][asset]
                asset_folder_page[asset][1].topleft = cur_pos
                cur_pos[0] += asset_w + offset

            asset_folder_pages['page ' + str(page_count)] = asset_folder_page
            self.assets[folder] = asset_folder_pages
            asset_folder_pages = {}
            asset_folder_page = {}
            page_count = 1
            cur_pos = [6,6]

    def init_ui_elements(self) -> None:
        count = 0

        # init folder selection buttons
        for folder in self.assets:
            self.ui_elements[folder] = TextButton((5*len(folder), 13), (12,3+(count*13)), self.asset_manager_surface, folder, self.font)
            count += 1

        # init page change buttons
        self.ui_elements['left arrow'] = ImageButton((15,15), (21, self.surface_size[1]-16), self.asset_manager_surface, self.ui_icons['left arrow'], self.ui_icons['left arrow hover'])
        self.ui_elements['right arrow'] = ImageButton((15,15), (self.surface_size[0]-15-21, self.surface_size[1]-16), self.asset_manager_surface, self.ui_icons['right arrow'], self.ui_icons['right arrow hover'])

    def update(self, mouse_data) -> None:
        # wipe surface for next frame
        self.asset_manager_surface.fill(COLOURS['gray 2'])
        self.asset_surface.fill(COLOURS['gray 3'])

        # update ui interactions
        self.update_ui(mouse_data)

        # update asset interactions
        self.update_assets(mouse_data)
        
    def update_ui(self, mouse_data) -> None:
        # update mouse position relative to asset manager surface
        mouse_pos = (mouse_data['pos'][0], mouse_data['pos'][1]-self.blit_pos[1])

        # handle ui element interaction
        for elem in self.ui_elements:
            if mouse_data['pos'][0] > self.surface_size[0] or mouse_data['pos'][1] < self.blit_pos[1]:
                self.ui_elements[elem].hovering = 0
                return

            # handle collision between button and mouse
            if not self.ui_elements[elem].button_rect.collidepoint(mouse_pos):
                self.ui_elements[elem].hovering = 0
                continue

            # handle ui hover indication
            self.ui_elements[elem].hovering = 1

            # handle ui selectiion indication
            if not mouse_data['l_click']:
                continue

            # handle folder selection
            if self.ui_elements[elem].type == 'text button':
                if not self.current_folder:
                    self.current_folder = elem
                    self.ui_elements[elem].selected = 1
                    continue

                if self.current_folder and self.current_folder == elem:
                    self.ui_elements[self.current_folder].selected = 0
                    self.current_folder = None
                    self.current_page = 1
                    continue

                if self.current_folder and self.current_folder != elem:
                    self.ui_elements[self.current_folder].selected = 0
                    self.current_folder = elem
                    self.current_page = 1
                    self.ui_elements[elem].selected = 1
                    continue

            # handle page change
            if self.current_folder and self.ui_elements[elem].type == 'image button':
                if elem == 'left arrow' and self.current_page > 1:
                    self.current_page -= 1
                    continue

                if elem == 'right arrow' and self.current_page < len(self.assets[self.current_folder]):
                    self.current_page += 1
                    continue

    def update_assets(self, mouse_data) -> None:
        mouse_pos = (mouse_data['pos'][0]-self.asset_surf_blit_pos[0], mouse_data['pos'][1]-self.blit_pos[1]-self.asset_surf_blit_pos[1])
        
        if not self.current_folder:
            return
        
        for name, asset in self.assets[self.current_folder]['page ' + str(self.current_page)].items():
            # check for asset collision
            if not asset[1].collidepoint(mouse_pos):
                asset[0].set_alpha(255)
                continue

            # lower opacity when hovering over asset
            asset[0].set_alpha(55)

            # handle asset selection indication
            if not mouse_data['l_click']:
                continue

            # handle asset selection
            if not self.current_asset:
                self.current_asset = [name, asset]
                self.current_asset_outline = pg.mask.from_surface(asset[0]).outline()
                self.current_asset_outline = [(self.current_asset_outline[i][0]+self.current_asset[1][1].topleft[0],
                                               self.current_asset_outline[i][1]+self.current_asset[1][1].topleft[1]) 
                                               for i in range(len(self.current_asset_outline))]
                continue

            if self.current_asset and self.current_asset[0] == name:
                self.current_asset = None
                self.current_asset_outline = None
                continue

            if self.current_asset and self.current_asset[0] != name:
                self.current_asset = [name, asset]
                self.current_asset_outline = pg.mask.from_surface(asset[0]).outline()
                self.current_asset_outline = [(self.current_asset_outline[i][0]+self.current_asset[1][1].topleft[0],
                                               self.current_asset_outline[i][1]+self.current_asset[1][1].topleft[1])
                                               for i in range(len(self.current_asset_outline))]
                continue

    def render(self, surface) -> None:
        self.render_ui_elements()
        self.render_assets()
        surface.blit(self.asset_manager_surface, self.blit_pos)

    def render_ui_elements(self) -> None:
        # render folder selection buttons
        pg.draw.line(self.asset_manager_surface, COLOURS['blue 3'], (6,3), (6,self.asset_surf_blit_pos[1]-9), 1)

        for elem in self.ui_elements:
            if self.ui_elements[elem].type == 'text button':
                self.ui_elements[elem].render()

                if self.ui_elements[elem].selected:
                    pg.draw.line(self.asset_manager_surface, COLOURS['red 2'], (6,3), (6,self.ui_elements[elem].text_pos[1]+7), 1)
                    pg.draw.line(self.asset_manager_surface, COLOURS['red 2'], (6,self.ui_elements[elem].text_pos[1]+7), (self.ui_elements[elem].text_pos[0],self.ui_elements[elem].text_pos[1]+7), 1)
                else:
                    pg.draw.line(self.asset_manager_surface, COLOURS['blue 3'], (6,self.ui_elements[elem].text_pos[1]+7), (self.ui_elements[elem].text_pos[0],self.ui_elements[elem].text_pos[1]+7), 1)

        # render current asset folder page number and page change buttons
        if self.current_folder:
            # render current page text
            text = 'page ' + str(self.current_page) + '/' + str(len(self.assets[self.current_folder]))
            text_center = self.font.get_center(text)
            self.font.write(self.asset_manager_surface, text, pos=[(self.surface_size[0]/2)-text_center[0], self.surface_size[1]-14], shadow=1)

            # render page change buttons
            self.ui_elements['left arrow'].render()
            self.ui_elements['right arrow'].render()
        else:
            text = 'select a folder'
            text_center = self.font.get_center(text)
            self.font.write(self.asset_manager_surface, text, pos=[self.surface_size[0]/2-text_center[0], self.surface_size[1]-14], shadow=1)

    def render_assets(self) -> None:
        if self.current_folder and len(self.assets[self.current_folder]) > 0:
            assets = self.assets[self.current_folder]['page ' + str(self.current_page)]

            for asset in assets.values():
                self.asset_surface.blit(asset[0], asset[1].topleft)

            if self.current_asset and self.current_asset[0] in assets:      
                pg.draw.lines(self.asset_surface, COLOURS['white'], 1, self.current_asset_outline, 1)
    
        self.asset_manager_surface.blit(self.asset_surface, self.asset_surf_blit_pos)

    def get_data(self) -> dict:
        return {
                'current asset': self.current_asset
               }