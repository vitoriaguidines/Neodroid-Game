import pygame


class Melee(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, game, player, enemy_group, melee_group, world):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/icons/melee.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.window_width = game.window_width
        self.player = player
        self.enemy_group = enemy_group
        self.melee_group = melee_group
        self.world = world
        self.game = game
        self.max_dist = self.rect.x


    def update(self):
        # move bullet
        for tile in self.world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        for enemy in self.enemy_group:
            if pygame.sprite.spritecollide(enemy, self.melee_group, False): # ENEMIES
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()
