import pygame as pg
import os

def load_images(path):
    images = {}

    try:
        for file in os.listdir(path):
            img = pg.image.load(path+file).convert_alpha()
            images[file[:-4]] = [img, img.get_rect()]
            images[file[:-4]][0].set_colorkey((0,0,0))

        return images
    except OSError:
        print('invalid path...')