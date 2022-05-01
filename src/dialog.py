import pygame
from src.settings import *
from src.quests import *

class Dialogbox:
	def __init__(self, name, quest: int):
		# general
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

		# dialog box setup
		self.name = name
		self.dialog_box_rect = pygame.Rect(300, HEIGTH-(UI_FONT_SIZE*4 + 12), 680, (UI_FONT_SIZE*4 + 12))
		if name in DIALOG_TEXTS:
			if str(quest) in DIALOG_TEXTS[name]['quests']:
				self.dialog_texts = DIALOG_TEXTS[name]['quests'][str(quest)]
			elif 'default' in DIALOG_TEXTS[name]:
				self.dialog_texts = DIALOG_TEXTS[name]['default']
			else:
				self.dialog_texts = ["!DIALOG MISSING!"]
		else:
			self.dialog_texts = ["!DIALOG NAME MISSING!"]

		self.dialog_line = 0
		self.frame_index = 0
		self.writing_speed = 2
		self.current_text = ""

		self.dialog_ended = False


	def draw_dialogbox(self):
		# draw border & background
		pygame.draw.rect(self.display_surface, DIALOG_BORDER_COLOR, self.dialog_box_rect.inflate(6,6))
		pygame.draw.rect(self.display_surface, DIALOG_BG_COLOR, self.dialog_box_rect)

		self.frame_index += 1
		if len(self.current_text) < len(self.dialog_texts[self.dialog_line]):
			# loop over the frame index
			if self.frame_index >= self.writing_speed:
				self.frame_index = 0
				self.current_text = self.current_text + self.dialog_texts[self.dialog_line][len(self.current_text)]

		x, y = self.dialog_box_rect.topleft

	    # nom du personnage qui parle
		name_surf = self.font.render(self.name + ":", False, TEXT_COLOR)
		self.display_surface.blit(name_surf, (x+6, y+3))

		# ligne de dialogue
		text_surf = self.font.render(self.current_text, False, TEXT_COLOR)
		self.display_surface.blit(text_surf, (x+6+UI_FONT_SIZE, y+6+UI_FONT_SIZE))

		if len(self.current_text) == len(self.dialog_texts[self.dialog_line]):
			x, y = self.dialog_box_rect.bottomright
			y = y - UI_FONT_SIZE - 6
			if self.dialog_line < len(self.dialog_texts) - 1:
				next_txt = self.font.render("SUIVANT...", False, TEXT_COLOR)
				x = x - UI_FONT_SIZE * 8 - 6
			else:
				next_txt = self.font.render("FIN.", False, TEXT_COLOR)
				x = x - UI_FONT_SIZE * 3 - 6

			self.display_surface.blit(next_txt, (x, y))

	def stop_dialog(self):
		# todo
		return

	def next_dialog(self):
		if len(self.current_text) == len(self.dialog_texts[self.dialog_line]):
			if self.dialog_line < len(self.dialog_texts) - 1:
				self.dialog_line += 1
				self.current_text = ""
			else:
				self.dialog_ended = True

	def display(self):
		self.draw_dialogbox()


