import pygame
from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16 , 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock() 
FPS = 60

Width = 1600
Height = 900


#Tao man hinh window game
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('18520688_Platformer_Game')

font = pygame.font.SysFont('Bauhaus 93',70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

tile_size = 50
game_over = 0
game_menu = True
score = 0

white = (255,255,255)
blue = (0,0,255)

#import hinh anh
bg_img = pygame.image.load('img/background.jpg')
restart_img = pygame.image.load('img/restart_img.png')
restart_img = pygame.transform.scale(restart_img, (150, 70))
exit_img = pygame.image.load('img/exit_img.png')
exit_img = pygame.transform.scale(exit_img, (150, 70))

#import sound effect
pygame.mixer.music.load('img/mario_theme.wav')
pygame.mixer.music.play(-1 , 0.0, 5000)
pygame.mixer.music.set_volume(0.2)
coin_fx = pygame.mixer.Sound('img/coin_fx.mp3')
coin_fx.set_volume(0.03)
jump_fx = pygame.mixer.Sound('img/mario_jump.wav')
jump_fx.set_volume(0.05)
die_fx = pygame.mixer.Sound('img/mario_dies.wav')
die_fx.set_volume(0.2)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset():
	player.reset(100, Height - 170)
	Goomba_group.empty()
	Lava_Group.empty()
	Coin_Group.empty()
	Coin_Group.add(score_coin)
	world = World(world_data)
	return world

class Button():
	def __init__(self, x, y ,image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False
	
	def draw(self):
		action = False

		#xac dinh con tro chuot
		pos = pygame.mouse.get_pos()

		#Check clicked 
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		#Giao dien nut bam
		screen.blit(self.image, self.rect)

		return action

class Player():
	def __init__(self, x, y):
		self.reset(x,y)

	def update(self,game_over):
		dx = 0
		dy = 0
		walk_cooldown = 4
		
		if game_over == 0:

			#Set key
			key = pygame.key.get_pressed()
			if key[pygame.K_q]:
				pygame.quit()
			if key[pygame.K_r]:
				reset()	
				score = 0 		
			if key[pygame.K_UP] and self.jumped == False and self.floating == False:
				jump_fx.play()
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
			self.floating = True
			for tile in world.tile_list:
				# #Kiem tra va cham ngang
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#kiem tra va cham doc
				if tile[1].colliderect(self.rect.x, self.rect.y +dy, self.width, self.height):
					#Check block cham dau khi nhay
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					
					#Check cham dat khi nguoi choi roi xuong
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.floating = False


			#Check va cham voi chuong ngai vat
			if pygame.sprite.spritecollide(self, Goomba_group, False):
				game_over = -1
				die_fx.play()
				pygame.mixer.music.stop()			
			if pygame.sprite.spritecollide(self, Lava_Group, False):
				game_over = -1
				die_fx.play()
				pygame.mixer.music.stop()

			#Check da cham vao ngoi sao
			if pygame.sprite.spritecollide(self, Star_Group, True):
				game_over = 1
				pygame.mixer.music.stop()

			#Cap nhat vi tri moi cua nhan vat
			self.rect.x += dx
			self.rect.y += dy
			
		#Check da chet
		elif game_over == -1:
			self.image = self.dead_image	
			draw_text('GAME OVER!', font, blue, Width//2 - 150, Height//2 - 100)		
			if self.rect.y > 750:
				self.rect.y -= 5
				
		#Cap nhat nhan vat len man hinh
		screen.blit(self.image, self.rect)
		pygame.draw.rect(screen, (255,255,255), self, 2)
			
		return game_over

	def reset(self, x, y):
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
		self.dead_image = pygame.image.load('img/game_over.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (60,50))
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.floating = True
	
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
					Goomba = Enemy(col_count * tile_size, row_count * tile_size + 8)
					Goomba_group.add(Goomba)
				if tile == 4:
					lava = Lava(col_count * tile_size, row_count * tile_size)
					Lava_Group.add(lava)
				if tile == 5:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					Coin_Group.add(coin)
				if tile == 6:
					star = Star(col_count * tile_size, row_count * tile_size)
					Star_Group.add(star)
				col_count += 1 
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images_enemy = []
		self.index = 0
		for step in range(1,3):
			self.image = pygame.image.load(f'img/Goomba{step}.png')
			self.image = pygame.transform.scale(self.image,  (50, 45))
			self.images_enemy.append(self.image)
		self.rect = self.image.get_rect()
				
		self.rect.x = x
		self.rect.y = y
		self.hitbox = x // 2
		self.move_direction = 1
		self.move_counter = 0
		self.scounter = 0
		
		

	def update(self):
		move_cooldown = 18
		self.scounter += 1
		if self.scounter > move_cooldown:
			self.scounter = 0
			self.index += 1
		if self.index >= len(self.images_enemy):
			self.index = 0 		
		self.image = self.images_enemy[self.index]

		self.rect.x += self.move_direction
		self.move_counter += 1 
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images_lava = []
		self.index = 0
		for lava in range(1,3):
			self.image = pygame.image.load(f'img/lava{lava}.png')
			self.image = pygame.transform.scale(self.image,  (tile_size, tile_size))
			self.images_lava.append(self.image)

		self.rect = self.image.get_rect()				
		self.rect.x = x
		self.rect.y = y
		self.lcounter = 0
		
		

	def update(self):
		lava_cooldown = 18
		self.lcounter += 1
		if self.lcounter > lava_cooldown:
			self.scounter = 0
			self.index += 1
		if self.index >= len(self.images_lava):
			self.index = 0 		
		self.image = self.images_lava[self.index]

class Star(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/star.png')
		self.image = pygame.transform.scale(img,  (tile_size , tile_size))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img,  (tile_size//2 , tile_size//2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

world_data = [
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 5, 5, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 6, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 1, 1, 1, 2],
[2, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 2],
[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 2],
[2, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 1, 1, 2],
[2, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 1, 1, 1, 2],
[2, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 5, 3, 5, 0, 0, 0, 1, 1, 1, 1, 2],
[1, 1, 1, 1, 1, 1, 1, 2, 4, 4, 4, 4, 4, 4, 4, 4, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

#Khai bao cac bien
player = Player(100, Height - 170)

Goomba_group = pygame.sprite.Group()
Coin_Group   = pygame.sprite.Group()
Lava_Group   = pygame.sprite.Group()
Star_Group   = pygame.sprite.Group()

score_coin = Coin(tile_size //2, tile_size //2)
Coin_Group.add(score_coin)

world = World(world_data)

restart_button = Button(Width//2 - 40, Height//2, restart_img)
exit_button	   = Button(Width//2 - 40, Height//2 + 70, exit_img)


#Giu cho window game luon mo cho den khi tat
run = True
while run == True:
	
	clock.tick(FPS) #Gioi han Frame rate

	screen.blit(bg_img, (5, 0)) #Import background len window
	
	if game_menu == True:
		if restart_button.draw():
			game_menu = False
		if exit_button.draw():
			run = False
	else:
		world.draw()


		if game_over == 0: #Trong luc game chay, Goomba se di chuyen
			Goomba_group.update()

			#Cap nhat diem
			#Check nhat coin
			if pygame.sprite.spritecollide(player, Coin_Group, True):
				score +=1
				coin_fx.play()
			draw_text('x' +str(score), font_score, white, tile_size -10, 10)
		
		#Draw len man hinh 
		Goomba_group.draw(screen)
		Lava_Group.draw(screen)
		Coin_Group.draw(screen)
		Star_Group.draw(screen)

		game_over = player.update(game_over)

		#check trang thai nguoi choi thi 
		if game_over == -1:	#Chet
			if restart_button.draw():
				world = reset()
				game_over = 0
				score = 0
				pygame.mixer.music.load('img/mario_theme.wav')
				pygame.mixer.music.play(-1 , 0.0, 500)
				pygame.mixer.music.set_volume(0.3)
		if game_over == 1:	#Win
			draw_text('YOU WIN!', font, blue, Width //2 - 110, Height //2 -100)
			if restart_button.draw():
				world = reset()
				game_over = 0
				score = 0
				pygame.mixer.music.load('img/mario_theme.wav')
				pygame.mixer.music.play(-1 , 0.0, 500)
				pygame.mixer.music.set_volume(0.3)
			

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()

pygame.quit()
