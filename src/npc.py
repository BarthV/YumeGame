import pygame
import pytmx
from src.settings import *
from src.support import import_folder


class NPC(pygame.sprite.Sprite):
    def __init__(self, group, tiled_object: pytmx.TiledObject):
        super().__init__(group)

        self.group = group
        self.group.change_layer(self, 30)

        sprite_sheet_file = tiled_object.properties["spritesheet"]
        self.sprite_sheet = pygame.image.load(sprite_sheet_file).convert()
        self.name = tiled_object.name

        # graphics setup
        self.status = 'down'
        self.frame_index = 1
        self.animation_speed = 0.17
        self.animations = {}

        # init sprite
        self.init_animation_table()
        self.image = self.get_image(32, 0)
        self.rect = self.image.get_rect(topleft=(tiled_object.x, tiled_object.y))
        self.hitbox = self.rect.inflate(0, -26)

    def init_animation_table(self):
        self.animations = {
            'up': [(0, 96), (32, 96), (64, 96), (32, 96)],
            'up_idle': [(32, 96)],
            'down': [(0, 0), (32, 0), (64, 0), (32, 0)],
            'down_idle': [(32, 0)],
            'left': [(0, 32), (32, 32), (64, 32), (32, 32)],
            'left_idle': [(32, 32)],
            'right': [(0, 64), (32, 64), (64, 64), (32, 64)],
            'right_idle': [(32, 64)],
            'up_attack': [(32, 96)],
            'down_attack': [(32, 0)],
            'left_attack': [(32, 32)],
            'right_attack': [(32, 64)]
        }

    def get_image(self, x, y):
        image = pygame.Surface([32, 32]).convert()
        image.set_colorkey([0, 0, 0])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        x, y = animation[int(self.frame_index)]
        self.image = self.get_image(x, y)
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        animation = self.animations[self.status]
        x, y = animation[int(self.frame_index)]

        self.image = self.get_image(x, y)
        self.rect = self.image.get_rect(center=self.hitbox.center)
