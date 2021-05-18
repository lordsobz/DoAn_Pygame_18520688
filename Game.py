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
			img_right =  pygame.transform.scale(img_right,  (60, 70))
			self.images_right.append(img_right)
			img_left = pygame.image.load(f'img/Char_l{i}.png')
			img_left =  pygame.transform.scale(img_left,  (60, 70))
			self.images_left.append(img_left)

		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0

	def update(self):
		dx = 0
		dy = 0
		walk_cooldown = 2

		#Set key
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and self.jumped == False:
			self.vel_y = -20
			self.jumped = True
		if key[pygame.K_UP] == False:
			self.jumped = False
		if key[pygame.K_LEFT]:
			self.direction = -1
			dx -= 6
			self.counter += 1
		if key[pygame.K_RIGHT]:
			self.direction = 1
			dx =+ 6
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

		#Them va cham
		for tile in world.tile_list:
			# #Kiem tra va cham ngang
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			#kiem tra va cham doc
			if tile[1].colliderect(self.rect.x, self.rect.y +dy, self.width, self.height):
				#Check block cham dau khi nhay
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y =0
				
				#Check cham dat khi nguoi choi roi xuong
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0

		#Cap nhat vi tri moi cua nhan vat
		self.rect.x += dx
		self.rect.y += dy

		if self.rect.bottom > Height:
			self.rect.bottom = Height
			dy = 0

		#Cap nhat nhan vat len man hinh
		screen.blit(self.image, self.rect)
	
class World():
	def __init__(self, data):
		self.tile_list = []

		#Xuat hinh anh ra man hinh
		dirt= pygame.image.load('img/dirt.png')
		block = pygame.image.load('img/block.png')
		 
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
				if tile == 2:
					img = pygame.transform.scale(block, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					Goomba = Enemy(col_count * tile_size, row_count * tile_size + 22)
					Goomba_group.add(Goomba)
				col_count += 1 
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/Goomba1.png')
		self.image = pygame.transform.scale(self.image,  (50, 50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.direction = 1
		self.move_counter = 0
		
		# self.images_enemy = []
		# for step in range(1,3):
		# 	img_enemy = pygame.image.load(f'img/Goomba{step}.png')
		# 	img_enemy = pygame.transform.scale(img_enemy,  (40, 40))
		# 	self.images_enemy.append(img_enemy)
		# self.rect = self.images_enemy.get_rect()

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1 
		if abs(self.move_counter) > 50:
			self.direction *= -1
			self.move_counter *= -1



world_data = [
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2],
[2, 0, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2],
[2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
[2, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 1, 1, 2],
[1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1]
]


player = Player(100, Height - 170)

Goomba_group = pygame.sprite.Group()

world = World(world_data)

#Giu cho window game luon mo cho den khi tat
run = True
while run == True:
	
	clock.tick(FPS) #Gioi han Frame rate

	screen.blit(bg_img, (0, 0)) #Import background len window

	world.draw()

	Goomba_group.draw(screen)
	Goomba_group.update()

	player.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()

pygame.quit()