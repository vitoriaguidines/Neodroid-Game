from button import *


class Gameover(pygame.sprite.Sprite):
    def __init__(self, wd):
        pygame.sprite.Sprite.__init__(self)
        self.window = wd
        exit_img = pygame.image.load('img/menu/exit.png').convert_alpha()
        self.game_over_bg = pygame.image.load('img/menu/gameover.png').convert_alpha()
        self.exit_btn = Button(250, 500, exit_img, 1)

    def game_over(self):
        self.exit_btn.draw(self.window)

    def draw(self):
        self.window.blit(self.game_over_bg, (0, 0))
        self.game_over()
        pygame.display.update()
