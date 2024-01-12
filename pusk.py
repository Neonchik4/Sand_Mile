import pygame
import os
import sys
import random
import math
from PIL import Image


def image_to_list(file_name):
    im = Image.open(file_name)
    pixels = list(im.getdata())
    width, height = im.size
    new_pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return new_pixels


def generate_level(level):
    new_player, lvl_x, lvl_y = None, None, None
    resource_map = image_to_list('data/maps/resource_maps/resource_map_1.png')
    for y in range(len(level)):
        for x in range(len(level[y])):
            if x != 0 and y != 0:
                if level[y][x] in tiles_images:
                    Tile(level[y][x], x, y)
                elif level[y][x] == (136, 0, 21):  # r, g, b игрока
                    Tile(player_pixel, x, y)
                    new_player = (x, y)
                elif level[y][x] != (255, 0, 0):
                    Tile(player_pixel, x, y)
            else:
                Tile((0, 0, 0), x, y)
            if level[y][x] == (210, 174, 141) or level[y][x] == (60, 56, 56):
                board.resource_map[y][x] = 'sand'

    for j in range(len(resource_map)):
        for i in range(len(resource_map[j])):
            if resource_map[j][i] != (255, 255, 255) and resource_map[j][i] in ores_images.keys():
                ResourceTile(resource_map[j][i], i, j)
                board.resource_map[j][i] = ores_to_str[resource_map[j][i]]
            if resource_map[j][i] == (255, 0, 128):
                board.industry_map[j][i] = ores_to_str[resource_map[j][i]]
    # вернем игрока, а также размер поля в клетках
    return *new_player, lvl_x, lvl_y


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
    # Не трогать пустую строку - это отступ от заставки
    intro_text = ['',
                  "Правила игры:",
                  "Здесь пока что карта не загружена - находится в процессе разработки",
                  "Загрузка тайлов в процессе"]

    fon = pygame.transform.scale(load_image('logo.png'), (674, 107))
    screen.blit(fon, (WIDTH // 2 - 337, 0))
    font = pygame.font.Font(None, 25)
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
        self.x = pos_x * tile_width
        self.y = pos_y * tile_height
        self.image = player_image
        self.is_in_motion = False
        self.hp = 100
        self.rect = self.image.get_rect().move(self.x, self.y)
        # print(self.x, self.y)
        # print()
        # print(self.rect[0], self.rect[1])
        # в комментариях лежит магический фокус
        self.orig = self.image

    def rotate_towards_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect[0] + self.rect[2] // 2), mouse_y - (self.rect[1] + self.rect[3] // 2)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.orig, int(angle) - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        if self.is_in_motion:
            self.orig = player_image_in_move
        else:
            self.orig = player_image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = None
        if type(tiles_images[tile_type]) == list:  # по неведомой причине через is не работает
            self.image = random.choice(tiles_images[tile_type])
        else:
            self.image = tiles_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class ResourceTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(resource_tiles_group, all_sprites)
        self.image = None
        if type(ores_images[tile_type]) == list:  # по неведомой причине через is не работает
            self.image = random.choice(ores_images[tile_type])
        else:
            self.image = ores_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class DJ:
    def __init__(self):
        # None означает, что ничего не надо проигрывать
        self.drill_sound = pygame.mixer.Sound("data/sounds/drill_idle.wav")
        self.play_drill_sound = None
        self.conveyor_sound = pygame.mixer.Sound("data/sounds/conveyorbelt_idle.wav")
        self.play_conveyor_sound = None

        self.soundtracks = [pygame.mixer.Sound("data/sounds/sandmile_ambient_1_dark.wav")]
        self.index_of_sound = None

    def update(self):
        # звук дрели
        if self.play_drill_sound:
            self.drill_sound.play(loops=-1)
            self.drill_sound.set_volume(0.75)
            self.play_drill_sound = None
        if not self.drill_sound:
            self.drill_sound.stop()

        # звук конвейера
        if self.play_conveyor_sound:
            self.conveyor_sound.play(loops=-1)
            self.play_conveyor_sound = None
        if not self.conveyor_sound:
            self.conveyor_sound.stop()

        # саундтреки
        if self.index_of_sound is not None:
            soundtrack.play(self.soundtracks[self.index_of_sound], loops=1)
            soundtrack.set_volume(0.75)
            self.index_of_sound = None


class Board:
    def __init__(self):
        # industry map отвечает за расположение логистических блоков (каждый блок занимает несколько клеток)030
        self.industry_map = [[None for _ in range(len(lst_map[0]))] for __ in range(len(lst_map))]
        # тоже самое, только каждый блок занимает одну клетку во избежание повторного отрисовывания
        self.industry_map_to_drawing = [[None for _ in range(len(lst_map[0]))] for __ in range(len(lst_map))]
        # Карта ресурсов
        self.resource_map = [[None for _ in range(len(lst_map[0]))] for __ in range(len(lst_map))]

    def append(self, ind_1, ind_2, block):
        # добавляем класс block во все нужные клетки
        for siz in range(2):
            for high in range(2):
                self.industry_map[ind_1 + siz][ind_2 + high] = block


def frame_positions(pos1, pos2, pos3, *pos_mouse):
    global destroy, build, blocks_type, type_of_current_block
    mouse_x, mouse_y = pos_mouse
    # задействуем правую часть меню
    if 214 <= mouse_x <= 309 and HEIGHT - 250 <= mouse_y <= HEIGHT - 5:
        if 214 <= mouse_x <= 263 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            # frame на турель
            pos1 = (214, HEIGHT - 250)
            blocks_type = 'turrets'
        elif 214 <= mouse_x <= 263 and HEIGHT - 199 <= mouse_y <= HEIGHT - 159:
            # frame на конвеер
            pos1 = (214, HEIGHT - 199)
            blocks_type = 'conveyors'
        elif 264 <= mouse_x <= 309 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            # frame на бур
            pos1 = (264, HEIGHT - 250)
            blocks_type = 'drills'
        elif 214 <= mouse_x <= 263 and HEIGHT - 97 <= mouse_y <= HEIGHT - 57:
            # frame на завод
            pos1 = (214, HEIGHT - 97)
            blocks_type = 'factories'
        elif 264 <= mouse_x <= 309 and HEIGHT - 150 <= mouse_y <= HEIGHT - 98:
            pos1 = (264, HEIGHT - 150)
            blocks_type = 'defensive_walls'
        elif 264 <= mouse_x <= 309 and HEIGHT - 97 <= mouse_y <= HEIGHT - 47:
            pos1 = (264, HEIGHT - 97)
            blocks_type = 'drone factories'

    # задействуем левую верхнюю часть меню (также выбор текущего блока)
    if blocks_type == 'drills':
        if 4 <= mouse_x <= 54 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'mechanical drill'
            pos2 = (4, HEIGHT - 250)
        elif 55 <= mouse_x <= 105 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'pneumatic drill'
            pos2 = (55, 710)

    # задействуем нижнюю левую часть меню
    if 4 <= mouse_x <= 209 and HEIGHT - 54 <= mouse_y <= HEIGHT - 4:
        if 4 <= mouse_x <= 54:
            build = not build
            destroy = False
        elif 55 <= mouse_x <= 105:
            destroy = not destroy
            build = False

        if destroy:  # frame на значок уничтожения блоков
            pos3 = (55, HEIGHT - 54)
        elif build:  # frame на строение блоков
            pos3 = (4, HEIGHT - 54)
        else:
            pos3 = None

    return pos1, pos2, pos3


pygame.init()
pygame.mixer.init()

size = WIDTH, HEIGHT = 1280, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sand Mile')
clock = pygame.time.Clock()

tile_width = tile_height = 32
STEP = 7
FPS = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
resource_tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

cursor = pygame.image.load('data/cursor.png')
menu = pygame.image.load('data/menu/item_menu.png')
frame = pygame.image.load('data/menu/frame.png')
drills_image = pygame.image.load('data/menu/menu_drills.png')
collected_mechanical_drill = pygame.image.load('data/drills/collected_mechanical_drill.png')
collected_pneumatic_drill = pygame.image.load('data/drills/collected_pneumatic_drill.png')
right_frame_pos, top_left_frame_pos, bottom_left_frame_pos = None, None, None
blocks_type = None
type_of_current_block = None
build, destroy = False, False

# r, g, b для каждого tile
tiles_images = {
    # ground blocks
    (0, 0, 0): load_image('tiles/ground/black_tile.png'),
    (232, 120, 0): load_image('cores/core_1.png'),
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
# если не знаем какой это пиксель, берём случайный из этих
default_pixels = [(127, 127, 127), (120, 120, 120), (60, 56, 56)]
# словарь цветов для руд
ores_images = {
    (0, 0, 0): [load_image('ores/coal/coal_1.png'), load_image('ores/coal/coal_2.png'),
                load_image('ores/coal/coal_3.png')],
    (174, 124, 91): [load_image('ores/copper/copper_1.png'), load_image('ores/copper/copper_2.png'),
                     load_image('ores/copper/copper_3.png')],
    (142, 133, 162): [load_image('ores/lead/lead_1.png'), load_image('ores/lead/lead_2.png'),
                      load_image('ores/lead/lead_3.png')],
    (155, 146, 139): [load_image('ores/scrap/scrap_1.png'), load_image('ores/scrap/scrap_2.png'),
                      load_image('ores/scrap/scrap_3.png')],
    (205, 159, 207): [load_image('ores/thorium/thorium_1.png'), load_image('ores/thorium/thorium_2.png'),
                      load_image('ores/thorium/thorium_3.png')],
    (120, 141, 207): [load_image('ores/titanium/titanium_1.png'), load_image('ores/titanium/titanium_2.png'),
                      load_image('ores/titanium/titanium_3.png')],

    # здесь для неудобства лежит ключ спауна юнитов
    (255, 0, 128): load_image('spawn_mark.png')
}
# словарь по переводу r, g, b в строки
ores_to_str = {
    (0, 0, 0): 'coal',
    (174, 124, 91): 'copper',
    (142, 133, 162): 'lead',
    (155, 146, 139): 'scrap',
    (205, 159, 207): 'thorium',
    (120, 141, 207): 'titanium',
    (255, 0, 128): 'spawn_mark'
}
# пиксель под игрока
player_pixel = image_to_list('data/maps/snow_map_1.png')[0][0]
# Для работы с картами
map_name = 'data/maps/snow_map_1.png'
lst_map = image_to_list(map_name)

dj = DJ()
# представления о игровой доске
board = Board()
camera = Camera()

# ВАЖНО: PLAYER всегда должен находиться над пикселем ядра(пометка для создания карт)
# (136, 0, 21): player
# цвет игрока обязан присутствовать на поле
# (255, 0, 0): blocked
player_image = pygame.transform.scale(load_image('units/alpha.png'), (45, 40))
player_image_in_move = pygame.transform.scale(load_image('units/alpha_with_light.png'), (45, 74))
player_x, player_y, level_x, level_y = generate_level(lst_map)
player = Player(player_x, player_y)

pygame.mixer.set_num_channels(10)
soundtrack = pygame.mixer.Channel(2)
start_screen()

while True:
    screen.fill((0, 0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # лкм
            right_frame_pos, top_left_frame_pos, bottom_left_frame_pos = frame_positions(right_frame_pos,
                                                                                         top_left_frame_pos,
                                                                                         bottom_left_frame_pos,
                                                                                         *pygame.mouse.get_pos())

    # перемещение персонажа
    player.is_in_motion = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.is_in_motion = True
        player.x -= STEP
        for i in range(5):
            player.rect.x -= STEP / 5
    if keys[pygame.K_d]:
        player.is_in_motion = True
        player.x += STEP
        for i in range(5):
            player.rect.x += STEP / 5
    if keys[pygame.K_w]:
        player.is_in_motion = True
        player.y -= STEP
        for i in range(5):
            player.rect.y -= STEP / 5
    if keys[pygame.K_s]:
        player.is_in_motion = True
        player.y += STEP
        for i in range(5):
            player.rect.y += STEP / 5
    player.update()  # для переключения картинки

    tmp = random.randrange(0, 5000)
    if tmp == 1 and not soundtrack.get_busy():
        dj.index_of_sound = random.randint(0, len(dj.soundtracks) - 1)
    dj.update()

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    # рисуем все группы спрайтов
    tiles_group.draw(screen)
    resource_tiles_group.draw(screen)
    player_group.draw(screen)
    player.rotate_towards_mouse()

    # рисуем выбранный блок (то что выбрано в меню)
    if mouse_x > 314 or mouse_y < WIDTH - 256:
        if type_of_current_block == 'mechanical drill':  # ДОРАБОТАТЬ!
            screen.blit(collected_mechanical_drill, (mouse_x - (mouse_x % 32), mouse_y - (mouse_y % 32)))
        elif type_of_current_block == 'pneumatic drill':
             pass

    # тут рисуем меню
    # ВНИМАНИЕ МИНИМАЛЬНЫЙ РАЗМЕР ЭКРАНА 260 пикселей
    screen.blit(menu, (0, HEIGHT - 254))
    if blocks_type == 'drills':
        screen.blit(drills_image, (4, HEIGHT - 250))

    if right_frame_pos is not None:
        screen.blit(frame, right_frame_pos)
    if top_left_frame_pos is not None:
        screen.blit(frame, top_left_frame_pos)
    if bottom_left_frame_pos is not None:
        screen.blit(frame, bottom_left_frame_pos)

    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        screen.blit(cursor, (mouse_x, mouse_y))

    pygame.display.flip()
    clock.tick(FPS)
