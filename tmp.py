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

    def can_take_resource(self):
        return False

    def logic_update(self):
        self.resources[self.extraction_resource] += self.speed_of_mining
        if self.resources[self.extraction_resource] > 20:
            self.resources[self.extraction_resource] = 20

        if self.resources[self.extraction_resource] > 0:
            cur_blocks = []
            for x, y in self.lst_neighboring_cells:
                if board.industry_map[y][x] is not None and type(board.industry_map[y][x]) is not str:
                    if board.industry_map[y][x].can_take_resource():
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
                block.take_resource(self.extraction_resource)

    def update(self):
        self.update_draw()
