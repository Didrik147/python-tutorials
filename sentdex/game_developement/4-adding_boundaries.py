import pygame


pygame.init()

display_width = 800
display_height = 600
SIZE = (display_width, display_height)

#RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


gameDisplay = pygame.display.set_mode(SIZE)
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar_V2.png')

sf = 2.5
new_w = int(carImg.get_rect().size[0]/sf)
new_h = int(carImg.get_rect().size[1]/sf)
carImg = pygame.transform.scale(carImg, (new_w, new_h))

car_width = carImg.get_rect().size[0]


def car(x,y):
	gameDisplay.blit(carImg, (x,y))



def game_loop():
	x = (display_width * 0.45)
	y = (display_height * 0.8)

	x_change = 0

	k_right = False
	k_left = False

	gameExit = False

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True	


			# From comments; this one works
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					k_left = True
				elif event.key == pygame.K_RIGHT:
					k_right = True
					
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
		car(x,y)
		
		if x > display_width - car_width or x < 0:
			gameExit = True
		
		
		pygame.display.update()
		FPS = 60
		clock.tick(FPS)





game_loop()

pygame.quit()
quit()
