from utils import load_images
import pygame as pg
from const import COLOURS

class PxFont:
    def __init__(self) -> None:
        self.font_images = load_images('assets/font/')
        self.font = {}
        self.init_special_chars()
        self.font_shadow = {}
        self.init_alphabet_shadow()
    
    def init_special_chars(self):
        for char in self.font_images:
            if char == 'space':
                self.font[' '] = self.font_images[char]
            elif char == 'semicolon':
                self.font[':'] = self.font_images[char]
            elif char == 'decimal':
                self.font['.'] = self.font_images[char]
            elif char == 'pipe':
                self.font['|'] = self.font_images[char]
            else:
                self.font[char] = self.font_images[char]

    def init_alphabet_shadow(self):
        for char, img in self.font.items():
            char_w = img[0].get_width()
            char_h = img[0].get_height()
            char_shadow = [img[0].copy(), img[1].copy()]

            for row in range(char_w):
                for col in range(char_h):
                    if char_shadow[0].get_at((row,col)) == COLOURS['white']:
                        char_shadow[0].set_at((row,col), COLOURS['black'])
            
            self.font_shadow[char] = char_shadow

    def write(self, surface, passage, pos=[0,0], x_off=1, y_off=1, shadow=0):
        pos_copy = pos.copy()

        for i in range(len(passage)):
            char = self.font[passage[i].lower()][0]
            char_w = char.get_width()
            char_h = char.get_height()

            if pos_copy[0] + char_w + x_off >= surface.get_width():
                pos_copy[0] = pos[0]
                pos_copy[1] += char_h + y_off
            
            if shadow:
                char_shadow = self.font_shadow[passage[i].lower()][0]
                surface.blit(char_shadow, (pos_copy[0]+1, pos_copy[1]+1))
                surface.blit(char, pos_copy)
            else:
                surface.blit(char, pos_copy)
            
            pos_copy[0] += char_w + x_off