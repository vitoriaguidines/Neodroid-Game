import pygame

from explosion import Explosion


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, game, explosion_group, grfx, player, enemy_group, world):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = pygame.image.load('img/icons/grenade.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.game = game
        self.explosion_group = explosion_group
        self.player = player
        self.enemy_group = enemy_group
        self.world = world
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.grenade_fx = grfx

    def update(self):
        self.vel_y += self.game.gravity
        dx = self.direction * self.speed
        dy = self.vel_y

        for tile in self.world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
        #update grenade position
        self.rect.x += dx + self.game.screen_scroll
        self.rect.y += dy

        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            self.grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 1, self.game)
            self.explosion_group.add(explosion)

            if abs(self.rect.centerx - self.player.rect.centerx) < self.game.tile_size and abs(self.rect.centery - self.player.rect.centery) < self.game.tile_size:
                self.player.health -= 50

            for enemy in self.enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < self.game.tile_size and abs(self.rect.centery - enemy.rect.centery) < self.game.tile_size * 2:
                    enemy.health -= 50
