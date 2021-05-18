import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock() 
FPS = 120
Width = 1600
Height = 900


#Tao man hinh window game
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('18520688_Platformer_Game')

tile_size = 70

#import hinh anh
bg_img = pygame.image.load('img/background.png')

class Player():
	def __init__(self, x, y):
		self.images_right = []
		self.images_left  = []
		self.index = 0
		self.counter = 0
		for i in range(1,5):
			img_right = pygame.image.load(f'img/Char_r{i}.png')
			img_right =  pygame.transform.scale(img_right,  (90, 100))
			self.images_right.append(img_right)
			img_left = pygame.image.load(f'img/Char_l{i}.png')
			img_left =  pygame.transform.scale(img_left,  (90, 100))
			self.images_left.append(img_left)

		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.vel_y = 0
		self.jumped = False
		self.direction = 0

	def update(self):
		dx = 0
		dy = 0
		walk_cooldown = 4

		#Set key
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and self.jumped == False:
			self.vel_y = -20
			self.jumped = True
		if key[pygame.K_UP] == False:
			self.jumped = False
		if key[pygame.K_LEFT]:
			self.direction = -1
			dx -= 10
			self.counter += 1
		if key[pygame.K_RIGHT]:
			self.direction = 1
			dx =+ 10
			self.counter += 1
		if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
			self.counter = 0 
			self.index = 0
			if self.direction == 1:
				self.image = self.images_right[self.index]
			if self.direction == -1:
				self.image = self.images_left[self.index]			
			

		#Hoat anh di chuyen
		if self.counter > walk_cooldown:
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images_right):
				self.index = 0
			if self.direction == 1:
				self.image = self.images_right[self.index]	
			if self.direction == -1:
				self.image = self.images_left[self.index]

		#Them trong luc
		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 20
		dy += self.vel_y


		#Cap nhat vi tri moi cua nhan vat
		self.rect.x += dx
		self.rect.y += dy

		if self.rect.bottom > Height:
			self.rect.bottom = Height
			dy = 0

		#Cap nhat nhan vat len man hinh
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (255,255,255), self.rect, 2)
	
class World():
	def __init__(self, data):
		self.tile_list = []

		#Xuat hinh anh ra man hinh
		dirt= pygame.image.load('img/dirt.png')
		 
		row_count = 0
		for row  in data:
			col_count = 0
			for tile in row:
				
				if tile == 1:
					img = pygame.transform.scale(dirt, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				
				col_count += 1 
			row_count += 1
	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


player = Player(50, Height - 170)
world = World(world_data)

#Giu cho window game luon mo cho den khi tat
run = True
while run == True:
	
	clock.tick(FPS)

	screen.blit(bg_img, (0, 0)) #Import background len window

	world.draw()
	player.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()

pygame.quit()