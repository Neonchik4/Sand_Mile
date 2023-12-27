import pygame
import os
import sys
import random


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


pygame.init()

size = WIDTH, HEIGHT = 960, 960
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sand Mile')

cursor = pygame.image.load('data/cursor.png')

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        screen.blit(cursor, (x, y))

    pygame.display.flip()

pygame.quit()
