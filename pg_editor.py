import pygame as pg
import sys
import time
from const import COLOURS
from mouse import Mouse
from keyboard import EditorKeyboardData
from font import PxFont
from toolbar import EditorToolbar
from asset_manager import EditorAssetManager
from map_manager import EditorMapManager


class PgEditor:
    def __init__(self, screen_size=(1280, 720), canvas_size=(640, 360)) -> None:
        pg.init()
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP])
        pg.display.set_caption("Pygame 2D Pixel Art Map Editor")
        self.screen_size = screen_size
        self.screen = pg.display.set_mode(screen_size)
        self.canvas_size = canvas_size
        self.canvas = pg.Surface(canvas_size).convert()
        self.ratio = (self.screen_size[0]/self.canvas_size[0], self.screen_size[1]/self.canvas_size[1])
        self.running = 1
        
        self.fps = 60
        self.clock = pg.time.Clock()

        self.mouse = Mouse()
        self.keyboard = EditorKeyboardData()
        
        self.font = PxFont()

        self.toolbar_w = self.canvas_size[0]
        self.toolbar_h = self.canvas_size[1]/15
        self.toolbar_size = (self.toolbar_w, self.toolbar_h)
        self.toolbar = EditorToolbar(self.toolbar_size, self.font)

        self.asset_manager_w = self.canvas_size[0]/5
        self.asset_manager_h = self.canvas_size[1]-self.toolbar_h
        self.asset_manager_size = (self.asset_manager_w, self.asset_manager_h)
        self.asset_manager = EditorAssetManager(self.asset_manager_size, self.toolbar_h, self.font)

        self.map_manager_w = self.canvas_size[0]-self.asset_manager_w
        self.map_manager_h = self.canvas_size[1]-self.toolbar_h
        self.map_manager_size = (self.map_manager_w, self.map_manager_h)
        self.map_size = (640, 352)
        self.map_manager = EditorMapManager(self.map_manager_size, self.map_size, self.asset_manager_w, self.toolbar_h, self.font)
    
    def run(self) -> None:
        while self.running:
            self.events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
            time.sleep(1/self.fps)

        pg.quit()
        sys.exit()

    def events(self) -> None:
        # update mouse position
        self.mouse.data['pos'] = (pg.mouse.get_pos()[0]/self.ratio[0], pg.mouse.get_pos()[1]/self.ratio[1])

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = 0

                # handle mouse event
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1: # left click down
                        self.mouse.data['l_click'] = 1
                        self.mouse.data['l_clicking'] = 1
                    if event.button == 3: # right click down
                        self.mouse.data['r_click'] = 1
                        self.mouse.data['r_clicking'] = 1
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1: # left click up
                        self.mouse.data['l_clicking'] = 0
                    if event.button == 3: # right click up
                        self.mouse.data['r_clicking'] = 0

                # handle keyboard event
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.keyboard.data['arrow keys']['left'] = 1
                    if event.key == pg.K_RIGHT:
                        self.keyboard.data['arrow keys']['right'] = 1
                    if event.key == pg.K_UP:
                        self.keyboard.data['arrow keys']['up'] = 1
                    if event.key == pg.K_DOWN:
                        self.keyboard.data['arrow keys']['down'] = 1
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT:
                        self.keyboard.data['arrow keys']['left'] = 0
                    if event.key == pg.K_RIGHT:
                        self.keyboard.data['arrow keys']['right'] = 0
                    if event.key == pg.K_UP:
                        self.keyboard.data['arrow keys']['up'] = 0
                    if event.key == pg.K_DOWN:
                        self.keyboard.data['arrow keys']['down'] = 0

    def update(self) -> None:
        self.canvas.fill(COLOURS['blue 3']) # wipe canvas for new frame
        
        # update objects
        self.toolbar.update(self.mouse.data)
        self.asset_manager.update(self.mouse.data)
        self.map_manager.update(self.mouse.data, self.keyboard.data, self.asset_manager.get_data(), self.toolbar.get_data())
        self.mouse.reset_click_status()

    def render(self) -> None:
        # render objects
        # render stack - bottom
        self.map_manager.render(self.canvas)
        self.asset_manager.render(self.canvas)
        self.toolbar.render(self.canvas)
        # render stack - top

        # blit canvas to screen and update display
        self.screen.blit(pg.transform.scale(self.canvas, self.screen_size), (0,0))
        pg.display.update()