import pygame
import time
import random


pygame.init()

display_width = 800
display_height = 600
SIZE = (display_width, display_height)

#RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255)


gameDisplay = pygame.display.set_mode(SIZE)
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar_V2.png')

sf = 2.5
new_w = int(carImg.get_rect().size[0]/sf)
new_h = int(carImg.get_rect().size[1]/sf)
carImg = pygame.transform.scale(carImg, (new_w, new_h))
car_width = carImg.get_rect().size[0]
car_height = carImg.get_rect().size[1]

pause = False

def things_dodged(count):
  font = pygame.font.SysFont(None, 25)
  text = font.render("Dodged: " + str(count), True, BLACK)
  gameDisplay.blit(text, (0,0))


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, 
        [thingx, thingy, thingw, thingh])



def car(x,y):
    gameDisplay.blit(carImg, (x,y))



def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()



def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 72)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(TextSurf, TextRect)
    
    pygame.display.update()
    
    time.sleep(2)
    
    game_loop()



def crash():
    message_display('You Crashed')


def button(msg, x,y,w,h, ic,ac, action=None):
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  #print(click)
  
  
  if x < mouse[0] < x+w and y < mouse[1] < y+h:
    pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
    if click[0] == 1 and action != None:
      action()
  else:
    pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
  
  
  smallText = pygame.font.Font("freesansbold.ttf", 20)
  textSurf, textRect = text_objects(msg, smallText)
  textRect.center = ( (x+(w/2)), (y+(h/2)) )
  gameDisplay.blit(textSurf, textRect)
  

def quitgame():
  pygame.quit()
  quit()


def unpause():
  global pause
  pause = False
  
def paused():
  while pause:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    
    gameDisplay.fill(WHITE)
    largeText = pygame.font.Font('freesansbold.ttf', 72)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(TextSurf, TextRect)
    
    button("Continue!", 150,450,100,50, GREEN,bright_green, unpause)    
    button("Quit", 550,450,100,50, RED,bright_red, quitgame)
    
    
    pygame.display.update()
    clock.tick(15)



def game_intro():
  
  intro = True
  
  while intro:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    
    gameDisplay.fill(WHITE)
    largeText = pygame.font.Font('freesansbold.ttf', 72)
    TextSurf, TextRect = text_objects("A bit Racey", largeText)
    TextRect.center = (display_width/2, display_height/2)
    gameDisplay.blit(TextSurf, TextRect)
    
    button("GO!", 150,450,100,50, GREEN,bright_green, game_loop)    
    button("Quit", 550,450,100,50, RED,bright_red, quitgame)
    
    
    pygame.display.update()
    clock.tick(15)



def game_loop():
    global pause
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    
    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100
    
    dodged = 0
    
    
    
    k_right = False
    k_left = False

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              pygame.quit()
              quit()

            # From comments; this one works
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    k_left = True
                elif event.key == pygame.K_RIGHT:
                    k_right = True
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    k_right = False
                    x_change = 0
                elif event.key == pygame.K_LEFT:
                    k_left = False
                    x_change = 0
            
            if k_left:
                x_change = -5
            if k_right:
                x_change = 5
            if k_right and k_left:
                x_change = 0
            
            
        x += x_change
            
        gameDisplay.fill(WHITE)
        
        things(thing_startx, thing_starty,
                thing_width, thing_height, block_color)
        
        thing_starty += thing_speed
        
        car(x,y)
        
        things_dodged(dodged)
        
        if x > display_width - car_width or x < 0:
            crash()
        
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty + thing_height:
            if x + car_width > thing_startx and \
            x < thing_startx + thing_width:
                crash()
                    
        pygame.display.update()
        FPS = 60
        clock.tick(FPS)



game_intro()

game_loop()

pygame.quit()
quit()
