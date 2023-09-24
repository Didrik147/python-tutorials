"""
Made from the following YouTube playlist by "KidsCanCode":
https://www.youtube.com/watch?v=uWvb3QzA48c&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq
"""

# Jumpy! - Platform game
import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialize game window, etc
        # Initialize pygame and create window
        pg.init()

        # For sound
        pg.mixer.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        # Keeps track of how fast we are running
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # Start a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()


    def run(self):
        # Game Loop
        self.playing = True

        while self.playing:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        

    def events(self):
        # Game Loop - events
        # Process input (events)
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False


    def draw(self):
        # Game Loop - draw
        # Draw / render
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        
        # *after* drawing everything, flip the display
        pg.display.flip()


    def show_start_screen(self):
        # Game splash/start screen
        pass

    def show_go_screen(self):
        # Game over/continue
        pass


g = Game()

g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()


pg.quit()
