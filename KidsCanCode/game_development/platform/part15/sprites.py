# Sprite classes for platform game
import pygame as pg
from settings import *
from random import choice, randrange

vec = pg.math.Vector2

# Sprites by Kenney.nl
# https://opengameart.org/content/jumper-pack

class Spritesheet:
    # Utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, width, height):
        # Grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        image = pg.transform.scale(image, (width//2, height//2))
        
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        #self.rect.center = (WIDTH//2, HEIGHT//2)
        self.rect.center = (40, HEIGHT-100)
        self.pos = vec(40, HEIGHT-100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191),
                        self.game.spritesheet.get_image(690, 406,120,201)]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
                
        self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
                        self.game.spritesheet.get_image(692, 1458, 120, 207)]

        self.walk_frames_l = []

        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)


    '''
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3 
    '''
    
    # From comment (smoother jump_cut)
    def jump_cut(self):
        if self.jumping and self.vel.y < 0:
            self.vel.y *= 0.5
    

    def jump(self):
        # Jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2

        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    
    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x*PLAYER_FRICTION
        
        # Equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
            
        self.pos += self.vel + 0.5*self.acc

        # Wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width/2:
            self.pos.x = WIDTH + self.rect.width/2

        self.rect.midbottom = self.pos



    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # Show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # Show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [
                self.game.spritesheet.get_image(0, 288, 380, 94), 
                self.game.spritesheet.get_image(213, 1662, 201, 100)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)


class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5


    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()