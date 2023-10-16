import pygame as pg
from const import COLOURS
from ui_elements import *
from utils import load_images

class EditorToolbar:
    def __init__(self, surface_size, font) -> None:
        self.surface_size = surface_size
        self.toolbar_surface = pg.Surface(surface_size).convert()
        self.last_frame = None
        self.font = font
        self.ui_icons = load_images('assets/icons/toolbar/')
        self.ui_elements = {}
        self.init_ui_elements()

        self.map_name = 'untitled map'
        self.map_size = '40 x 20'
        self.current_layer = 0
        self.layer_count = 0
        self.current_tool = 'none'

    def init_ui_elements(self) -> None:
        button_size = (15, 15)
        off_x = 6
        y_pos = (self.surface_size[1]/2) - button_size[1]/2
        
        self.ui_elements['cut'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*20, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['copy'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*19, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['paste'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*18, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['change map name'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*17, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['change map size'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*16, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['draw'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*15, y_pos), self.toolbar_surface, self.ui_icons['draw'])
        self.ui_elements['erase'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*14, y_pos), self.toolbar_surface, self.ui_icons['erase'])
        self.ui_elements['fill'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*13, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['clear'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*12, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['drag'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*11, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['select'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*10, y_pos), self.toolbar_surface, self.ui_icons['blank'])
        self.ui_elements['grid'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*9, y_pos), self.toolbar_surface, self.ui_icons['grid'])
        self.ui_elements['save'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*8, y_pos), self.toolbar_surface, self.ui_icons['save'])
        self.ui_elements['load'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*7, y_pos), self.toolbar_surface, self.ui_icons['load'])
        self.ui_elements['undo'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*6, y_pos), self.toolbar_surface, self.ui_icons['undo'])
        self.ui_elements['redo'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*5, y_pos), self.toolbar_surface, self.ui_icons['redo'])
        self.ui_elements['add layer'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*4, y_pos), self.toolbar_surface, self.ui_icons['add layer'])
        self.ui_elements['delete layer'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*3, y_pos), self.toolbar_surface, self.ui_icons['delete layer'])
        self.ui_elements['layer down'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*2, y_pos), self.toolbar_surface, self.ui_icons['layer down'])
        self.ui_elements['layer up'] = ImageButton(button_size, (self.surface_size[0]-button_size[0]-off_x, y_pos), self.toolbar_surface, self.ui_icons['layer up'])

    def update(self) -> None:
        self.toolbar_surface.fill(COLOURS['gray'])
        self.update_ui_elements()

    def update_ui_elements(self) -> None:
        pass

    def render(self, surface) -> None:
        self.render_ui_elements()
        surface.blit(self.toolbar_surface, (0,0))

    def render_ui_elements(self) -> None:
        editor_version_text = 'pygame map editor v1.0'
        editor_version_text_center = self.font.get_center(editor_version_text)
        self.font.write(self.toolbar_surface, editor_version_text, [6, 1], shadow=1)

        map_name_text = 'map name : ' + self.map_name
        map_name_text_center = self.font.get_center(map_name_text)
        self.font.write(self.toolbar_surface, map_name_text, [6, editor_version_text_center[1]*2 + 1], shadow=1)

        map_size_text = '/ map size : ' + self.map_size
        self.font.write(self.toolbar_surface, map_size_text, [map_name_text_center[0]*2 + 12, map_name_text_center[1]*2 + 1], shadow=1)

        for elem in self.ui_elements:
            if not self.ui_elements[elem]:
                continue

            self.ui_elements[elem].render()

    def get_data(self) -> dict:
        return {
            'current tool': None,
            'current layer': None,
            'layer count': None,
        }