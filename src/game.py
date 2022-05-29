from tkinter import dialog
import pygame, sys
from src.settings import * 
import src.menus as menus
import src.level as level


class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('YumeGame - Adventure')
		favicon_sfc = pygame.image.load('assets/favicon.png')
		pygame.display.set_icon(favicon_sfc)
		self.clock = pygame.time.Clock()
		self.mainmenu = menus.Menu()
		self.level = level.Level()

	# 	# # sound 
	# 	# main_sound = pygame.mixer.Sound('../audio/main.ogg')
	# 	# main_sound.set_volume(0.w5)
	# 	# main_sound.play(loops = -1)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.level.toggle_menu()
					if event.key == pygame.K_p:
						self.level.paused = not self.level.paused
					if event.key == pygame.K_e:
						self.level.interact_with_world()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			# self.mainmenu.display()
			pygame.display.update()
			self.clock.tick(FPS)
