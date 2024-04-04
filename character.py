import pygame
import os
import globals

class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades, shot_fx, game, bullet_group, water_group, exit_group, world):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_delay = 0
        self.grenades = grenades
        self.shot_fx = shot_fx
        self.health = 100
        self.game = game
        self.water_group = water_group
        self.bullet_group = bullet_group
        self.exit_group = exit_group
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.update_time = pygame.time.get_ticks()
        # load all actions for the player
        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Attack']
        for animation in animation_types:
            # reset temp list of actions
            temp_list = []
            # count number of frames in a folder
            num_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for sprite_num in range(num_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{sprite_num}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale - 5), int(img.get_height() * scale - 5)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.world = world

    def update(self):
        self.update_animation()
        self.check_alive()
        #update delay
        if self.shoot_delay > 0:
            self.shoot_delay -= 1

    def move(self, moving_left, moving_right):
        GRAVITY = self.game.gravity
        # reset movement variables
        dx = dy = 0
        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump and self.in_air is False:
            self.vel_y = - 11
            self.jump = False
            self.in_air = True

        # gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        for tile in self.world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # death by water
        if pygame.sprite.spritecollide(self, self.water_group, False):
            self.health = 0

        # check for next level
        self.game.level_complete = False
        if pygame.sprite.spritecollide(self, self.exit_group, False):
            self.game.level_complete = True

        # death by fall
        if self.rect.bottom > self.game.window_height:
            self.health = 0

        # check edges of screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > self.game.window_width:
                dx = 0

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        if self.char_type == 'player':
            self.game.screen_scroll = 0
            if(self.rect.right > self.game.window_width - self.game.SCROLL_THRESH and self.game.bg_scroll < (self.world.level_length * (self.game.window_height // globals.ROWS)) - self.game.window_width) or (self.rect.left < self.game.SCROLL_THRESH and self.game.bg_scroll > abs(dx)):
                self.rect.x -= dx
                self.game.screen_scroll = -dx

    def shoot(self, bullet):
        if self.shoot_delay == 0 and self.ammo > 0:
            self.shoot_delay = 20
            self.bullet_group.add(bullet)
            # reduce ammo
            self.ammo -= 1
            self.shot_fx.play()

    def melee(self, bullet):
        if self.shoot_delay == 0:
            self.shoot_delay = 20
            self.bullet_group.add(bullet)

    def update_animation(self):
        # delay for the next animation
        ANIMATION_DELAY = 100
        # update image by frames
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # resets animation
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different from the actual one
        if new_action != self.action:
            self.action = new_action
            # update the animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self, window):
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
