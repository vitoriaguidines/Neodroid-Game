import pygame

class ScreenFade:
    def __init__(self, direction, color, speed, wd, game):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
        self.window = wd
        self.game = game

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(self.window, self.color, (0 - self.fade_counter, 0, self.game.window_width // 2, self.game.window_height))
            pygame.draw.rect(self.window, self.color, (self.game.window_width // 2 + self.fade_counter, 0, self.game.window_width, self.game.window_height))
            pygame.draw.rect(self.window, self.color, (0, 0 - self.fade_counter, self.game.window_width, self.game.window_height // 2))
            pygame.draw.rect(self.window, self.color, (0, self.game.window_height // 2 + self.fade_counter, self.game.window_width, self.game.window_height))
        if self.direction == 2:
            pygame.draw.rect(self.window, self.color, (0, 0, self.game.window_width, 0 + self.fade_counter))
        if self.fade_counter >= self.game.window_width:
            fade_complete = True

        return fade_complete

