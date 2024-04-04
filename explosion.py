import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, game):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 6):
            img = pygame.image.load(f'img/explosion/exp{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
        self.game = game

    def update(self):
        # scroll
        self.rect.x += self.game.screen_scroll

        EXPLOSION_SPEED = 4
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            # if the animation is complete, delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
