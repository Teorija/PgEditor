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

        self.editor_version_text = 'pygame map editor v1.0'
        self.editor_version_text_center = self.font.get_center(self.editor_version_text)

        self.map_name = 'untitled map'
        self.map_name_text = 'map name : ' + self.map_name
        self.map_name_text_center = self.font.get_center(self.map_name_text)
        
        self.map_size = '40 x 22'
        self.map_size_text = '/ map size : ' + self.map_size
        
        self.new_map_status = 0
        self.new_map_surface_blit_pos = (self.ui_elements['new map'].button_rect.bottomright[0]+15, self.ui_elements['new map'].button_rect.bottomright[1]+15)
        self.new_map_surface = pg.Surface((150, 60)).convert()
        self.new_map_ui_elements = {}
        self.new_map_ui_elements['create'] = ImageButton((30, 15), (self.new_map_surface.get_width()/2-15, self.new_map_surface.get_height()-19), self.new_map_surface, self.ui_icons['create'], self.ui_icons['create hover'])
        self.new_map_ui_elements['map name'] = TextEntry((90, 15), (55, 3), self.new_map_surface)
        self.new_map_ui_elements['map size row'] = TextEntry((45, 15), (50, 21), self.new_map_surface)
        self.new_map_ui_elements['map size col'] = TextEntry((45, 15), (100, 21), self.new_map_surface)
        self.saving_status = 0
        self.loading_status = 0
        self.drawing = 0
        self.erasing = 0
        self.grid_status = 0
        self.drag_status = 0
        self.reset_status = 0
        self.clear_status = 0
        self.current_zoom_scale = 1
        self.new_layer_status = 0
        self.delete_layer_status = 0
        self.current_layer = 0
        self.layer_count = 0
        self.current_tool = 'none'

    def init_ui_elements(self) -> None:
        button_size = (15, 15)
        off_x = 6
        y_pos = (self.surface_size[1]/2) - button_size[1]/2
        
        self.ui_elements['new map'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*15, y_pos), self.toolbar_surface, self.ui_icons['new map'], self.ui_icons['new map hover'], self.ui_icons['new map selected'])
        self.ui_elements['load map'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*14, y_pos), self.toolbar_surface, self.ui_icons['load'], self.ui_icons['load hover'])
        self.ui_elements['save map'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*13, y_pos), self.toolbar_surface, self.ui_icons['save'], self.ui_icons['save hover'])
        self.ui_elements['draw'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*12, y_pos), self.toolbar_surface, self.ui_icons['draw'], self.ui_icons['draw hover'], self.ui_icons['draw selected'])
        self.ui_elements['erase'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*11, y_pos), self.toolbar_surface, self.ui_icons['erase'], self.ui_icons['erase hover'], self.ui_icons['erase selected'])
        self.ui_elements['clear'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*10, y_pos), self.toolbar_surface, self.ui_icons['clear'], self.ui_icons['clear hover'])
        self.ui_elements['grid'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*9, y_pos), self.toolbar_surface, self.ui_icons['grid'], self.ui_icons['grid hover'], self.ui_icons['grid selected'])
        self.ui_elements['reset'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*8, y_pos), self.toolbar_surface, self.ui_icons['reset'], self.ui_icons['reset hover'])
        self.ui_elements['drag'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*7, y_pos), self.toolbar_surface, self.ui_icons['drag'], self.ui_icons['drag hover'], self.ui_icons['drag selected'])
        self.ui_elements['zoom in'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*6, y_pos), self.toolbar_surface, self.ui_icons['zoom in'], self.ui_icons['zoom in hover'])
        self.ui_elements['zoom out'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*5, y_pos), self.toolbar_surface, self.ui_icons['zoom out'], self.ui_icons['zoom out hover'])
        self.ui_elements['add layer'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*4, y_pos), self.toolbar_surface, self.ui_icons['add layer'], self.ui_icons['add layer hover'])
        self.ui_elements['delete layer'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*3, y_pos), self.toolbar_surface, self.ui_icons['delete layer'], self.ui_icons['delete layer hover'])
        self.ui_elements['layer down'] = ImageButton(button_size, (self.surface_size[0]-(button_size[0]+off_x)*2, y_pos), self.toolbar_surface, self.ui_icons['layer down'], self.ui_icons['layer down hover'])
        self.ui_elements['layer up'] = ImageButton(button_size, (self.surface_size[0]-button_size[0]-off_x, y_pos), self.toolbar_surface, self.ui_icons['layer up'], self.ui_icons['layer up hover'])

    def update(self, mouse_data, keyboard_data) -> None:
        self.toolbar_surface.fill(COLOURS['gray'])
        self.new_map_surface.fill(COLOURS['black'])
        self.update_toolbar_ui_elements(mouse_data)
        
        if self.new_map_status:
            self.update_new_map_ui_elements(mouse_data, keyboard_data)

    def update_new_map_ui_elements(self, mouse_data, keyboard_data) -> None:
        mouse_pos = (mouse_data['pos'][0] - self.new_map_surface_blit_pos[0], mouse_data['pos'][1] - self.new_map_surface_blit_pos[1])

        for elem in self.new_map_ui_elements:
            if keyboard_data['special keys']['esc']:
                self.new_map_ui_elements['map name'].selected = 0
                self.new_map_ui_elements['map size row'].selected = 0
                self.new_map_ui_elements['map size col'].selected = 0
                continue

            if not self.new_map_ui_elements[elem].button_rect.collidepoint(mouse_pos):
                self.new_map_ui_elements[elem].hovering = 0
                continue

            self.new_map_ui_elements[elem].hovering = 1

            if not mouse_data['l_click']:
                continue

            if elem == 'map name':
                self.new_map_ui_elements[elem].selected = 1
                self.new_map_ui_elements['map size row'].selected = 0
                self.new_map_ui_elements['map size col'].selected = 0
                continue

            if elem == 'map size row':
                self.new_map_ui_elements[elem].selected = 1
                self.new_map_ui_elements['map name'].selected = 0
                self.new_map_ui_elements['map size col'].selected = 0
                continue

            if elem == 'map size col':
                self.new_map_ui_elements[elem].selected = 1
                self.new_map_ui_elements['map name'].selected = 0
                self.new_map_ui_elements['map size row'].selected = 0
                continue

    def update_toolbar_ui_elements(self, mouse_data) -> None:
        mouse_pos = mouse_data['pos']

        for elem in self.ui_elements:
            if mouse_pos[1] > self.surface_size[1]:
                self.ui_elements[elem].hovering = 0
        
            if not self.ui_elements[elem].button_rect.collidepoint(mouse_pos):
                self.ui_elements[elem].hovering = 0
                continue

            self.ui_elements[elem].hovering = 1
            self.reset_status = 0
            self.clear_status = 0
            self.new_layer_status = 0
            self.delete_layer_status = 0

            if not mouse_data['l_click']:
                continue

            if elem == 'new map' and not self.new_map_status:
                self.new_map_status = 1
                self.ui_elements[elem].selected = 1
            elif elem == 'new map' and self.new_map_status:
                self.new_map_status = 0
                self.ui_elements[elem].selected = 0

            if elem == 'draw' and not self.drawing:
                self.drawing = 1
                self.erasing = 0
                self.ui_elements[elem].selected = 1
                self.ui_elements['erase'].selected = 0
            elif elem == 'draw' and self.drawing:
                self.drawing = 0
                self.ui_elements[elem].selected = 0

            if elem == 'erase' and not self.erasing:
                self.erasing = 1
                self.drawing = 0
                self.ui_elements[elem].selected = 1
                self.ui_elements['draw'].selected = 0
            elif elem == 'erase' and self.erasing:
                self.erasing = 0
                self.ui_elements[elem].selected = 0

            if elem == 'grid' and not self.grid_status:
                self.grid_status = 1
                self.ui_elements[elem].selected = 1
            elif elem == 'grid' and self.grid_status:
                self.grid_status = 0
                self.ui_elements[elem].selected = 0

            if elem == 'reset':
                self.reset_status = 1

            if elem == 'clear':
                self.clear_status = 1
                self.current_layer = 0
                self.layer_count = 0

            if elem == 'drag' and not self.drag_status:
                self.drag_status = 1
                self.ui_elements[elem].selected = 1
            elif elem == 'drag' and self.drag_status:
                self.drag_status = 0
                self.ui_elements[elem].selected = 0

            if elem == 'zoom in':
                self.current_zoom_scale += 0.1

            if elem == 'zoom out' and self.current_zoom_scale > 0.1:
                self.current_zoom_scale -= 0.1

            if elem == 'add layer':
                self.layer_count += 1
                self.current_layer = self.layer_count
                self.new_layer_status = 1

            if elem == 'delete layer' and self.layer_count > 0 and self.current_layer > 0:
                self.layer_count -= 1
                self.current_layer -= 1
                self.delete_layer_status = 1

            if elem == 'layer down' and self.current_layer > 0:
                self.current_layer -= 1

            if elem == 'layer up' and self.current_layer < self.layer_count:
                self.current_layer += 1

    def render(self, surface) -> None:
        self.render_ui_elements()
        surface.blit(self.toolbar_surface, (0,0))
        self.render_new_map_popup(surface)

    def render_ui_elements(self) -> None:
        self.font.write(self.toolbar_surface, self.editor_version_text, [6, 1], shadow=1)
        self.font.write(self.toolbar_surface, self.map_name_text, [6, self.editor_version_text_center[1]*2 + 1], shadow=1)
        self.font.write(self.toolbar_surface, self.map_size_text, [self.map_name_text_center[0]*2 + 12, self.map_name_text_center[1]*2 + 1], shadow=1)

        for elem in self.ui_elements:
            self.ui_elements[elem].render()

    def render_new_map_popup(self, surface) -> None:
        if self.new_map_status:
                start_pos = self.ui_elements['new map'].button_rect.bottomright
                pg.draw.line(surface, COLOURS['black'], start_pos, (start_pos[0]+15, start_pos[1]+15), width=3)
                self.font.write(self.new_map_surface, 'map name : ', [6,6], shadow=1)
                self.font.write(self.new_map_surface, 'map size : ', [6,24], shadow=1)
                
                for elem in self.new_map_ui_elements:
                    self.new_map_ui_elements[elem].render()

                surface.blit(self.new_map_surface, self.new_map_surface_blit_pos)

    def get_data(self) -> dict:
        return {
                'drawing' : self.drawing,
                'erasing' : self.erasing,
                'drag state' : self.drag_status,
                'grid status' : self.grid_status,
                'zoom scale' : self.current_zoom_scale,
                'reset status' : self.reset_status,
                'clear status' : self.clear_status,
                'new layer status' : self.new_layer_status,
                'delete layer status' : self.delete_layer_status,
                'current layer': self.current_layer,
                'layer count': self.layer_count
               }