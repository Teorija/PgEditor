from const import COLOURS
import pygame as pg
from utils import load_images

# To Do
# improve and update base class for widgets (e.g. add more attributes, methods, etc...)
# extend capability of widget creation (e.g. placing widgets in a grid, placing widgets directionaly, padding, margin, etc...)
# add more widgets (e.g. drop down, check box, etc...)

class PgUiElement:
    def __init__(self, size, pos, surface) -> None:
        self.size = size
        self.pos = pos
        self.surface = surface
        self.selected = 0
        self.hovering = 0

class TextButton(PgUiElement):
    def __init__(self, size, pos, surface, text, font) -> None:
        super().__init__(size, pos, surface)
        self.type = 'text button'
        self.button_surface = pg.Surface(size).convert()
        self.button_surface.fill(COLOURS['transparent black'])
        self.button_surface.set_colorkey(COLOURS['transparent black'])
        self.button_rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.text_pos = pos
        self.font = font
    
    def render(self) -> None:
        self.text_pos = self.pos

        if self.hovering:
            self.text_pos = (self.pos[0]+3, self.pos[1])

        if self.selected:
            self.text_pos = (self.pos[0]+9, self.pos[1])

        self.font.write(self.button_surface, self.text, pos=[2,2], shadow=1) 
        self.surface.blit(self.button_surface, self.text_pos)

class ImageButton(PgUiElement):
    def __init__(self, size, pos, surface, image, hover_image=None, selected_image=None) -> None:
        super().__init__(size, pos, surface)
        self.type = 'image button'
        self.hover_image = hover_image
        self.selected_image = selected_image
        self.button_image = image[0]
        self.button_rect = image[1]
        self.button_rect.topleft = pos
        self.button_pos = pos

    def render(self) -> None:
        if self.hovering and self.hover_image:
            self.surface.blit(self.hover_image[0], self.pos)
            return
        
        if self.selected and self.selected_image:
            self.surface.blit(self.selected_image[0], self.pos)
            return

        self.surface.blit(self.button_image, self.pos)

class TextEntry(PgUiElement):
    def __init__(self, size, pos, surface, limit, restriction, font) -> None:
        super().__init__(size, pos, surface)
        self.type = 'text entry'
        self.button_rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.font = font
        self.restriction = restriction # 0 = no restriction, 1 = numbers only, 2 = letters only, 3 = letters and numbers only
        self.entry_text_limit = limit
        self.entry_text = ''
        self.entry_text_pos = [pos[0]+3, pos[1]+2]
    
    def render(self) -> None:
        self.font.write(self.surface, self.entry_text, pos=self.entry_text_pos, shadow=1)
        pg.draw.rect(self.surface, COLOURS['gray'], self.button_rect, width=1)

        if self.hovering:
            pg.draw.rect(self.surface, COLOURS['blue 3'], self.button_rect, width=1)
            return
        if self.selected:
            pg.draw.rect(self.surface, COLOURS['red 2'], self.button_rect, width=1)
            return

    def update(self, keyboard_data):
        for key in keyboard_data['regular keys']:
            if keyboard_data['regular keys'][key] and key == 'del':
                self.entry_text = self.entry_text[:-1]
                continue

            if keyboard_data['regular keys'][key] and len(self.entry_text) < self.entry_text_limit:
                if self.restriction == 0:
                    self.entry_text += key
                    continue
                if self.restriction == 1 and key.isdigit():
                    self.entry_text += key
                    continue
                if self.restriction == 2 and key.isalpha():
                    self.entry_text += key
                    continue
                if self.restriction == 3 and (key.isalnum() or key == ' '):
                    self.entry_text += key
                    continue
                
    def get_entry(self):
        return self.entry_text
    
    def clear_entry(self):
        self.entry_text = ''

    def reset(self):
        self.clear_entry()
        self.selected = 0
        self.hovering = 0