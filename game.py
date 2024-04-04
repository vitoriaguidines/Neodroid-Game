import pygame

class Game:
    def __init__(self):
        self.gravity = 0.75
        self.window_width = 800
        self.window_height = int(self.window_width * 0.8)
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.tile_size = 100
        self.font = pygame.font.SysFont('Futura Md BT', 20)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.black = (0, 0, 0)

        self.SCROLL_THRESH = 200
        self.screen_scroll = 0
        self.bg_scroll = 0
        self.level_complete = False

    def draw_text(self, text, text_col, x, y, window):
        img = self.font.render(text, True, text_col)
        window.blit(img, (x,y))