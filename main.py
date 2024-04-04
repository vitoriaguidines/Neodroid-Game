# pyinstaller main
import os
import sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)


from pygame import mixer
import csv
import globals
from gameover import *
from grenade import Grenade
from ai import Ai
from melee import Melee
from menu import *
from world import *
from button import Button
from screenfade import ScreenFade

mixer.init()
pygame.init()

# game instance
game = Game()
GRAVITY = game.gravity
ROWS = globals.ROWS
COLS = globals.COLS
TILE_SIZE = game.window_height // ROWS
TILE_TYPES = 21
level = 1
MAX_LEVELS = globals.MAX_LEVELS
start_game = globals.start_game
start_intro = globals.start_intro

window = pygame.display.set_mode((game.window_width, game.window_height))
pygame.display.set_caption("Neodroid")
menu = Menu(window, game)
game_over = Gameover(window)
# set frame
clock = pygame.time.Clock()
FPS = 60

# define player action variables
moving_left = False
moving_right = False
shoot = False
melee = False
grenade = False
grenade_thrown = False

# sound fx
pygame.mixer.music.load('audio/music.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.5)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.5)

# main menu images
restart_img = pygame.image.load('img/menu/restart.png').convert_alpha()

# bg images
bg1_img = pygame.image.load('img/background/bg1.png').convert_alpha()
bg2_img = pygame.image.load('img/background/bg2.png').convert_alpha()
buildings_img = pygame.image.load('img/background/buildings.png').convert_alpha()
sky_img = pygame.image.load('img/background/sky.png').convert_alpha()
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
# bullet img
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
# grenade img
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()

# define BG colours
BG = (144, 201, 120)
RED = globals.RED
WHITE = globals.WHITE
GREEN = globals.GREEN
BLACK = globals.BLACK
PINK = globals.PINK

click = 0
paused = False

def update_music():
    if menu.sound == 0:
        pygame.mixer.music.set_volume(0)
    elif menu.sound == 1:
        pygame.mixer.music.set_volume(0.5)


def draw_bg():
    window.fill(BG)
    bg_width = sky_img.get_width()
    for x in range(5):
        window.blit(sky_img, ((x * bg_width) - game.bg_scroll * 0.5, 0))
        window.blit(buildings_img, ((x * bg_width) - game.bg_scroll * 0.6, game.window_height - buildings_img.get_height() - 300))
        window.blit(bg1_img, ((x * bg_width) - game.bg_scroll * 0.7, game.window_height - bg1_img.get_height() - 150))
        window.blit(bg2_img, ((x * bg_width) - game.bg_scroll * 0.8, game.window_height - bg2_img.get_height()))

def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


# screen fades
intro_fade = ScreenFade(1, BLACK, 4, window, game)
death_fade = ScreenFade(2, PINK, 4, window, game)

# button restart
restart_btn = Button(game.window_width // 2 - 150, game.window_height // 2 - 50, restart_img, 1)

# create sprite groups
bullet_group = game.bullet_group
enemy_group = game.enemy_group
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World(img_list, TILE_SIZE, game, bullet_group, enemy_group, grenade_group, explosion_group, item_box_group,
              decoration_group, water_group, exit_group, shot_fx)
player, health_bar, bullet_group, enemy_group, grenade_group, explosion_group, item_box_group, decoration_group, water_group, exit_group = world.process_data(
    world_data)

run = True

while run:
    clock.tick(FPS)
    menu.state = 0
    if not start_game:
        menu.draw_menu()
        if menu.play_btn.clicked:
            start_game = True
            start_intro = True
        if menu.stt_btn.clicked:
            menu.settings()
            if menu.stt_btn.clicked and menu.sound == 1:
                menu.stt_btn.clicked = False
                pygame.time.delay(100)
                pygame.mixer.music.set_volume(0)
                menu.sound = 0
            elif menu.stt_btn.clicked and menu.sound == 0:
                menu.stt_btn.clicked = False
                pygame.time.delay(100)
                pygame.mixer.music.set_volume(0.5)
                menu.sound = 1
        if menu.exit_btn.clicked:
            run = False
    else:
        draw_bg()
        # draw world map
        world.draw(window)
        # show player health
        health_bar.draw(player.health, window)
        # show ammo
        game.draw_text(f'AMMO: ', game.white, 10, 35, window)
        for x in range(player.ammo):
            window.blit(bullet_img, (90 + (x * 10), 40))
        # show grenades
        game.draw_text(f'GRENADES: ', game.white, 10, 60, window)
        for x in range(player.grenades):
            window.blit(grenade_img, (135 + (x * 15), 60))

        player.update()
        player.draw(window)

        enemy_bullet = Bullet(player.rect.centerx + (0.75 * player.rect.size[0] * player.direction),
                              player.rect.centery,
                              player.direction, game, player, enemy_group, bullet_group, world)
        update_music()
        for enemy in enemy_group:
            ai = Ai(enemy, player, window, game, enemy_group, bullet_group, world)
            ai.run()
            enemy.update()
            enemy.draw(window)

        # update and draw groups
        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update(player)
        decoration_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(window)
        grenade_group.draw(window)
        explosion_group.draw(window)
        item_box_group.draw(window)
        decoration_group.draw(window)
        water_group.draw(window)
        exit_group.draw(window)

        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # update player actions
        if player.alive:
            # shoot bullets
            if shoot:
                bullet = Bullet(player.rect.centerx + (0.90 * player.rect.size[0] * player.direction),
                                player.rect.centery,
                                player.direction, game, player, enemy_group, bullet_group, world)
                player.shoot(bullet)
            elif melee:
                sword = Melee(player.rect.centerx + (0.90 * player.rect.size[0] * player.direction),
                                player.rect.centery,
                                player.direction, game, player, enemy_group, bullet_group, world)
                player.melee(sword)
            # throw grenades
            elif grenade and grenade_thrown is False and player.grenades > 0:
                bomb = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),
                                  player.rect.top, player.direction, game, explosion_group, grenade_fx, player,
                                  enemy_group, world)
                grenade_group.add(bomb)
                # reduce grenades
                player.grenades -= 1
                grenade_thrown = True
            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            elif melee:
                player.update_action(4)
            else:
                player.update_action(0)  # 2 is jump, 1 is run, 0 is idle
            player.move(moving_left, moving_right)
            game.bg_scroll -= game.screen_scroll
            # check for level completion
            if game.level_complete:
                level += 1
                if level <= MAX_LEVELS:
                    start_intro = True
                    game.bg_scroll = 0
                    world_data = reset_level()
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World(img_list, TILE_SIZE, game, bullet_group, enemy_group, grenade_group, explosion_group,
                                  item_box_group, decoration_group, water_group, exit_group, shot_fx)
                    player, health_bar, bullet_group, enemy_group, grenade_group, explosion_group, item_box_group, decoration_group, water_group, exit_group = world.process_data(
                        world_data)
                else:
                    paused = True
                    game_over.draw()
                    pygame.time.delay(100)
                    if game_over.exit_btn.clicked:
                        run = False



        else:
            game.screen_scroll = 0
            if death_fade.fade():
                if restart_btn.draw(window):
                    death_fade.fade_counter = 0
                    start_intro = True
                    game.bg_scroll = 0
                    world_data = reset_level()
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World(img_list, TILE_SIZE, game, bullet_group, enemy_group, grenade_group, explosion_group,
                                  item_box_group, decoration_group, water_group, exit_group, shot_fx)
                    player, health_bar, bullet_group, enemy_group, grenade_group, explosion_group, item_box_group, decoration_group, water_group, exit_group = world.process_data(
                        world_data)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and not paused:
                    moving_left = True
                if event.key == pygame.K_d and not paused:
                    moving_right = True
                if event.key == pygame.K_SPACE and not paused:
                    shoot = True
                if event.key == pygame.K_v and not paused:
                    melee = True
                if event.key == pygame.K_q:
                    grenade = True
                if event.key == pygame.K_w and player.alive and not paused:
                    player.jump = True
                    jump_fx.play()
                if event.key == pygame.K_ESCAPE:
                    run = False
            # keyboard button released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_SPACE:
                    shoot = False
                if event.key == pygame.K_v:
                    melee = False
                if event.key == pygame.K_q:
                    grenade = False
                    grenade_thrown = False
    pygame.display.update()
pygame.quit()
