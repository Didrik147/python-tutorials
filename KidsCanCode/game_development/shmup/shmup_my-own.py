"""
Made from the following YouTube playlist by "KidsCanCode":
https://www.youtube.com/watch?v=VO8rTszcW4s&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=1
"""

# Shmup game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
import pygame
import random
from os import path

'''
Art from Kenney.nl
https://opengameart.org/content/space-shooter-redux
'''
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')


# Constants
WIDTH = 480
HEIGHT = 600

# Frames per second
FPS = 60

POWERUP_TIME = 5000  # ms

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")

# For sound
pygame.mixer.init()

# Keeps track of how fast we are running
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

# Function for drawing text on the screen


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Function that creates a new mob
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


# Function for making shield bar
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 10

    fill = (pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

    fill_color = GREEN

    # Change color based on percentage left
    if 20 < pct < 50:
        fill_color = YELLOW
    elif pct <= 20:
        fill_color = RED

    pygame.draw.rect(surf, fill_color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img, img_rect)


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((50,40))
        #self.image.fill(GREEN)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        # Timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # Unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH//2
            self.rect.bottom = HEIGHT-10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # Hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH//2, HEIGHT+200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(RED)
        #self.image_orig = meteor_img
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)

        self.image = self.image_orig.copy()

        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT + 10 or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(1, 8)


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        boss_img = pygame.image.load(
            path.join(img_dir, 'enemyBlack2.png')).convert()
        #self.image = pygame.transform.scale(boss_img, (50, 38))
        self.image = boss_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        self.shield = 100
        
        self.rect.width -= 20
        self.rect.x += 10
        self.rect.height -= 20
        self.rect.y += 10
        
        #pygame.draw.rect(self.image, RED, self.rect)
        
        self.rect.centerx = WIDTH//2
        self.rect.top = 50
        
        
        self.speedx = 3
        self.speedy = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        
        self.shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
        self.shoot_sound.set_volume(0.25)
        
    def update(self):
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speedx *= -1
            self.speedy = random.randint(-2,2)
            
            #print(self.speedy)
            
        if self.rect.top <= 0:
            self.speedy *= -1
            
        if self.rect.bottom > 3*HEIGHT//4:
            self.speedy *= -1
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        now = pygame.time.get_ticks()
        
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot()
            self.shoot_delay = random.randint(200,2000)
        
    def shoot(self):
            enemyBullet = EnemyBullet(self.rect.centerx+10, self.rect.bottom)
            all_sprites.add(enemyBullet)
            enemyBullets.add(enemyBullet)
            
            self.shoot_sound.play()
    
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((10,20))
        #self.image.fill(YELLOW)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

        self.speedy = -10
        

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'laserBlue13.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x

        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()



class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


shipColor = "green"

def show_go_screen():
    global shipColor
    screen.blit(background, background_rect)
    draw_text(screen, 'SHMUP!', 64, WIDTH//2, HEIGHT//4)
    draw_text(screen, 'Arrow keys move, Space to fire', 22, WIDTH//2, HEIGHT//2)

    
    
    shipfiles = ["playerShip1_red.png", "playerShip1_green.png", "playerShip1_blue.png"]
    letters = ["R", "G", "B"]
    ships = []
    p = 0.25
    
    for i in range(len(shipfiles)):
        ship_img = pygame.image.load(
            path.join(img_dir, shipfiles[i])).convert()

        ship = pygame.transform.scale(ship_img, (50, 38))

        ship.set_colorkey(BLACK)
        ship_rect = ship.get_rect()
        
        ship_rect.center = (WIDTH*p,HEIGHT*0.64)
        screen.blit(ship, ship_rect)
        
        draw_text(screen, letters[i], 18, WIDTH*p,HEIGHT*0.7)
        p += 0.25

        
    draw_text(screen, 'Choose a ship by pressing the corresponding key', 18, WIDTH//2, HEIGHT*4//5)

    pygame.display.flip()
    waiting = True

    while waiting:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    #print("Red")
                    shipColor = "red"
                elif event.key == pygame.K_g:
                    #print("Green")
                    shipColor = "green"
                elif event.key == pygame.K_b:
                    #print("Blue")
                    shipColor = "blue"
                    
                waiting = False




# Load all game graphics
# Starfield image from https://i.imgur.com/bHiPMju.png
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()


# Other images from Kenney https://opengameart.org/content/space-shooter-redux
#meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())


explosion_anim = {}

explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []


for i in range(9):
    #filename = 'regularExplosion0{}.png'.format(i)
    filename = f'regularExplosion0{i}.png'

    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)

    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)

    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    filename = f'sonicExplosion0{i}.png'
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)


