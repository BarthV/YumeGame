import pygame
import pyscroll
from src.settings import *
from src.support import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group: pyscroll.PyscrollGroup, world_colliders, create_attack, destroy_attack):
		super().__init__(group)

		self.group = group
		self.group.change_layer(self, 40)
		self.sprite_sheet = pygame.image.load('assets/sprites/Male/Male 16-1.png').convert()

		# graphics setup
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.17
		self.animations = {}

		# init sprite
		self.init_animation_table()
		self.image = self.get_image(0,0)
		self.rect = self.image.get_rect(topleft = pos)
		#hitbox
		self.hitbox = self.rect.inflate(0,0)
		self.last_pos = (self.hitbox.x, self.hitbox.y)

		# movement 
		self.direction = pygame.math.Vector2()
		self.speed = 1
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.world_colliders = world_colliders

		# weapon
		# self.create_attack = create_attack
		# self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 200

		# stats
		self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 3}
		self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic' : 10, 'speed': 5}
		self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
		self.health = self.stats['health'] * 0.5
		self.energy = self.stats['energy'] * 0.8
		self.exp = 5000
		self.speed = self.stats['speed']

	def get_image(self, x, y):
		image = pygame.Surface([32, 32]).convert()
		image.set_colorkey([0, 0, 0])
		image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
		return image

	def init_animation_table(self):
		self.animations = {
			'up': [(0,96),(32,96),(64,96),(32,96)],
			'up_idle':[(32,96)],
			'down': [(0,0),(32,0),(64,0),(32,0)],
			'down_idle':[(32,0)],
			'left': [(0,32),(32,32),(64,32),(32,32)],
			'left_idle':[(32,32)],
			'right': [(0,64),(32,64),(64,64),(32,64)],
			'right_idle':[(32,64)],
			'up_attack':[(32,96)],
			'down_attack':[(32,0)],
			'left_attack':[(32,32)],
			'right_attack':[(32,64)]
		}

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			# movement input
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# attack input 
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				print('attack')
				# self.create_attack()

			# magic input 
			if keys[pygame.K_LCTRL]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				print('magic')

			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
					
				self.weapon = list(weapon_data.keys())[self.weapon_index]

	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self,direction):
		if self.hitbox.collidelist(self.world_colliders) != -1:
			x, y = self.last_pos
			self.hitbox.x = x
			self.hitbox.y = y

		if self.hitbox.collidelist(self.group.get_sprites_from_layer(30)) != -1:
			x, y = self.last_pos
			self.hitbox.x = x
			self.hitbox.y = y

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				# self.destroy_attack()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		x, y = animation[int(self.frame_index)]
		self.image = self.get_image(x, y)
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.last_pos = (self.hitbox.x, self.hitbox.y)
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)