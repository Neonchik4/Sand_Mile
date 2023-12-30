import pygame
import os
import sys
import random
import math


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    screen.fill((125, 125, 125))
    intro_text = ['',
                  "Правила игры:",
                  "Здесь пока что карта не загружена - находится в процессе разработки",
                  "Загрузка тайлов в процессе"]

    fon = pygame.transform.scale(load_image('logo.png'), (674, 107))
    screen.blit(fon, (WIDTH // 2 - 337, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 75
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect()
        self.orig = self.image

    def rotate_towards_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.x + self.rect[2] // 3), mouse_y - (self.y + self.rect[3] // 3)
        print(mouse_x, mouse_y)
        if ((mouse_x < 456 or mouse_x > 504) or (mouse_y > 501 or mouse_y < 459)) and mouse_y != 391 and mouse_y != 512:
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.orig, int(angle) - 90)
            self.rect = self.image.get_rect(center=self.rect.center)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


pygame.init()

size = WIDTH, HEIGHT = 960, 960
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sand Mile')
clock = pygame.time.Clock()

tile_width = tile_height = 32
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
camera = Camera()
STEP = 50
FPS = 50

player_image = pygame.transform.scale(load_image('units/alpha.png'), (44, 40))
cursor = pygame.image.load('data/cursor.png')
player = Player(WIDTH // 2 - 22, HEIGHT // 2 - 20)
start_screen()

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= STEP
            if event.key == pygame.K_RIGHT:
                player.rect.x += STEP
            if event.key == pygame.K_UP:
                player.rect.y -= STEP
            if event.key == pygame.K_DOWN:
                player.rect.y += STEP

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    tiles_group.draw(screen)
    player_group.draw(screen)
    player.rotate_towards_mouse()

    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        screen.blit(cursor, (x, y))

    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
