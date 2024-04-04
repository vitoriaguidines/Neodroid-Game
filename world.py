import pygame
from game import Game
from itembox import ItemBox
from healthbar import HealthBar
from character import Character
from bullet import Bullet
import random

class World:
	def __init__(self, img_list, tile_size, game, bg, eng, gg, exg, ibg, dg, wg, etg, shfx):
		self.obstacle_list = []
		self.img_list = img_list
		self.tile_size = tile_size
		self.game = game
		self.bullet_group = bg
		self.enemy_group = eng
		self.grenade_group = gg
		self.explosion_group = exg
		self.item_box_group = ibg
		self.decoration_group = dg
		self.water_group = wg
		self.exit_group = etg
		self.shot_fx = shfx

	def process_data(self, data):
		self.level_length = len(data[0])
		global player, health_bar
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = self.img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * self.tile_size
					img_rect.y = y * self.tile_size
					tile_data = (img, img_rect)
					if 0 <= tile <= 8:
						self.obstacle_list.append(tile_data)

					elif 9 <= tile <= 10:
						water = Water(img, x * self.tile_size, y * self.tile_size, self.tile_size, self.game)
						self.water_group.add(water)

					elif 11 <= tile <= 14:
						decoration = Decoration(img, x * self.tile_size, y * self.tile_size, self.tile_size, self.game)
						self.decoration_group.add(decoration)

					elif tile == 15: #create player
						player = Character('player', x * self.tile_size, y * self.tile_size, 1.65, 5, 20, 5, self.shot_fx, self.game, self.bullet_group, self.water_group, self.exit_group, self)
						health_bar = HealthBar(10, 10, player.health, player.health)

					elif tile == 16: #create enemies
						i = random.randint(1, 2)
						enemy = Character(f'enemy{i}', x * self.tile_size, y * self.tile_size, 1.65, 2, 20, 0, self.shot_fx, self.game, self.bullet_group, self.water_group, self.exit_group, self)
						self.enemy_group.add(enemy)

					elif tile == 17: #create ammo box
						ammo_box = ItemBox('Ammo', x * self.tile_size, (y - 1.5) * self.tile_size, self.game)
						self.item_box_group.add(ammo_box)

					elif tile == 18: #create grenade box
						grenade_box = ItemBox('Grenade', x * self.tile_size, (y - 1.5) * self.tile_size, self.game)
						self.item_box_group.add(grenade_box)

					elif tile == 19: #create health box
						health_box = ItemBox('Health', x * self.tile_size, (y - 1.5) * self.tile_size, self.game)
						self.item_box_group.add(health_box)

					elif tile == 20: #create exit
						exit = Exit(img, x * self.tile_size, y * self.tile_size, self.tile_size, self.game)
						self.exit_group.add(exit)

		return player, health_bar, self.bullet_group, self.enemy_group, self.grenade_group, self.explosion_group, \
			   self.item_box_group, self.decoration_group, self.water_group, self.exit_group

	def draw(self, window):
		for tile in self.obstacle_list:
			tile[1][0] += self.game.screen_scroll
			window.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y, tile_size, game):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.game = game
		self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

	def update(self):
		self.rect.x += self.game.screen_scroll


class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y, tile_size, game):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.game = game
		self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

	def update(self):
		self.rect.x += self.game.screen_scroll


class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y, tile_size, game):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.game = game
		self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

	def update(self):
		self.rect.x += self.game.screen_scroll