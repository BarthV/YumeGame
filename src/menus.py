import pygame
import pygame_menu

def set_difficulty(self, value, difficulty):
    # Do the job here !
    pass

def start_the_game(self):
    # Do the job here !
    pass


class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button('Start Game', start_the_game)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def display(self):
        self.menu.mainloop(self.display_surface)
