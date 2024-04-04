from button import *
from pygame import *


class Menu(pygame.sprite.Sprite):
    def __init__(self, wd, game):
        pygame.sprite.Sprite.__init__(self)
        self.window = wd
        self.game = game
        play_img = pygame.image.load('img/menu/play.png').convert_alpha()
        stt_img = pygame.image.load('img/menu/settings.png').convert_alpha()
        self.with_sound_img = pygame.image.load('img/menu/with_sound.png').convert_alpha()
        self.mute_img = pygame.image.load('img/menu/mute.png').convert_alpha()
        exit_img = pygame.image.load('img/menu/exit.png').convert_alpha()
        controls_img = pygame.image.load('img/menu/controls.png').convert_alpha()
        self.menu_bg = pygame.image.load('img/menu/menu.png').convert_alpha()
        self.controls_bg = pygame.image.load('img/menu/controls_bg.png').convert_alpha()
        self.play_btn = Button(107, 179, play_img, 1)
        self.stt_btn = Button(107, 254, stt_img, 1)
        self.exit_btn = Button(107, 333, exit_img, 1)
        self.controls_btn = Button(490, 450, controls_img, 1)
        self.state = 1
        self.sound = 1
        self.select = 0

    def controls(self):
        self.window.blit(self.controls_bg, (0, 0))

    def settings(self):
        if self.sound == 1:
            self.stt_btn = Button(107, 254, self.with_sound_img, 1)
            self.stt_btn.draw(self.window)

        if self.sound == 0:
            self.stt_btn = Button(107, 254, self.mute_img, 1)
            self.stt_btn.draw(self.window)

    def menu(self):
        self.play_btn.draw(self.window)
        self.stt_btn.draw(self.window)
        self.exit_btn.draw(self.window)
        self.controls_btn.draw(self.window)

    def draw_menu(self):
        self.window.blit(self.menu_bg, (0, 0))
        self.menu()
        if self.controls_btn.clicked:
            self.controls()
        if self.state == 0:
            self.state = 1
            for event in pygame.event.get():
                if event.type == pygame.K_ESCAPE:
                    self.state = 1
        elif self.state == 2:
            self.window.blit(self.menu_bg)
            self.settings()
            for event in pygame.event.get():
                if self.select == 0 and event.type == pygame.K_ESCAPE:
                    self.state = 1
        elif self.state == 1:
            self.menu()
        pygame.display.update()
