import pygame as pg
from const import COLOURS
from ui_elements import PgUiElement

class EditorToolbar:
    def __init__(self, surface_size) -> None:
        self.surface_size = surface_size
        self.toolbar_surface = pg.Surface(surface_size).convert()
        self.last_frame = None

    def init_ui_elements(self) -> None:
        pass

    def update(self) -> None:
        self.toolbar_surface.fill(COLOURS['gray'])

    def render(self, surface) -> None:
        surface.blit(self.toolbar_surface, (0,0))