import pygame
import globals
import random
from bullet import Bullet

class Ai(pygame.sprite.Sprite):
    def __init__(self, enemy, player, window, game, enemy_group, bullet_group, world):
        self.enemy = enemy
        self.player = player
        self.window = window
        self.bullet_group = bullet_group
        self.enemy_group = enemy_group
        self.game = game
        self.bullet = Bullet(self.enemy.rect.centerx + (0.75 * self.enemy.rect.size[0] * self.enemy.direction),
                             self.enemy.rect.centery, self.enemy.direction, game, self.player, self.enemy_group, self.bullet_group, world)

    def run(self):
        if self.enemy.alive and self.player.alive:
            if self.enemy.idling == False and random.randint(1, 200) == 1:
                self.enemy.update_action(0)
                self.enemy.idling = True
                self.enemy.idling_counter = 50
            if self.enemy.vision.colliderect(self.player.rect):
                self.enemy.update_action(0)
                self.enemy.shoot(self.bullet)
            else:
                if not self.enemy.idling:
                    if self.enemy.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.enemy.move(ai_moving_left, ai_moving_right)
                    self.enemy.update_action(1)
                    self.enemy.move_counter += 1
                    self.enemy.vision.center = (self.enemy.rect.centerx + 75 * self.enemy.direction,
                                                self.enemy.rect.centery)

                    if self.enemy.move_counter > globals.tile_size:
                        self.enemy.direction *= -1
                        self.enemy.move_counter *= -1
                else:
                    self.enemy.idling_counter -= 1
                    if self.enemy.idling_counter <= 0:
                        self.enemy.idling = False

        self.enemy.rect.x += self.game.screen_scroll