powerup_images = {}
powerup_images['shield'] = pygame.image.load(
    path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(
    path.join(img_dir, 'bolt_gold.png')).convert()


# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))

# Reduce volume
shoot_sound.set_volume(0.25)
shield_sound.set_volume(0.25)
power_sound.set_volume(0.25)


expl_sounds = []

for snd in ['expl3.wav', 'expl6.wav']:
    #for snd in ['Explosion.wav', 'Explosion2.wav']:
    expl_sound = pygame.mixer.Sound(path.join(snd_dir, snd))
    expl_sound.set_volume(0.25)
    expl_sounds.append(expl_sound)

player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
player_die_sound.set_volume(0.25)

pygame.mixer.music.load(
    path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.15)


pygame.mixer.music.play(loops=-1)

# Game loop
game_over = True

threshold = 200

running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        player_img = pygame.image.load(
            path.join(img_dir, f'playerShip1_{shipColor}.png')).convert()
        player_mini_img = pygame.transform.scale(player_img, (25, 19))
        player_mini_img.set_colorkey(BLACK)

        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemyBullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()


        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()

        score = 0
    
    # keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    if score < threshold:
        # Check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            # From tutorial
            #score += 50 - hit.radius

            # My own
            score += 100//hit.radius

            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)

            # Spawning power ups
            if random.random() > 0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
        
            if score < threshold:
                newmob()
            else:
                for m in mobs:
                    expl = Explosion(m.rect.center, 'lg')
                    all_sprites.add(expl)
                    m.kill()
                
                boss = Boss()
                all_sprites.add(boss)
                mobs.add(boss)
                    
                    


        # check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(
            player, mobs, True, pygame.sprite.collide_circle)

        for hit in hits:
            player.shield -= hit.radius * 2
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            newmob()

            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                #player.kill()
                player.hide()
                player.lives -= 1
                player.shield = 100

        # Check to see if player hit a powerup
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                shield_sound.play()

                if player.shield >= 100:
                    player.shield = 100

            if hit.type == 'gun':
                player.powerup()
                power_sound.play()
        
    
    
    else: # Boss mode
        # Check to see if bullet hits boss
        hits = pygame.sprite.spritecollide(boss, bullets, True)
        
        for hit in hits:
            boss.shield -= 10
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            
            if boss.shield <= 0:
                #print("Boss defeated")
                player_die_sound.play()
                death_explosion = Explosion(boss.rect.center, 'player')
                all_sprites.add(death_explosion)
                boss.kill()
                boss.rect.top = -300
                
                
                
               
        
    
        # Check to see if enemy bullet hits player
        hits = pygame.sprite.spritecollide(player, enemyBullets, True)
        for hit in hits:
            player.shield -= 20
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            
            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                #player.kill()
                player.hide()
                player.lives -= 1
                player.shield = 100
        
    # If the player died and the explosion has finished playing
    #if not player.alive() and not death_explosion.alive():
    if player.lives == 0 and not death_explosion.alive():
        #running = False
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH//2, 10)
    
    if len(mobs) == 0:
        draw_text(screen, "You Won!", 50, WIDTH//2, HEIGHT//2)

    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH-100, 5, player.lives, player_mini_img)
    
    
    
    
    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()
