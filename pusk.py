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
    global core
    new_player, lvl_x, lvl_y = None, tile_width * len(level[0]), tile_height * len(level)
    resource_map = image_to_list(
        ['data/maps/resource_maps/resource_map_1.png', 'data/maps/resource_maps/resource_map_2.png'][
            index_of_selected_map])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if x != 0 and y != 0:
                if level[y][x] == (232, 120, 0):
                    for i in range(3):
                        for j in range(3):
                            Tile(player_pixel, x + i, y + j)
                    core = Core(load_image('cores/core_1.png'), x, y)
                    board.append(y, x, core, 3)
                elif level[y][x] in tiles_images:
                    Tile(level[y][x], x, y)
                elif level[y][x] == (136, 0, 21):  # r, g, b игрока
                    Tile(player_pixel, x, y)
                    new_player = (x, y)
                elif level[y][x] != (255, 0, 0):
                    Tile(player_pixel, x, y)
            else:
                Tile((0, 0, 0), x, y)
                board.industry_map[0][0] = 'blocked'

            if level[y][x] == (210, 174, 141) or level[y][x] == (60, 56, 56):
                board.resource_map[y][x] = 'sand'
            if level[y][x] in blocked_blocks:
                board.industry_map[y][x] = 'blocked'

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
    intro_text = [
        "",
        "Эта игра-песочница, в которой предстоит создать собственный завод по производству различных ресурсов",
        "Управление реализованно черз кнопки W -> Вперед, A -> Влево, S -> Назад, D -> Вправо",
        "Ваша задача - это копить ресурсы и готовить оброну. Ведь уже скоро пойдут враги, которые хотят забрать \
ваши ресурсы",
    ]

    fon = pygame.transform.scale(load_image('logo.png'), (674, 107))
    screen.blit(fon, (WIDTH // 2 - 337, 0))
    font = pygame.font.Font(None, 32)
    text_coord = 140
    text = font.render("Представляем вашему вниманию проект Sand Mile.", True, pygame.Color('black'))
    text_rect = text.get_rect(center=(WIDTH / 2, text_coord))
    screen.blit(text, text_rect)
    font = pygame.font.Font(None, 28)
    text_coord += 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    x, y = screen.get_size()
    width = 300
    height = 75
    btn_new_game = Button(
        color=(244, 169, 0),
        x=x // 2 - (width // 2),
        y=int(y * 0.75 - (height // 2)),
        width=width,
        height=height,
        text="Play"
    )
    btn_new_game.draw(screen)
    NEW_GAME = pygame.USEREVENT + 2
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == NEW_GAME:
                return

        if btn_new_game.box.collidepoint(pygame.mouse.get_pos()):
            pygame.event.post(pygame.event.Event(NEW_GAME))

        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    pygame.init()
    size = WIDTH, HEIGHT = 1280, 960
    screen = pygame.display.set_mode(size)
    screen.fill((125, 125, 125))
    cursor = pygame.image.load('data/cursor.png')
    # Не трогать пустую строку - это отступ от заставки
    res = core.resources
    intro_text = [
        "",
        "Ваши ресурсы:"
    ]
    for k, v in res.items():
        intro_text.append(f"{k} - {v}")
    fon = pygame.transform.scale(load_image('logo.png'), (674, 107))
    screen.blit(fon, (WIDTH // 2 - 337, 0))
    font = pygame.font.Font(None, 32)
    text_coord = 140
    text = font.render("Поздравляю с концом игры, надеюсь вам понравилось!", True, pygame.Color('black'))
    text_rect = text.get_rect(center=(WIDTH / 2, text_coord))
    screen.blit(text, text_rect)
    font = pygame.font.Font(None, 28)
    text_coord += 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    x, y = screen.get_size()
    width = 300
    height = 75
    btn_new_game = Button(
        color=(244, 169, 0),
        x=x // 2 - (width // 2),
        y=int(y * 0.75 - (height // 2)),
        width=width,
        height=height,
        text="Выход"
    )
    btn_new_game.draw(screen)
    END_GAME = pygame.USEREVENT + 2
    pygame.mouse.set_visible(True)
    # BUG: С кнопкой экран пояляется на 1 секунду и закрвыется
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            # elif event.type == END_GAME:
                # return

        if btn_new_game.box.collidepoint(pygame.mouse.get_pos()):
            pygame.event.post(pygame.event.Event(END_GAME))

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
    def __init__(self, pos_x, pos_y):  # pos_x и pos_y индексы на карте
        super().__init__(player_group, all_sprites)
        self.x = pos_x * tile_width
        self.y = pos_y * tile_height
        self.image = player_image
        self.is_in_motion = False
        self.health = 100
        self.rect = self.image.get_rect().move(self.x, self.y)
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


def get_pos_spawn_mark():
    for i in range(len(board.industry_map)):
        for j in range(len(board.industry_map[i])):
            if board.industry_map[i][j] == "spawn_mark":
                return i, j


def get_pos_core():
    for i in range(len(board.industry_map)):
        for j in range(len(board.industry_map[i])):
            if board.industry_map[i][j]:
                if isinstance(board.industry_map[i][j], Core):
                    return i, j


# TODO: сделать спавн в опр радиусе
# Пока в определом месте, потом пройдемся по карте и найдем место спавна
def spawn_enemy():
    y, x = get_pos_spawn_mark()
    units = [Dagger, Crawler, Nova]
    for _ in range(21):
        y_t, x_t = random.randint(y, y + 6), random.randint(x- 10, x + 6)
        random.choice(units)(x_t, y_t)


class Dagger(pygame.sprite.Sprite):
    def __init__(self, ind_x, ind_y):
        super().__init__(enemy_group, all_sprites)
        # self.hp = ???
        # self.damage = ???
        self.speed = 10
        self.damage = 10
        self.image = pygame.transform.scale(load_image("units/dagger.png"), (50, 50))
        self.orig = self.image
        self.rect = self.image.get_rect()
        self.ind_x = ind_x
        self.ind_y = ind_y
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.range()
        self.flag = True
        self.flag_check = False
        self.fn_left = None
        self.fn_right = None
        self.fn_top = None
        self.fn_bottom = None
        self.core = None
        self.template_x = self.rect.x
        self.template_y = self.rect.y
        self.target = None

    def update(self):
        core_x, core_y = get_pos_core()
        self.core = board.industry_map[core_x][core_y]
        self.move_to_base()
        self.rotate(core_x, core_y)
        self.range()
        # Range(self, 100).draw_range()

    def rotate(self, core_x, core_y):
        rel_x, rel_y = core_x - (self.rect[0] + self.rect[2] // 2), core_y - (self.rect[1] + self.rect[3] // 2)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.orig, int(angle) - 135)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_to_base(self):
        dx, dy = (self.core.rect.x + self.core.rect.w // 2 - (self.rect.x + self.rect.w // 2),
                  self.core.rect.y + self.core.rect.h // 2 - (self.rect.y + self.rect.h // 2))
        dist = (math.hypot(dx, dy))
        if dist < 150:
            return
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        if pygame.sprite.spritecollideany(self, invisible_group):
            if self.flag:
                self.flag = not self.flag
                self.fn_left = InvsibleFinder(self.rect.x, self.rect.y, -1000)
                self.fn_right = InvsibleFinder(self.rect.x, self.rect.y, 1000)
            if pygame.sprite.spritecollideany(self.fn_left, invisible_group):
                if self.fn_left.check_positon() and self.fn_left.check_positon():
                    if self.fn_left.rect.x > self.fn_right.rect.x:
                        dx, dy = (abs(self.rect.x - self.fn_left.rect.x) - self.rect.x,
                                  abs(self.rect.y - self.fn_left.rect.y) - self.rect.y)
                    else:
                        dx, dy = (abs(self.rect.x - self.fn_right.rect.x) - self.rect.x,
                                  abs(self.rect.y - self.fn_right.rect.y) - self.rect.y)
                    dist = (math.hypot(dx, dy))
                    if dist != 0:
                        dx, dy = dx / dist, dy / dist
                    self.rect.x += dx * self.speed
                    self.template_x += dx * self.speed
                    self.rect.y += dy * self.speed
                    self.template_y += dy * self.speed
        else:
            self.rect.x += dx * self.speed
            self.template_x += dx * self.speed
            self.rect.y += dy * self.speed
            self.template_y += dy * self.speed

    # BUG: Нужно убрать видимость круга
    # Пока сделанно он увидел строение, он остновился и как-бы начал атаковать
    def range(self):
        color = (100, 100, 100, 255)
        t = pygame.draw.circle(screen, color, (self.rect.center), 100, 1)
        for i in industry_tiles_group:
            if pygame.Rect.colliderect(i.rect, t):
                # i.hp -= self.damage
                self.speed = 0
                # if i.hp == 0:
                    # self.speed = 10

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        bullet_group.add(bullet)
        all_sprites.add(bullet)


class Crawler(pygame.sprite.Sprite):
    def __init__(self, ind_x, ind_y):
        super().__init__(enemy_group, all_sprites)
        self.speed = 10
        self.image = pygame.transform.scale(load_image("units/crawler.png"), (50, 50))
        self.orig = self.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.flag = True
        self.flag_check = False
        self.fn_left = None
        self.fn_right = None
        self.fn_top = None
        self.fn_bottom = None
        self.core = None

    def update(self):
        if t := pygame.sprite.spritecollideany(self, invisible_group):
            col_x = t.rect.x
            col_y = t.rect.y
            if col_x > self.rect.x:
                self.rect.x -= col_x - self.rect.x
            if col_x < self.rect.x:
                self.rect.x += self.rect.x - col_x
            # self.rect.x += self.rect.x + 0.5 * self.t
            # self.t *= -1
        core_x, core_y = get_pos_core()
        self.core = board.industry_map[core_x][core_y]
        self.move_to_base()
        self.rotate(core_x, core_y)

    def rotate(self, core_x, core_y):
        rel_x, rel_y = core_x - (self.rect[0] + self.rect[2] // 2), core_y - (self.rect[1] + self.rect[3] // 2)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.orig, int(angle) - 135)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_to_base(self):
        dx, dy = (self.core.rect.x + self.core.rect.w // 2 - (self.rect.x + self.rect.w // 2),
                  self.core.rect.y + self.core.rect.h // 2 - (self.rect.y + self.rect.h // 2))
        dist = (math.hypot(dx, dy))
        if dist < 150:
            return
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        if pygame.sprite.spritecollideany(self, invisible_group):
            if self.flag:
                self.flag = not self.flag
                self.fn_left = InvsibleFinder(self.rect.x, self.rect.y, -1000)
                self.fn_right = InvsibleFinder(self.rect.x, self.rect.y, 1000)
            if pygame.sprite.spritecollideany(self.fn_left, invisible_group):
                if self.fn_left.check_positon() and self.fn_left.check_positon():
                    if self.fn_left.rect.x > self.fn_right.rect.x:
                        dx, dy = (abs(self.rect.x - self.fn_left.rect.x) - self.rect.x,
                                  abs(self.rect.y - self.fn_left.rect.y) - self.rect.y)
                    else:
                        dx, dy = (abs(self.rect.x - self.fn_right.rect.x) - self.rect.x,
                                  abs(self.rect.y - self.fn_right.rect.y) - self.rect.y)
                    dist = (math.hypot(dx, dy))
                    if dist != 0:
                        dx, dy = dx / dist, dy / dist
                    self.rect.x += dx * self.speed
                    self.rect.y += dy * self.speed
        else:
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def attack(self, target):
        ...

    def range(self):
        color = (100, 100, 100, 255)
        t = pygame.draw.circle(screen, color, (self.rect.center), 100, 1)
        for i in industry_tiles_group:
            if pygame.Rect.colliderect(i.rect, t):
                # i.hp -= self.damage
                self.speed = 0
                # if i.hp == 0:
                    # self.speed = 10


class Nova(pygame.sprite.Sprite):
    def __init__(self, ind_x, ind_y):
        super().__init__(enemy_group, all_sprites)
        self.speed = 10
        self.image = pygame.transform.scale(load_image("units/nova.png"), (50, 50))
        self.orig = self.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.flag = True
        self.flag_check = False
        self.fn_left = None
        self.fn_right = None
        self.fn_top = None
        self.fn_bottom = None

    def update(self):
        if t := pygame.sprite.spritecollideany(self, invisible_group):
            col_x = t.rect.x
            col_y = t.rect.y
            if col_x > self.rect.x:
                self.rect.x -= col_x - self.rect.x
            if col_x < self.rect.x:
                self.rect.x += self.rect.x - col_x
            # self.rect.x += self.rect.x + 0.5 * self.t
            # self.t *= -1
        core_x, core_y = get_pos_core()
        self.core = board.industry_map[core_x][core_y]
        self.move_to_base()
        self.rotate(core_x, core_y)

    def rotate(self, core_x, core_y):
        rel_x, rel_y = core_x - (self.rect[0] + self.rect[2] // 2), core_y - (self.rect[1] + self.rect[3] // 2)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.orig, int(angle) - 135)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move_to_base(self):
        dx, dy = (self.core.rect.x + self.core.rect.w // 2 - (self.rect.x + self.rect.w // 2),
                  self.core.rect.y + self.core.rect.h // 2 - (self.rect.y + self.rect.h // 2))
        dist = (math.hypot(dx, dy))
        if dist < 150:
            return
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        if pygame.sprite.spritecollideany(self, invisible_group):
            if self.flag:
                self.flag = not self.flag
                self.fn_left = InvsibleFinder(self.rect.x, self.rect.y, -1000)
                self.fn_right = InvsibleFinder(self.rect.x, self.rect.y, 1000)
            if pygame.sprite.spritecollideany(self.fn_left, invisible_group):
                if self.fn_left.check_positon() and self.fn_left.check_positon():
                    if self.fn_left.rect.x > self.fn_right.rect.x:
                        dx, dy = (abs(self.rect.x - self.fn_left.rect.x) - self.rect.x,
                                  abs(self.rect.y - self.fn_left.rect.y) - self.rect.y)
                    else:
                        dx, dy = (abs(self.rect.x - self.fn_right.rect.x) - self.rect.x,
                                  abs(self.rect.y - self.fn_right.rect.y) - self.rect.y)
                    dist = (math.hypot(dx, dy))
                    if dist != 0:
                        dx, dy = dx / dist, dy / dist
                    self.rect.x += dx * self.speed
                    self.rect.y += dy * self.speed
        else:
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def range(self):
        color = (100, 100, 100, 255)
        t = pygame.draw.circle(screen, color, (self.rect.center), 100, 1)
        for i in industry_tiles_group:
            if pygame.Rect.colliderect(i.rect, t):
                # i.hp -= self.damage
                self.speed = 0
                # if i.hp == 0:
                    # self.speed = 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ind_x, ind_y, target):
        super().__init__(bullet_group, all_sprites)
        self.image = load_image("bullet.png")
        self.orig = self.image
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.x = ind_x
        self.rect.y = ind_y
        self.target = target


class InvsibleFinder(pygame.sprite.Sprite):
    def __init__(self, ind_x, ind_y, x):
        super().__init__(invisible_finder, all_sprites)
        self.image = pygame.transform.scale(load_image("bullet_invisible.png"), (25, 25))
        self.orig = self.image
        self.speed = 50
        self.rect = self.image.get_rect()
        self.rect.x = ind_x
        self.rect.y = ind_y
        self.delta_x = x

    def update(self):
        self.move_to(self.rect.x + self.delta_x, self.rect.y)

    def check_positon(self):
        if self.speed == 0:
            return True
        return False

    def move_to(self, x, y):
        dx, dy = (x - self.rect.x,
                  y - self.rect.y)
        dist = (math.hypot(dx, dy))
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        if pygame.sprite.spritecollideany(self, invisible_group):
            self.speed = 0


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.ogcol = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.box = None
        self.clicked = False

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        self.box = pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont("segoeuisymbol", 24)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


class InvisibleWall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(invisible_group, all_sprites)
        self.image = load_image("tiles/wall_blocks/dirt-wall2.png")
        self.rect = self.image.get_rect().move(tile_width * x, tile_height * y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = None
        if isinstance(tiles_images[tile_type], list):
            self.image = random.choice(tiles_images[tile_type])
        else:
            self.image = tiles_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class ResourceTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(resource_tiles_group, all_sprites)
        self.image = None
        if isinstance(ores_images[tile_type], list):
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
            soundtrack.play(self.soundtracks[self.index_of_sound])
            soundtrack.set_volume(0.75)
            self.index_of_sound = None


class Board:
    def __init__(self):
        # industry map отвечает за расположение логистических блоков (каждый блок занимает несколько клеток)
        self.industry_map = [[None for _ in range(len(lst_map[0]))] for __ in range(len(lst_map))]
        # тоже самое, только каждый блок занимает одну клетку во избежание повторного отрисовывания
        self.resource_map = [[None for _ in range(len(lst_map[0]))] for __ in range(len(lst_map))]

    def append(self, ind_1, ind_2, block, width):
        # добавляем класс block во все нужные клетки
        for siz in range(width):
            for high in range(width):
                self.industry_map[ind_1 + siz][ind_2 + high] = block

    def destroy(self, ind_1, ind_2, block):
        for h in range(len(self.industry_map)):
            for w in range(len(self.industry_map[0])):
                if self.industry_map[h][w] == block:
                    self.industry_map[h][w] = None


class DoubleTurret(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.orig_duo_turret = duo_turret.copy()
        self.health = 100
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.damage = 20
        self.width = 1  # отвечает за ширину блока в клетках
        self.direction = None

    def attack(self, obj):
        obj.decrease_health(self.damage)

    def logic_update(self):
        pass

    def decrease_health(self, a):
        self.health -= a
        if self.health <= 0:
            self.kill()

    def rotate_towards_units(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect[0] + self.rect[2] // 2), mouse_y - (self.rect[1] + self.rect[3] // 2)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        duo_turret_img = pygame.transform.rotate(self.orig_duo_turret, int(angle) - 90)
        duo_turret_rect = duo_turret_img.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
        self.image = block_1.copy()
        self.image.blit(duo_turret_img, duo_turret_rect.topleft)

    def update(self):
        self.rotate_towards_units()

    def can_take_resource(self, resource='', direction=''):
        return False

    def take_resource(self, resource, direction=''):
        pass


class ScatterTurret(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.orig_scatter_turret = scatter.copy()
        self.health = 100
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.damage = 20
        self.width = 2  # отвечает за ширину блока в клетках
        self.direction = None

    def attack(self, obj):
        obj.decrease_health(self.damage)

    def logic_update(self):
        pass

    def decrease_health(self, a):
        self.health -= a
        if self.health <= 0:
            self.kill()

    def rotate_towards_units(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect[0] + self.rect[2] // 2), mouse_y - (self.rect[1] + self.rect[3] // 2)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        scarret_turret_img = pygame.transform.rotate(self.orig_scatter_turret, int(angle) - 90)
        scarret_turret_rect = scarret_turret_img.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
        self.image = block_2.copy()
        self.image.blit(scarret_turret_img, scarret_turret_rect.topleft)

    def update(self):
        self.rotate_towards_units()

    def can_take_resource(self, resource='', direction=''):
        return False

    def take_resource(self, resource, direction=''):
        pass


class HailTurret(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.orig_hail_turret = hail.copy()
        self.health = 100
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.damage = 20
        self.width = 1  # отвечает за ширину блока в клетках
        self.direction = None

    def attack(self, obj):
        obj.decrease_health(self.damage)

    def logic_update(self):
        pass

    def decrease_health(self, a):
        self.health -= a
        if self.health <= 0:
            self.kill()

    def rotate_towards_units(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect[0] + self.rect[2] // 2), mouse_y - (self.rect[1] + self.rect[3] // 2)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        hail_turret_img = pygame.transform.rotate(self.orig_hail_turret, int(angle) - 90)
        hail_turret_rect = hail_turret_img.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
        self.image = block_1.copy()
        self.image.blit(hail_turret_img, hail_turret_rect.topleft)

    def update(self):
        self.rotate_towards_units()

    def can_take_resource(self, resource='', direction=''):
        return False

    def take_resource(self, resource, direction=''):
        pass


class SwarmerTurret(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.orig_scatter_turret = swarmer.copy()
        self.health = 100
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.damage = 20
        self.width = 2  # отвечает за ширину блока в клетках
        self.direction = None

    def attack(self, obj):
        obj.decrease_health(self.damage)

    def logic_update(self):
        pass

    def decrease_health(self, a):
        self.health -= a
        if self.health <= 0:
            self.kill()

    def rotate_towards_units(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - (self.rect[0] + self.rect[2] // 2), mouse_y - (self.rect[1] + self.rect[3] // 2)
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        swarmer_turret_img = pygame.transform.rotate(self.orig_scatter_turret, int(angle) - 90)
        swarmer_turret_rect = swarmer_turret_img.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
        self.image = block_2.copy()
        self.image.blit(swarmer_turret_img, swarmer_turret_rect.topleft)

    def update(self):
        self.rotate_towards_units()

    def can_take_resource(self, resource='', direction=''):
        return False

    def take_resource(self, resource, direction=''):
        pass


def frame_positions(pos1, pos2, pos3, *pos_mouse):
    global destroy, build, blocks_type, type_of_current_block, rotate_arrow, arrow_direction
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
            blocks_type = 'logistics blocks'
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
            blocks_type = 'defensive walls'
        elif 264 <= mouse_x <= 309 and HEIGHT - 97 <= mouse_y <= HEIGHT - 47:
            pos1 = (264, HEIGHT - 97)
            blocks_type = 'drone factories'

    # задействуем левую верхнюю часть меню (также выбор текущего блока)
    # По умолчанию будет включен первый блок при открытии любого раздела
    first_case = ['mechanical drill', 'pneumatic drill']
    second_case = ['conveyor', 'junction', 'router', 'distributor', 'overflow gate', 'underflow gate', 'sorter',
                   'bridge conveyor']
    third_case = ['double turret', 'scatter turret', 'hail turret', 'swarmer turret']
    if blocks_type == 'drills':
        if type_of_current_block not in first_case:
            type_of_current_block = 'mechanical drill'
            pos2 = (4, HEIGHT - 250)

        if 4 <= mouse_x <= 54 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'mechanical drill'
            pos2 = (4, HEIGHT - 250)
        elif 55 <= mouse_x <= 105 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'pneumatic drill'
            pos2 = (55, HEIGHT - 250)
    elif blocks_type == 'logistics blocks':
        if type_of_current_block not in second_case:
            type_of_current_block = 'conveyor'
            pos2 = (4, HEIGHT - 250)

        if 4 <= mouse_x <= 54 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'conveyor'
            pos2 = (4, HEIGHT - 250)
        elif 55 <= mouse_x <= 105 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'junction'
            pos2 = (55, HEIGHT - 250)
        elif 106 <= mouse_x <= 156 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'router'
            pos2 = (106, HEIGHT - 250)
        elif 157 <= mouse_x <= 207 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'distributor'
            pos2 = (157, HEIGHT - 250)

        if 4 <= mouse_x <= 54 and HEIGHT - 199 <= mouse_y <= HEIGHT - 149:
            type_of_current_block = 'overflow gate'
            pos2 = (4, HEIGHT - 199)
        elif 55 <= mouse_x <= 105 and HEIGHT - 199 <= mouse_y <= HEIGHT - 149:
            type_of_current_block = 'underflow gate'
            pos2 = (55, HEIGHT - 199)
        elif 106 <= mouse_x <= 156 and HEIGHT - 199 <= mouse_y <= HEIGHT - 149:
            type_of_current_block = 'sorter'
            pos2 = (106, HEIGHT - 199)
        elif 157 <= mouse_x <= 207 and HEIGHT - 199 <= mouse_y <= HEIGHT - 149:
            type_of_current_block = 'bridge conveyor'
            pos2 = (157, HEIGHT - 199)
    elif blocks_type == 'turrets':
        if type_of_current_block not in third_case:
            type_of_current_block = 'double turret'
            pos2 = (4, HEIGHT - 250)

        if 4 <= mouse_x <= 54 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'double turret'
            pos2 = (4, HEIGHT - 250)
        elif 55 <= mouse_x <= 105 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'scatter turret'
            pos2 = (55, HEIGHT - 250)
        elif 106 <= mouse_x <= 156 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'hail turret'
            pos2 = (106, HEIGHT - 250)
        elif 157 <= mouse_x <= 207 and HEIGHT - 250 <= mouse_y <= HEIGHT - 200:
            type_of_current_block = 'swarmer turret'
            pos2 = (157, HEIGHT - 250)
    else:
        pos2 = None

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

        if 106 <= mouse_x <= 156 and type_of_current_block == 'conveyor':
            if arrow_direction == 'east':
                arrow_direction = 'north'
            elif arrow_direction == 'north':
                arrow_direction = 'west'
            elif arrow_direction == 'west':
                arrow_direction = 'south'
            elif arrow_direction == 'south':
                arrow_direction = 'east'
            rotate_arrow = pygame.transform.rotate(rotate_arrow.copy(), 90)

    return pos1, pos2, pos3


class CursorFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = frame_33
        self.angle_of_rotating_frame = 0.0
        self.rect = self.image.get_rect().move(pygame.mouse.get_pos())
        self.orig = self.image.copy()

    def draw(self):
        if build:
            self.image = frame_33
        elif destroy:
            self.image = red_frame

        if build or destroy:
            rotated_image = pygame.transform.rotate(self.image, self.angle_of_rotating_frame)
            rotated_image_rect = rotated_image.get_rect(center=(mouse_x, mouse_y))
            screen.blit(rotated_image, rotated_image_rect.topleft)


class Core(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img
        self.rect = self.image.get_rect().move(ind_x * tile_width, ind_y * tile_height)
        self.hp = 250
        self.level = 1
        self.resources = {
            'coal': 0,
            'copper': 0,
            'graphite': 0,
            'lead': 0,
            'plastanium': 0,
            'pyratite': 0,
            'sand': 0,
            'scrap': 0,
            'silicon': 0,
            'surge-alloy': 0,
            'thorium': 0,
            "titanium": 0
        }
        self.width = 3  # отвечает за ширину блока в клетках
        self.direction = None

    def kill_myself(self):
        self.kill()

    def logic_update(self):
        pass

    def get_resources(self, *args, **kwargs):
        """Сюда передавать cловарь(строчка: кол-во ресурсов) или список(песок, медь, свинец). Данный метод будет
        принимать данные ресурсы и записывать к себе в словарь."""
        for el in args:
            self.resources[el] += 1
        for el in kwargs:
            self.resources[el] += kwargs[el]

    def update(self):
        pass

    def can_take_resource(self, resource='', direction=''):
        return True

    def take_resource(self, resource, direction=''):
        if resource is not None:
            self.resources[resource] += 1


class MechanicalDrill(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy

        self.angle = 0.0
        self.orig_rotate_img = rotator_mechanical_drill.copy()
        self.delta_rotating = 5.0
        self.width = 2  # отвечает за ширину блока в клетках
        self.speed_of_mining = 0.8
        try:
            tmp_1 = board.resource_map[ind_y][ind_x]
            tmp_2 = board.resource_map[ind_y][ind_x + 1]
            tmp_3 = board.resource_map[ind_y + 1][ind_x]
            tmp_4 = board.resource_map[ind_y + 1][ind_x + 1]
        except:
            print('С выбранным ресурсом что-то не так!')
        self.extraction_resource = random.choice([tmp_1, tmp_2, tmp_3, tmp_4])
        while self.extraction_resource is None:
            self.extraction_resource = random.choice([tmp_1, tmp_2, tmp_3, tmp_4])
        self.resources = {self.extraction_resource: 0}
        self.ind_x = ind_x
        self.ind_y = ind_y
        self.direction = None

        # считаем кол-во ресурсов под буром
        self.speed_of_mining = self.speed_of_mining * (self.width * 2 - [tmp_1, tmp_2, tmp_3, tmp_4].count(None)) / 4

        # эта штука под соседние клетки куда будем скидывать ресурсы
        self.lst_neighboring_cells = [(ind_x, ind_y - 1), (ind_x + 1, ind_y - 1), (ind_x - 1, ind_y),
                                      (ind_x + 2, ind_y), (ind_x - 1, ind_y + 1), (ind_x + 2, ind_y + 1),
                                      (ind_x, ind_y + 2), (ind_x + 1, ind_y + 2)]

    def update_draw(self):
        self.angle += self.delta_rotating
        rotated_img = pygame.transform.rotate(self.orig_rotate_img, self.angle)
        rotated_img_rect = rotated_img.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
        self.image.blit(base_mechanical_drill, (0, 0))
        self.image.blit(rotated_img, rotated_img_rect.topleft)
        self.image.blit(stub_mechanical_drill, (0, 0))

    def can_take_resource(self, resource='', direction=''):
        return False

    def logic_update(self):
        self.resources[self.extraction_resource] += self.speed_of_mining
        if self.resources[self.extraction_resource] > 20:
            self.resources[self.extraction_resource] = 20

        if self.resources[self.extraction_resource] > 0:
            cur_blocks = []
            for x, y in self.lst_neighboring_cells:
                if board.industry_map[y][x] is not None and type(board.industry_map[y][x]) is not str:
                    if board.industry_map[y][x].can_take_resource('', ''):
                        if type(board.industry_map[y][x]) is Conveyor:
                            if y < self.ind_y and board.industry_map[y][x].direction == 'south':
                                continue
                            if y > self.ind_y + 1 and board.industry_map[y][x].direction == 'north':
                                continue
                            if x < self.ind_x and board.industry_map[y][x].direction == 'east':
                                continue
                            if x > self.ind_x + 1 and board.industry_map[y][x].direction == 'west':
                                continue

                        cur_blocks.append(board.industry_map[y][x])

            if cur_blocks:
                block = random.choice(cur_blocks)
                if self.resources[self.extraction_resource] >= 1:
                    block.take_resource(self.extraction_resource)
                    self.resources[self.extraction_resource] -= 1

    def update(self):
        self.update_draw()


class PneumaticDrill(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy

        self.angle = 0.0
        self.orig_rotate_img = rotator_pneumatic_drill.copy()
        self.delta_rotating = 5.0
        self.width = 2  # отвечает за ширину блока в клетках
        self.speed_of_mining = 1.4
        try:
            tmp_1 = board.resource_map[ind_y][ind_x]
            tmp_2 = board.resource_map[ind_y][ind_x + 1]
            tmp_3 = board.resource_map[ind_y + 1][ind_x]
            tmp_4 = board.resource_map[ind_y + 1][ind_x + 1]
        except:
            print('С выбранным ресурсом что-то не так!')
        self.extraction_resource = random.choice([tmp_1, tmp_2, tmp_3, tmp_4])
        while self.extraction_resource is None:
            self.extraction_resource = random.choice([tmp_1, tmp_2, tmp_3, tmp_4])
        self.resources = {self.extraction_resource: 0}
        self.ind_x = ind_x
        self.ind_y = ind_y
        self.direction = None

        # считаем кол-во ресурсов под буром
        self.speed_of_mining = self.speed_of_mining * (self.width * 2 - [tmp_1, tmp_2, tmp_3, tmp_4].count(None)) / 4

        # эта штука под соседние клетки куда будем скидывать ресурсы
        self.lst_neighboring_cells = [(ind_x, ind_y - 1), (ind_x + 1, ind_y - 1), (ind_x - 1, ind_y),
                                      (ind_x + 2, ind_y), (ind_x - 1, ind_y + 1), (ind_x + 2, ind_y + 1),
                                      (ind_x, ind_y + 2), (ind_x + 1, ind_y + 2)]

    def update_draw(self):
        self.angle += self.delta_rotating
        rotated_img = pygame.transform.rotate(self.orig_rotate_img, self.angle)
        rotated_img_rect = rotated_img.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
        self.image.blit(base_pneumatic_drill, (0, 0))
        self.image.blit(rotated_img, rotated_img_rect.topleft)
        self.image.blit(stub_pneumatic_drill, (0, 0))

    def can_take_resource(self, resource='', direction=''):
        return False

    def logic_update(self):
        self.resources[self.extraction_resource] += self.speed_of_mining
        if self.resources[self.extraction_resource] > 20:
            self.resources[self.extraction_resource] = 20

        if self.resources[self.extraction_resource] > 0:
            cur_blocks = []
            for x, y in self.lst_neighboring_cells:
                if board.industry_map[y][x] is not None and type(board.industry_map[y][x]) is not str:
                    if board.industry_map[y][x].can_take_resource('', ''):
                        if type(board.industry_map[y][x]) is Conveyor:
                            if y < self.ind_y and board.industry_map[y][x].direction == 'south':
                                continue
                            if y > self.ind_y + 1 and board.industry_map[y][x].direction == 'north':
                                continue
                            if x < self.ind_x and board.industry_map[y][x].direction == 'east':
                                continue
                            if x > self.ind_x + 1 and board.industry_map[y][x].direction == 'west':
                                continue

                        cur_blocks.append(board.industry_map[y][x])

            if cur_blocks:
                block = random.choice(cur_blocks)
                if self.resources[self.extraction_resource] >= 1:
                    block.take_resource(self.extraction_resource)
                    self.resources[self.extraction_resource] -= 1

    def update(self):
        self.update_draw()


class Conveyor(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y, direction):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.width = 1
        self.anim_images = [conveyor_0, conveyor_1, conveyor_2, conveyor_3]
        self.resources = [None, None]
        # направление - north, south, west and east
        self.direction = direction
        self.ind_x = ind_x
        self.ind_y = ind_y
        self.zick_zack = False

    def update_draw(self):
        self.image = self.anim_images[current_anim_img_conv].copy()
        if self.direction == 'north':
            self.image = pygame.transform.rotate(self.image.copy(), 90)
        elif self.direction == 'west':
            self.image = pygame.transform.rotate(self.image.copy(), 180)
        elif self.direction == 'south':
            self.image = pygame.transform.rotate(self.image.copy(), 270)

        for i in range(len(self.resources)):
            template_img_resource = None
            if self.resources[i] == 'copper':
                template_img_resource = copper.copy()
            elif self.resources[i] == 'coal':
                template_img_resource = coal.copy()
            elif self.resources[i] == 'lead':
                template_img_resource = lead.copy()
            elif self.resources[i] == 'sand':
                template_img_resource = sand.copy()
            elif self.resources[i] == 'graphite':
                template_img_resource = graphite.copy()
            elif self.resources[i] == 'thorium':
                template_img_resource = thorium.copy()
            elif self.resources[i] == 'surge-alloy':
                template_img_resource = surge_alloy.copy()
            elif self.resources[i] == 'plastanium':
                template_img_resource = plastanium.copy()
            elif self.resources[i] == 'pyratite':
                template_img_resource = pyratite.copy()
            elif self.resources[i] == 'scrap':
                template_img_resource = scrap.copy()
            elif self.resources[i] == 'silicon':
                template_img_resource = silicon.copy()
            elif self.resources[i] == 'titanium':
                template_img_resource = titanium.copy()

            res_x, res_y = i * 9, 5
            if i == 0:
                res_x -= 2
            elif i == 1:
                res_x += 2

            if self.direction == 'north':
                res_x, res_y = 5, 0
                if i == 0:
                    res_y = 11
                elif i == 1:
                    res_y = -2
            elif self.direction == 'west':
                res_x, res_y = 0, 5
                if i == 0:
                    res_x = 11
                elif i == 1:
                    res_x = -2
            elif self.direction == 'south':
                res_x, res_y = 5, 0
                if i == 0:
                    res_y = -2
                elif i == 1:
                    res_y = 11

            if template_img_resource is not None:
                self.image.blit(template_img_resource, (res_x, res_y))

    def update(self):
        self.update_draw()

    def can_take_resource(self, resource='', direction=''):
        if self.resources[0] is not None:
            return False
        if direction == 'east' and self.direction == 'west':
            return False
        if direction == 'north' and self.direction == 'south':
            return False
        if direction == 'south' and self.direction == 'north':
            return False
        if direction == 'west' and self.direction == 'east':
            return False
        return True

    def logic_update(self):
        if self.zick_zack:
            if self.resources[1] is None:
                self.resources[1] = self.resources[0]
                self.resources[0] = None
        else:
            if self.direction == 'north':
                if (type(board.industry_map[self.ind_y - 1][self.ind_x]) is not str and
                        board.industry_map[self.ind_y - 1][self.ind_x] is not None):
                    if board.industry_map[self.ind_y - 1][self.ind_x].can_take_resource('', self.direction):
                        board.industry_map[self.ind_y - 1][self.ind_x].take_resource(self.resources[-1], self.direction)
                        self.resources[-1] = None
            if self.direction == 'east':
                if (type(board.industry_map[self.ind_y][self.ind_x + 1]) is not str and
                        board.industry_map[self.ind_y][self.ind_x + 1] is not None):
                    if board.industry_map[self.ind_y][self.ind_x + 1].can_take_resource('', self.direction):
                        board.industry_map[self.ind_y][self.ind_x + 1].take_resource(self.resources[-1], self.direction)
                        self.resources[-1] = None
            if self.direction == 'south':
                if (type(board.industry_map[self.ind_y + 1][self.ind_x]) is not str and
                        board.industry_map[self.ind_y + 1][self.ind_x] is not None):
                    if board.industry_map[self.ind_y + 1][self.ind_x].can_take_resource('', self.direction):
                        board.industry_map[self.ind_y + 1][self.ind_x].take_resource(self.resources[-1], self.direction)
                        self.resources[-1] = None
            if self.direction == 'west':
                if (type(board.industry_map[self.ind_y][self.ind_x - 1]) is not str and
                        board.industry_map[self.ind_y][self.ind_x - 1] is not None):
                    if board.industry_map[self.ind_y][self.ind_x - 1].can_take_resource('', self.direction):
                        board.industry_map[self.ind_y][self.ind_x - 1].take_resource(self.resources[-1], self.direction)
                        self.resources[-1] = None

        self.zick_zack = not self.zick_zack

    def take_resource(self, resource, direction=''):
        if resource is not None:
            self.resources[0] = resource


class Junction(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.width = 1
        self.ind_x = ind_x
        self.ind_y = ind_y

        # нет направления
        self.direction = None
        self.res_north_to_south = None
        self.res_south_to_north = None
        self.res_west_to_east = None
        self.res_east_to_west = None

    def update(self):
        pass

    def can_take_resource(self, resource='', direction=''):
        if direction == '':
            return False
        elif direction == 'north' and self.res_south_to_north is not None:
            return False
        elif direction == 'south' and self.res_north_to_south is not None:
            return False
        elif direction == 'east' and self.res_west_to_east is not None:
            return False
        elif direction == 'west' and self.res_east_to_west is not None:
            return False

        return True

    def take_resource(self, resource, direction=''):
        if resource is not None:
            if direction == 'north':
                self.res_south_to_north = resource
            elif direction == 'south':
                self.res_north_to_south = resource
            elif direction == 'west':
                self.res_east_to_west = resource
            elif direction == 'east':
                self.res_west_to_east = resource

    def logic_update(self):
        if self.res_east_to_west is not None:
            if (board.industry_map[self.ind_y][self.ind_x - 1] is not None and
                    type(board.industry_map[self.ind_y][self.ind_x - 1]) is not str):
                if board.industry_map[self.ind_y][self.ind_x - 1].can_take_resource('', 'west'):
                    board.industry_map[self.ind_y][self.ind_x - 1].take_resource(self.res_east_to_west, 'west')
                    self.res_east_to_west = None

        if self.res_north_to_south is not None:
            if (board.industry_map[self.ind_y + 1][self.ind_x] is not None and
                    type(board.industry_map[self.ind_y + 1][self.ind_x]) is not str):
                if board.industry_map[self.ind_y + 1][self.ind_x].can_take_resource('', 'south'):
                    board.industry_map[self.ind_y + 1][self.ind_x].take_resource(self.res_north_to_south, 'south')
                    self.res_north_to_south = None

        if self.res_south_to_north is not None:
            if (board.industry_map[self.ind_y - 1][self.ind_x] is not None and
                    type(board.industry_map[self.ind_y - 1][self.ind_x]) is not str):
                if board.industry_map[self.ind_y - 1][self.ind_x].can_take_resource('', 'north'):
                    board.industry_map[self.ind_y - 1][self.ind_x].take_resource(self.res_south_to_north, 'north')
                    self.res_south_to_north = None

        if self.res_west_to_east is not None:
            if (board.industry_map[self.ind_y][self.ind_x + 1] is not None and
                    type(board.industry_map[self.ind_y][self.ind_x + 1]) is not str):
                if board.industry_map[self.ind_y][self.ind_x + 1].can_take_resource('', 'east'):
                    board.industry_map[self.ind_y][self.ind_x + 1].take_resource(self.res_west_to_east, 'east')
                    self.res_west_to_east = None


class Router(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.width = 1

        self.resources = [None]
        self.direction = None
        # направления куда маршрутизатор будет выводить
        # пока что с погрешностью
        self.directions = []
        self.ind_x = ind_x
        self.ind_y = ind_y
        self.update_directions()
        self.current_direction = 0

    def update_directions(self):
        """Добавляет в список directions направления куда будет выводить ресурсы.
        Проверка на can_take_resource обязательна."""
        if board.industry_map[self.ind_y - 1][self.ind_x] is not None and type(
                board.industry_map[self.ind_y - 1][self.ind_x]) is not str:
            if board.industry_map[self.ind_y - 1][self.ind_x].direction != 'south':
                if 'north' not in self.directions:
                    self.directions.append('north')
        if board.industry_map[self.ind_y + 1][self.ind_x] is not None and type(
                board.industry_map[self.ind_y + 1][self.ind_x]) is not str:
            if board.industry_map[self.ind_y + 1][self.ind_x].direction != 'north':
                if 'south' not in self.directions:
                    self.directions.append('south')
        if board.industry_map[self.ind_y][self.ind_x - 1] is not None and type(
                board.industry_map[self.ind_y][self.ind_x - 1]) is not str:
            if board.industry_map[self.ind_y][self.ind_x - 1].direction != 'east':
                if 'west' not in self.directions:
                    self.directions.append('west')
        if board.industry_map[self.ind_y][self.ind_x + 1] is not None and type(
                board.industry_map[self.ind_y][self.ind_x + 1]) is not str:
            if board.industry_map[self.ind_y][self.ind_x + 1].direction != 'west':
                if 'east' not in self.directions:
                    self.directions.append('east')

    def update(self):
        pass

    def logic_update(self):
        self.update_directions()
        if len(self.directions) > 0:
            self.current_direction = random.randint(0, len(self.directions) - 1)

            if self.directions[self.current_direction] == 'east':
                if board.industry_map[self.ind_y][self.ind_x + 1] is not None and type(
                        board.industry_map[self.ind_y][self.ind_x + 1]) is not str:
                    if board.industry_map[self.ind_y][self.ind_x + 1].can_take_resource(self.resources[0], 'east'):
                        board.industry_map[self.ind_y][self.ind_x + 1].take_resource(self.resources[0], 'east')
                        self.resources[0] = None
            if self.directions[self.current_direction] == 'north':
                if board.industry_map[self.ind_y - 1][self.ind_x] is not None and type(
                        board.industry_map[self.ind_y - 1][self.ind_x]) is not str:
                    if board.industry_map[self.ind_y - 1][self.ind_x].can_take_resource(self.resources[0], 'north'):
                        board.industry_map[self.ind_y - 1][self.ind_x].take_resource(self.resources[0], 'north')
                        self.resources[0] = None
            if self.directions[self.current_direction] == 'south':
                if board.industry_map[self.ind_y + 1][self.ind_x] is not None and type(
                        board.industry_map[self.ind_y + 1][self.ind_x]) is not str:
                    if board.industry_map[self.ind_y + 1][self.ind_x].can_take_resource(self.resources[0], 'south'):
                        board.industry_map[self.ind_y + 1][self.ind_x].take_resource(self.resources[0], 'south')
                        self.resources[0] = None
            if self.directions[self.current_direction] == 'west':
                if board.industry_map[self.ind_y][self.ind_x - 1] is not None and type(
                        board.industry_map[self.ind_y][self.ind_x - 1]) is not str:
                    if board.industry_map[self.ind_y][self.ind_x - 1].can_take_resource(self.resources[0], 'west'):
                        board.industry_map[self.ind_y][self.ind_x - 1].take_resource(self.resources[0], 'west')
                        self.resources[0] = None

    def can_take_resource(self, resource='', direction=''):
        if self.resources[0] is not None:
            return False
        return True

    def take_resource(self, resource, direction=''):
        if resource is not None:
            self.resources[0] = resource


class Distributor(pygame.sprite.Sprite):
    def __init__(self, img, ind_x, ind_y):
        super().__init__(industry_tiles_group, all_sprites)
        self.image = img.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = WIDTH // 2 - template_player_x % 32, HEIGHT // 2 - template_player_y % 32
        dx = (ind_x - index_player_x) * tile_width
        dy = (ind_y - index_player_y) * tile_height
        self.rect.x += dx
        self.rect.y += dy
        self.width = 2
        self.direction = None

    def update(self):
        pass

    def can_take_resource(self, resource='', direction=''):
        return False

    def take_resource(self, resource, direction=''):
        pass


pygame.init()
pygame.mixer.init()

# ВНИМАНИЕ МИНИМАЛЬНЫЙ РАЗМЕР ЭКРАНА 260 пикселей
size = WIDTH, HEIGHT = 1280, 960
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sand Mile')
clock = pygame.time.Clock()

tile_width = tile_height = 32
STEP = 7
FPS = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
resource_tiles_group = pygame.sprite.Group()
industry_tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
invisible_group = pygame.sprite.Group()
invisible_finder = pygame.sprite.Group()
ranges_group = pygame.sprite.Group()

cursor = pygame.image.load('data/cursor.png')
menu = pygame.image.load('data/menu/item_menu.png')
resources_menu = pygame.image.load('data/menu/resource_panel.png')
frame = pygame.image.load('data/menu/frame.png')
red_frame = pygame.image.load('data/menu/red-frame-33-33.png')
frame_33 = pygame.image.load('data/menu/frame-33-33.png')
drills_image = pygame.image.load('data/menu/menu_drills.png')
logistics_blocks_image = pygame.image.load('data/menu/menu_logistics_blocks.png')
collected_mechanical_drill = pygame.image.load('data/drills/collected_mechanical_drill.png')
collected_pneumatic_drill = pygame.image.load('data/drills/collected_pneumatic_drill.png')
rotator_mechanical_drill = pygame.image.load('data/drills/mechanical-drill-rotator.png')
rotator_pneumatic_drill = pygame.image.load('data/drills/pneumatic-drill-rotator.png')
stub_mechanical_drill = pygame.image.load('data/drills/mechanical-drill-top.png')
stub_pneumatic_drill = pygame.image.load('data/drills/pneumatic-drill-top.png')
turrets_image = pygame.image.load('data/menu/menu_turrets.png')
rotate_arrow = pygame.image.load('data/menu/rotate-arrow.png')

block_1 = pygame.image.load('data/turrets/base_block/block-1.png')
duo_turret = pygame.image.load('data/turrets/top_part/duo-turret-top.png')
block_2 = pygame.image.load('data/turrets/base_block/block-2.png')
scatter = pygame.image.load('data/turrets/top_part/scatter-top.png')
hail = pygame.image.load('data/turrets/top_part/hail-top.png')
swarmer = pygame.image.load('data/turrets/top_part/swarmer-top.png')
base_mechanical_drill = pygame.image.load('data/drills/mechanical-drill.png')
base_pneumatic_drill = pygame.image.load('data/drills/pneumatic-drill.png')

conveyor_0 = pygame.image.load('data/logistics_blocks/conveyor-0-0.png')
conveyor_1 = pygame.image.load('data/logistics_blocks/conveyor-0-1.png')
conveyor_2 = pygame.image.load('data/logistics_blocks/conveyor-0-2.png')
conveyor_3 = pygame.image.load('data/logistics_blocks/conveyor-0-3.png')
bridge_conveyor = pygame.image.load('data/logistics_blocks/bridge_conveyor.png')
distributor = pygame.image.load('data/logistics_blocks/distributor.png')
inverted_sorter = pygame.image.load('data/logistics_blocks/inverted_sorter.png')
junction = pygame.image.load('data/logistics_blocks/junction.png')
overflow_gate = pygame.image.load('data/logistics_blocks/overflow_gate.png')
router = pygame.image.load('data/logistics_blocks/router.png')
sorter = pygame.image.load('data/logistics_blocks/sorter.png')
underflow_gate = pygame.image.load('data/logistics_blocks/underflow_gate.png')

coal = pygame.transform.scale(pygame.image.load('data/resources/coal.png'), (22, 22))
copper = pygame.transform.scale(pygame.image.load('data/resources/copper.png'), (22, 22))
graphite = pygame.transform.scale(pygame.image.load('data/resources/graphite.png'), (22, 22))
lead = pygame.transform.scale(pygame.image.load('data/resources/lead.png'), (22, 22))
plastanium = pygame.transform.scale(pygame.image.load('data/resources/plastanium.png'), (22, 22))
pyratite = pygame.transform.scale(pygame.image.load('data/resources/pyratite.png'), (22, 22))
sand = pygame.transform.scale(pygame.image.load('data/resources/sand.png'), (22, 22))
scrap = pygame.transform.scale(pygame.image.load('data/resources/scrap.png'), (22, 22))
silicon = pygame.transform.scale(pygame.image.load('data/resources/silicon.png'), (22, 22))
surge_alloy = pygame.transform.scale(pygame.image.load('data/resources/surge-alloy.png'), (22, 22))
thorium = pygame.transform.scale(pygame.image.load('data/resources/thorium.png'), (22, 22))
titanium = pygame.transform.scale(pygame.image.load('data/resources/titanium.png'), (22, 22))

coal_for_menu = pygame.image.load('data/resources/coal.png')
cooper_for_menu = pygame.image.load('data/resources/copper.png')
grahite_for_menu = pygame.image.load('data/resources/graphite.png')
lead_for_menu = pygame.image.load('data/resources/lead.png')
plastanium_for_menu = pygame.image.load('data/resources/plastanium.png')
pyratite_for_menu = pygame.image.load('data/resources/pyratite.png')
sand_for_menu = pygame.image.load('data/resources/sand.png')
scrap_for_menu = pygame.image.load('data/resources/scrap.png')
silicon_for_menu = pygame.image.load('data/resources/silicon.png')
surge_alloy_for_menu = pygame.image.load('data/resources/surge-alloy.png')
thorium_for_menu = pygame.image.load('data/resources/thorium.png')
titanium_for_menu = pygame.image.load('data/resources/titanium.png')

right_frame_pos, top_left_frame_pos, bottom_left_frame_pos = None, None, None
blocks_type = None
type_of_current_block = None
current_anim_img_conv = 0
build, destroy = False, False
is_there_arrow = False
arrow_direction = 'east'

# r, g, b для каждого tile
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

# r, g, b
blocked_blocks = [(0, 0, 0), (196, 100, 64), (141, 141, 141), (120, 101, 92), (130, 125, 233), (126, 38, 66),
                  (218, 181, 96), (92, 86, 122),
                  (69, 32, 32), (174, 180, 196), (225, 228, 201), (153, 94, 154), (82, 82, 92), (146, 94, 70)]

tile_wall = [
    (196, 100, 64),
    (141, 141, 141),
    (120, 101, 92),
    (130, 125, 233),
    (126, 38, 66),
    (218, 181, 96),
    (69, 32, 32),
    (174, 180, 196),
    (225, 228, 201),
    (92, 86, 122),
    (225, 233, 240),
    (153, 94, 154),
    (82, 82, 92),
    (146, 94, 70),
]

# r, g, b
blocked_blocks = [(0, 0, 0), (196, 100, 64), (141, 141, 141), (120, 101, 92), (130, 125, 233), (126, 38, 66),
                  (218, 181, 96),
                  (69, 32, 32), (174, 180, 196), (225, 228, 201), (153, 94, 154), (82, 82, 92), (146, 94, 70)]

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

# словарь, переводящий тип блока в его ширину
type_of_current_block_to_width = {
    'mechanical drill': 2,
    'conveyor': 1,
    'junction': 1,
    'router': 1,
    'distributor': 2,
    'overflow gate': 1,
    'underflow gate': 1,
    'sorter': 1,
    'bridge conveyor': 1,
    'pneumatic drill': 2,
    'double turret': 1,
    'scatter turret': 2,
    'hail turret': 1,
    'swarmer turret': 2
}

resources_coordinates = {
    'coal': [coal_for_menu, (315, HEIGHT - 120)],
    'copper': [cooper_for_menu, (315, HEIGHT - 80)],
    'graphite': [grahite_for_menu, (315, HEIGHT - 40)],
    'lead': [lead_for_menu, (425, HEIGHT - 120)],
    'plastanium': [plastanium_for_menu, (425, HEIGHT - 80)],
    'pyratite': [pyratite_for_menu, (425, HEIGHT - 40)],
    'sand': [sand_for_menu, (535, HEIGHT - 120)],
    'scrap': [scrap_for_menu, (535, HEIGHT - 80)],
    'silicon': [silicon_for_menu, (535, HEIGHT - 40)],
    'surge-alloy': [surge_alloy_for_menu, (645, HEIGHT - 120)],
    'thorium': [thorium_for_menu, (645, HEIGHT - 80)],
    'titanium': [titanium_for_menu, (645, HEIGHT - 40)]
}

index_of_selected_map = random.choice([0, 1])
# пиксель под игрока
player_pixel = image_to_list(['data/maps/snow_map_1.png', 'data/maps/sand_map_2.png'][index_of_selected_map])[0][0]
# Для работы с картами
map_name = ['data/maps/snow_map_1.png', 'data/maps/sand_map_2.png'][index_of_selected_map]
lst_map = image_to_list(map_name)

dj = DJ()
# представления о игровой доске лежат в board
board = Board()
camera = Camera()
cursor_frame = CursorFrame()
core = None

# ВАЖНО: PLAYER всегда должен находиться над пикселем ядра(пометка для создания карт)
# (136, 0, 21): player
# цвет игрока обязан присутствовать на поле
# (255, 0, 0): blocked
player_image = pygame.transform.scale(load_image('units/alpha.png'), (45, 40))
player_image_in_move = pygame.transform.scale(load_image('units/alpha_with_light.png'), (45, 74))
player_x, player_y, level_x, level_y = generate_level(lst_map)
player = Player(player_x, player_y)
template_player_x, template_player_y = player.rect.x + player.rect.w // 2, player.rect.y + player.rect.h // 2
index_player_x, index_player_y = template_player_x // 32, template_player_y // 32
pygame.mixer.set_num_channels(10)
soundtrack = pygame.mixer.Channel(2)
start_screen()

SPAWN_ENEMY = pygame.USEREVENT + 1
flag = True
flag_exit = False
pygame.time.set_timer(SPAWN_ENEMY, 100)
CHANGE_CONVEYOR_ANIM = pygame.USEREVENT + 2
pygame.time.set_timer(CHANGE_CONVEYOR_ANIM, 50)
LOGIC_UPDATE = pygame.USEREVENT + 3
pygame.time.set_timer(LOGIC_UPDATE, 1000)
LOGIC_UPDATE_CONVEYOR = pygame.USEREVENT + 4
pygame.time.set_timer(LOGIC_UPDATE_CONVEYOR, 100)
LOGIC_UPDATE_JUNCTION = pygame.USEREVENT + 5
pygame.time.set_timer(LOGIC_UPDATE_JUNCTION, 75)
LOGIC_UPDATE_ROUTER = pygame.USEREVENT + 6
pygame.time.set_timer(LOGIC_UPDATE_ROUTER, 100)

while True:
    screen.fill((0, 0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # индексы персонажа относительно карты
    index_player_x, index_player_y = template_player_x // 32, template_player_y // 32
    # индексы мышки относительно карты
    index_mouse_x = math.floor((template_player_x + mouse_x - WIDTH / 2) / 32)
    index_mouse_y = math.floor((template_player_y + mouse_y - HEIGHT / 2) / 32)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == CHANGE_CONVEYOR_ANIM:
            current_anim_img_conv = (current_anim_img_conv + 1) % 4
        if event.type == LOGIC_UPDATE:
            for el in industry_tiles_group:
                if type(el) is PneumaticDrill or type(el) is MechanicalDrill:
                    el.logic_update()
        if event.type == LOGIC_UPDATE_CONVEYOR:
            for el in industry_tiles_group:
                if type(el) is Conveyor:
                    el.logic_update()
        if event.type == LOGIC_UPDATE_JUNCTION:
            for el in industry_tiles_group:
                if type(el) is Junction:
                    el.logic_update()
        if event.type == LOGIC_UPDATE_ROUTER:
            for el in industry_tiles_group:
                if type(el) is Router:
                    el.logic_update()

        if event.type == SPAWN_ENEMY and flag:
            flag = False
            spawn_enemy()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            flag_exit = True
            break
        if event.type == CHANGE_CONVEYOR_ANIM:
            current_anim_img_conv = (current_anim_img_conv + 1) % 4
        if event.type == LOGIC_UPDATE:
            for el in industry_tiles_group:
                if type(el) is PneumaticDrill or type(el) is MechanicalDrill:
                    el.logic_update()
        if event.type == LOGIC_UPDATE_CONVEYOR:
            for el in industry_tiles_group:
                if type(el) is Conveyor:
                    el.logic_update()
        if event.type == LOGIC_UPDATE_JUNCTION:
            for el in industry_tiles_group:
                if type(el) is Junction:
                    el.logic_update()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # лкм
            right_frame_pos, top_left_frame_pos, bottom_left_frame_pos = frame_positions(right_frame_pos,
                                                                                         top_left_frame_pos,
                                                                                         bottom_left_frame_pos,
                                                                                         *pygame.mouse.get_pos())

            if (build and (mouse_x > 320 or mouse_y < HEIGHT - 260) and blocks_type is not None
                    and not player.is_in_motion):
                can_build_cur_block = True
                is_there_resources = False
                tmp_width_cur_block = type_of_current_block_to_width[type_of_current_block]

                for i in range(tmp_width_cur_block):
                    for j in range(tmp_width_cur_block):
                        if board.resource_map[index_mouse_y + j][index_mouse_x + i] is not None:
                            is_there_resources = True
                    if is_there_resources:
                        break

                for i in range(tmp_width_cur_block):
                    for j in range(tmp_width_cur_block):
                        if board.industry_map[index_mouse_y + i][index_mouse_x + j] is not None:
                            can_build_cur_block = False

                if can_build_cur_block:
                    tmp_class_cur_block = None
                    if is_there_resources:
                        if type_of_current_block == 'mechanical drill':
                            tmp_class_cur_block = MechanicalDrill(base_mechanical_drill, index_mouse_x, index_mouse_y)
                        elif type_of_current_block == 'pneumatic drill':
                            tmp_class_cur_block = PneumaticDrill(base_pneumatic_drill, index_mouse_x, index_mouse_y)

                    if type_of_current_block == 'double turret':
                        tmp_class_cur_block = DoubleTurret(block_1, index_mouse_x, index_mouse_y)
                    elif type_of_current_block == 'scatter turret':
                        tmp_class_cur_block = ScatterTurret(block_2, index_mouse_x, index_mouse_y)
                    elif type_of_current_block == 'hail turret':
                        tmp_class_cur_block = HailTurret(block_1, index_mouse_x, index_mouse_y)
                    elif type_of_current_block == 'swarmer turret':
                        tmp_class_cur_block = SwarmerTurret(block_2, index_mouse_x, index_mouse_y)

                    if type_of_current_block == 'conveyor':
                        tmp_class_cur_block = Conveyor(conveyor_0, index_mouse_x, index_mouse_y, arrow_direction)
                    elif type_of_current_block == 'router':
                        tmp_class_cur_block = Router(router, index_mouse_x, index_mouse_y)
                    elif type_of_current_block == 'junction':
                        tmp_class_cur_block = Junction(junction, index_mouse_x, index_mouse_y)
                    elif type_of_current_block == 'distributor':
                        tmp_class_cur_block = Distributor(distributor, index_mouse_x, index_mouse_y)

                    if tmp_class_cur_block is not None:
                        board.append(index_mouse_y, index_mouse_x, tmp_class_cur_block, tmp_width_cur_block)

            if (destroy and (mouse_x > 320 or mouse_y < HEIGHT - 260) and
                    type(board.industry_map[index_mouse_y][index_mouse_x]) is not Core):
                if board.industry_map[index_mouse_y][index_mouse_x] is not None:
                    board.industry_map[index_mouse_y][index_mouse_x].kill()
                    board.destroy(index_mouse_y, index_mouse_x, board.industry_map[index_mouse_y][index_mouse_x])

    # перемещение персонажа
    player.is_in_motion = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.is_in_motion = True
        template_player_x -= 5
        for i in range(5):
            player.rect.x -= STEP / 5
    if keys[pygame.K_d]:
        player.is_in_motion = True
        template_player_x += 5
        for i in range(5):
            player.rect.x += STEP / 5
    if keys[pygame.K_w]:
        player.is_in_motion = True
        template_player_y -= 5
        for i in range(5):
            player.rect.y -= STEP / 5
    if keys[pygame.K_s]:
        player.is_in_motion = True
        template_player_y += 5
        for i in range(5):
            player.rect.y += STEP / 5
    player.update()  # для переключения картинки

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    # рисуем все группы спрайтов
    tiles_group.draw(screen)
    resource_tiles_group.draw(screen)
    industry_tiles_group.update()
    industry_tiles_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.update()
    enemy_group.draw(screen)
    player_group.draw(screen)
    player.rotate_towards_mouse()

    # саундтрек
    tmp = random.randrange(0, 75000)
    if tmp == 1 and not soundtrack.get_busy():
        dj.index_of_sound = random.randint(0, len(dj.soundtracks) - 1)
    dj.update()

    cursor_frame.angle_of_rotating_frame += 1
    if mouse_x > 320 or mouse_y < HEIGHT - 260:
        cursor_frame.draw()

    # тут рисуем меню
    # ВНИМАНИЕ МИНИМАЛЬНЫЙ РАЗМЕР ЭКРАНА 260 пикселей
    screen.blit(menu, (0, HEIGHT - 254))
    if blocks_type == 'drills':
        screen.blit(drills_image, (4, HEIGHT - 250))
    elif blocks_type == 'logistics blocks':
        screen.blit(logistics_blocks_image, (4, HEIGHT - 250))
    elif blocks_type == 'turrets':
        screen.blit(turrets_image, (4, HEIGHT - 250))

    # меню ресурсов
    screen.blit(resources_menu, (313, HEIGHT - 125))
    for res in core.resources:
        font = pygame.font.Font(None, 32)
        text = font.render(f"{core.resources[res]}", True, pygame.Color('white'))
        text_rect = resources_coordinates[res][1]
        screen.blit(resources_coordinates[res][0], resources_coordinates[res][1])
        screen.blit(text, (text_rect[0] + 42, text_rect[1] + 11))

    # отрисовка frame
    if right_frame_pos is not None:
        screen.blit(frame, right_frame_pos)
    if top_left_frame_pos is not None:
        screen.blit(frame, top_left_frame_pos)
    if bottom_left_frame_pos is not None:
        screen.blit(frame, bottom_left_frame_pos)

    # рисуем стрелочку направления конвеера
    if type_of_current_block == 'conveyor' and blocks_type == 'logistics blocks':
        screen.blit(rotate_arrow, (114, HEIGHT - 45))

    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        screen.blit(cursor, (mouse_x, mouse_y))

    pygame.display.flip()
    clock.tick(FPS)

if flag_exit:
    end_screen()
