import pygame

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
        self.ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
        self.grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
        self.item_type = item_type
        self.item_boxes = {
            'Health' : self.health_box_img,
            'Ammo'   : self.ammo_box_img,
            'Grenade': self.grenade_box_img,
        }
        self.image = self.item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.game = game
        self.rect.midtop = (x + self.game.tile_size // 2, y + (self.game.tile_size - self.image.get_height()))


    def update(self, player):
        self.rect.x += self.game.screen_scroll
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Grenade':
                player.grenades += 3
            self.kill()

