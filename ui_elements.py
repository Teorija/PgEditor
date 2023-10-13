from const import COLOURS
import pygame as pg

class PgUiElement:
    def __init__(self, size, pos, surface) -> None:
        self.size = size
        self.pos = pos
        self.surface = surface

    def update(self) -> None:
        pass

    def render(self) -> None:
        pass

class TextButton(PgUiElement):
    def __init__(self, size, pos, surface, text, font) -> None:
        super().__init__(size, pos, surface)
        self.button_surface = pg.Surface(size).convert()
        self.button_surface.fill(COLOURS['transparent black'])
        self.button_surface.set_colorkey(COLOURS['transparent black'])
        self.button_rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.text_pos = pos
        self.font = font
        self.selected = 0
        self.hovering = 0
    
    def render(self) -> None:
        self.text_pos = self.pos

        if self.hovering:
            self.text_pos = (self.pos[0]+3, self.pos[1])

        if self.selected:
            self.text_pos = (self.pos[0]+9, self.pos[1])

        self.font.write(self.button_surface, self.text, pos=[2,2], shadow=1) 
        self.surface.blit(self.button_surface, self.text_pos)

class ImageButton(PgUiElement):
    def __init__(self, size, pos, surface) -> None:
        super().__init__(size, pos, surface)

    def render(self) -> None:
        pass