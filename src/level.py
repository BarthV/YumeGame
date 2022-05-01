from operator import le
from xml.etree.ElementInclude import default_loader
import pygame
import pytmx
import pyscroll

from src.settings import *
from src.player import Player
from src.npc import NPC
from src.ui import UI
from src.debug import debug
from src.dialog import Dialogbox

class Level:
    def __init__(self):

        self.paused = False

        # get the display surface 
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_level = START_MAP_NAME
        self.world = pyscroll.PyscrollGroup
        self.world_colliders = []

        # NPC
        self.npcs = []

        # tile setup
        self.load_level(self.current_level)

        # level UI
        self.ui = UI()
        self.current_quest = 0

        self.dialogbox = Dialogbox("vieux pecheur", self.current_quest)

    def load_npc(self, poi: pytmx.TiledObject):
        # self.npcs = NPC((poi.x, poi.y), [self.world], poi)
        self.world.add(NPC(self.world, poi), layer=30)

    def load_level(self,level_name):
        # charger map
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/maps/{level_name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        start_pos = map_data.tmx.get_object_by_name("PLAYER_START")

        # charge l'ensemble des tiles qui ont des collisions configurées
        tile_colliders = map_data.tmx.get_tile_colliders()
        for tile_collider in tile_colliders:
            tile_gid, colliders = tile_collider
            # pour chaque type de tile avec des collisions, on recherche sur la map toutes les coordonées qui affichent cette tile là
            tiles_pos = map_data.tmx.get_tile_locations_by_gid(tile_gid)
            # pour chacune des tiles de la map, on va créer un rectagle et l'ajouter a une liste globale (qui servira pour calculer les collisions avec le joueur)
            for (x, y, l) in tiles_pos:
                for coll in colliders:
                    self.world_colliders.append(pygame.Rect((x*TILESIZE + coll.x, y*TILESIZE + coll.y), (coll.width, coll.height)))

        # for layer in pytmx_map.visible_layers:
        #     if isinstance(layer, pytmx.TiledTileLayer):
        #         for x in range(0, 25):
        #             for y in range(0, 25):
        #                 image = pytmx_map.get_tile_image(x, y, layer_index)
        #                 if image != None:
        #                     background.blit(image, (32*x, 32*y))
        #     layer_index += 1
        #     if isinstance(layer, pytmx.TiledObjectGroup):
        #         if layer.name == "hit block":
        #             for obj in layer:
        #                 if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(block.rect) == True:
        #                     print "YOU HIT THE RED BLOCK!!"
        #                     break

        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, (WIDTH,HEIGTH))
        map_layer.zoom = ZOOM_FACTOR

        self.world = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=10)

        # spawn NPC
        poi_layer = map_data.tmx.get_layer_by_name("poi")
        for poi in poi_layer:
            if poi.type == "npc":
                self.load_npc(poi)

        self.player = Player((start_pos.x, start_pos.y), self.world, self.world_colliders, self.create_attack, self.destroy_attack)
        self.world.add(self.player)
        

    def create_attack(self):
        # self.current_attack = Weapon(self.player,[self.visible_sprites])
        return

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def draw_pause(self):
        if self.paused:
            font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            text_surf = font.render("- PAUSED -",False,TEXT_COLOR)
            x = self.display_surface.get_size()[0] // 2
            y = self.display_surface.get_size()[1] // 2
            text_rect = text_surf.get_rect(midtop=(WIDTH//2, 6))
            pygame.draw.rect(self.display_surface, DIALOG_BORDER_COLOR, text_rect.inflate(6,6))
            pygame.draw.rect(self.display_surface, DIALOG_BG_COLOR, text_rect)
            self.display_surface.blit(text_surf,text_rect)

    def interact(self):
        self.paused = True
        self.dialogbox.next_dialog()
        if self.dialogbox.dialog_ended:
            self.paused = False
            self.dialogbox = Dialogbox("vieux pecheur", 1)

    def run(self):
        if not self.paused:
            # update and draw the game
            self.world.update()
            self.visible_sprites.update()
            self.obstacle_sprites.update()

        self.world.center(self.player.rect.center)

        self.world.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)
        self.obstacle_sprites.draw(self.display_surface)

        self.ui.display(self.player)
        self.draw_pause()
        if self.paused:
            self.dialogbox.display()
