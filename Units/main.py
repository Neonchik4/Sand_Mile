import os
import sys
import math
import pygame
import random
from PIL import Image


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


def terminate():
    pygame.quit()
    sys.exit()


def image_to_list(file_name):
    im = Image.open(file_name)
    pixels = list(im.getdata())
    width, height = im.size
    new_pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return new_pixels


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
    return image


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in tiles_images:
                Tile(level[y][x], x, y)
            elif level[y][x] == (136, 0, 21):
                Tile(base_pixel, x, y)
                new_player = Player(x, y)
            else:
                Tile(base_pixel, x, y)
    return new_player, x, y


# TODO: сделать спавн в опр радиусе
# Пока в определом месте, потом пройдемся по карте и найдем место спавна
def spawn_enemy(level, r):
    return Dagger(400, 400)


class Dagger(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        # self.hp = ???
        # self.damage = ???
        self.x = pos_x
        self.y = pos_y
        self.image = pygame.transform.scale(load_image("units/dagger.png"), (50, 50))
        self.rect = self.image.get_rect().move(self.x, self.y)

    # Как пример реализовал движение за мышкой
    # TODO: Сделать нормальное движение в сторонц мышки(так же понадобится для пуль и для перемещения в сторону главного здания)
    def update(self):
        velocity = 5
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, int(angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        print(angle)
        # self.x, self.y = velocity * math.cos(angle), velocity * math.sin(angle)
        # self.rect.move_ip(self.x, self.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.x = pos_x * tile_width
        self.y = pos_y * tile_height
        self.image = player_image
        self.rect = self.image.get_rect().move(self.x, self.y)
        # в комментариях лежит магический фокус
        self.orig = self.image

        def rotate_towards_mouse(self):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - (self.rect[0] + self.rect[2] // 2), mouse_y - (self.rect[1] + self.rect[3] // 2)
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            self.image = pygame.transform.rotate(self.orig, int(angle) - 90)
            self.rect = self.image.get_rect(center=self.rect.center)

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = None
            if type(tiles_images[tile_type]) == list:  # по неведомой причине через is не работает
                self.image = random.choice(tiles_images[tile_type])
            else:
                self.image = tiles_images[tile_type]
            self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


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


tiles_images = {
    # ground blocks
    (0, 0, 0): load_image('tiles/ground/black_tile.png'),
    (127, 127, 127): [load_image('tiles/ground/basalt_1.png'), load_image('tiles/ground/basalt_2.png'),
                      load_image('tiles/ground/basalt_3.png')],
    (255, 128, 255): [load_image('tiles/ground/bluemat1.png'), load_image('tiles/ground/bluemat2.png'),
                      load_image('tiles/ground/bluemat3.png')],
    (120, 120, 120): [load_image('tiles/ground/classem-stolnene1.png'),
                      load_image('tiles/ground/classem-stolnene2.png'),
                      load_image('tiles/ground/classem-stolnene3.png')],
    (120, 64, 20): [load_image('tiles/ground/dirt1.png'), load_image('tiles/ground/dirt2.png'),
                    load_image('tiles/ground/dirt3.png')],
    (181, 181, 240): [load_image('tiles/ground/ice1.png'), load_image('tiles/ground/ice2.png'),
                      load_image('tiles/ground/ice3.png')],
    (251, 82, 0): [load_image('tiles/ground/magmarock1.png'), load_image('tiles/ground/magmarock2.png'),
                   load_image('tiles/ground/magmarock3.png')],
    (102, 33, 0): [load_image('tiles/ground/mud1.png'), load_image('tiles/ground/mud2.png'),
                   load_image('tiles/ground/mud3.png')],
    (210, 174, 141): [load_image('tiles/ground/sand_ground_1.png'), load_image('tiles/ground/sand_ground_2.png'),
                      load_image('tiles/ground/sand_ground_3.png')],
    (60, 56, 56): [load_image('tiles/ground/darksand1.png'), load_image('tiles/ground/darksand2.png'),
                   load_image('tiles/ground/darksand3.png')],
    # wall blocks
    (196, 100, 64): [load_image('tiles/wall_blocks/dirt-wall1.png'), load_image('tiles/wall_blocks/dirt-wall2.png')],
    (141, 141, 141): [load_image('tiles/wall_blocks/dune-wall1.png'), load_image('tiles/wall_blocks/dune-wall2.png')],
    (120, 101, 92): [load_image('tiles/wall_blocks/ferric-stone-wall1.png'),
                     load_image('tiles/wall_blocks/ferric-stone-wall2.png')],
    (130, 125, 233): [load_image('tiles/wall_blocks/ice-wall1.png'), load_image('tiles/wall_blocks/ice-wall2.png')],
    (126, 38, 66): [load_image('tiles/wall_blocks/red-stone-wall1.png'),
                    load_image('tiles/wall_blocks/red-stone-wall2.png'),
                    load_image('tiles/wall_blocks/red-stone-wall3.png')],
    (218, 181, 96): [load_image('tiles/wall_blocks/regolith-wall1.png'),
                     load_image('tiles/wall_blocks/regolith-wall2.png')],
    (69, 32, 32): [load_image('tiles/wall_blocks/rhyolite-wall1.png'),
                   load_image('tiles/wall_blocks/rhyolite-wall2.png')],
    (174, 180, 196): [load_image('tiles/wall_blocks/salt-wall1.png'), load_image('tiles/wall_blocks/salt-wall2.png')],
    (225, 228, 201): [load_image('tiles/wall_blocks/sand_tile_1.png'), load_image('tiles/wall_blocks/sand_tile_2.png')],
    (92, 86, 122): [load_image('tiles/wall_blocks/shale-wall1.png'), load_image('tiles/wall_blocks/shale-wall2.png')],
    (225, 233, 240): [load_image('tiles/wall_blocks/snow-wall1.png'), load_image('tiles/wall_blocks/snow-wall2.png')],
    (153, 94, 154): [load_image('tiles/wall_blocks/spore-wall1.png'), load_image('tiles/wall_blocks/spore-wall2.png')],
    (82, 82, 92): [load_image('tiles/wall_blocks/stone-wall1.png'), load_image('tiles/wall_blocks/stone-wall2.png')],
    (146, 94, 70): [load_image('tiles/wall_blocks/yellow-stone-wall1.png'),
                    load_image('tiles/wall_blocks/yellow-stone-wall2.png')],
}

pygame.init()
FPS = 60
STEP = 50

tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
camera = Camera()
player_image = load_image('units/alpha.png')
base_pixel = image_to_list('data/maps/map_1.png')[0][0]  # если не знаем какой это пиксель, берём этот
player_image = pygame.transform.scale(load_image('units/alpha.png'), (44, 40))
player, level_x, level_y = generate_level(image_to_list('data/maps/map_1.png'))
SIZE = WIDTH, HEIGHT = 1980, 1980
screen = pygame.display.set_mode(SIZE)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()


cursor = pygame.image.load('data/cursor.png')
start_screen()

my_event = pygame.USEREVENT
pygame.time.set_timer(my_event, 1000)
flag = True
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == my_event and flag:
            # Список пока не настоящий(Должна передватся карта или координаты точки спавна)
            enemy = spawn_enemy([1, 2, 3], 10)
            flag = False
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
    # player_group.draw(screen)
    enemy_group.draw(screen)
    enemy_group.update()
    player.rotate_towards_mouse()

    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        screen.blit(cursor, (x, y))

    pygame.display.flip()
    clock.tick(FPS)
