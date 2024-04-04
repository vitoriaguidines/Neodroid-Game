import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, game, player, enemy_group, bullet_group, world):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load('img/icons/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.window_width = game.window_width
        self.player = player
        self.enemy_group = enemy_group
        self.bullet_group = bullet_group
        self.world = world
        self.game = game

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed) + self.game.screen_scroll
        # check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > self.window_width:
            self.kill()
        for tile in self.world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(self.player, self.bullet_group, False):  # PLAYER
            if self.player.alive:
                self.player.health -= 5
                self.kill()
        for enemy in self.enemy_group:
            if pygame.sprite.spritecollide(enemy, self.bullet_group, False): # ENEMIES
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()
