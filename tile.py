import pygame as pg

class Tile:
    def __init__(self, type, position, name, image, size) -> None:
        self.tile_type = type
        self.pos = position
        self.name = name
        self.image = image
        self.size = size

    def get_type(self) -> str:
        return self.tile_type
    
    def get_pos(self) -> tuple[int, int]:
        return (self.pos[0]*self.size, self.pos[1]*self.size)
    
    def get_image(self) -> pg.Surface:
        return self.image
    
    def get_name(self) -> str:
        return self.name