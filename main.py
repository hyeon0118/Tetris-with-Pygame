import pygame
import random
from itertools import cycle

pygame.init()


class Colors:
    colors = [(255, 0, 0), (255, 127, 0), (255, 247, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
    title_colors = [(255, 0, 0), (255, 127, 0), (255, 247, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (80, 80, 80)


class Blocks:
    blocks = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 2, 6, 7], [2, 5, 6, 9]],
        [[2, 3, 5, 6], [2, 6, 7, 11]],
        [[2, 6, 9, 10], [5, 6, 7, 11], [2, 3, 6, 10], [1, 5, 6, 7]],
        [[2, 6, 10, 11], [3, 5, 6, 7], [1, 2, 6, 10], [5, 6, 7, 9]],
        [[2, 5, 6, 7], [2, 5, 6, 10], [5, 6, 7, 10], [2, 6, 7, 10]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # type variables
        self.first_type = random.randint(0, len(self.blocks) - 1)
        self.next_type = random.randint(0, len(self.blocks) - 1)
        self.current_type = random.randint(0, len(self.blocks) - 1)
        self.held_type = None

        # color number variables
        self.next_color_number = random.randint(0, len(Colors.colors) - 1)
        self.current_color_number = random.randint(0, len(Colors.colors) - 1)
        self.fixed_color_number = None
        self.held_color_number = None

        # color variables
        self.next_color = Colors.colors[self.next_color_number]
        self.current_color = Colors.colors[self.current_color_number]
        self.fixed_color = None
        self.held_color = None

        self.rotation = 0

    def first_block_data(self):
        return self.blocks[self.first_type][self.rotation]

    def current_block_data(self):
        return self.blocks[self.current_type][self.rotation]

    def next_block_data(self):
        return self.blocks[self.next_type][0]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.blocks[self.current_type])


class Tetris:
    # screen
    width = 500
    height = 700

    # play field
    rows = 20
    columns = 10
    field = []

    # cell
    cell = 30
    mini_cell = 20
    mini_cell2 = 15
    fps = 60

    # play field margin (position play field in the center of the screen)
    board_x = (width / 2) - (cell * columns / 2)
    board_y = (height / 2) - (cell * rows / 2)

    # class setting
    block = Blocks(3, 0)
    next_block = Blocks(3, 0)

    # pos of score board and next block board
    score_board_x = (width - board_x - (cell * columns + mini_cell * 4)) / 2
    next_block_board_x = board_x + (cell * columns) + (width - (board_x + cell * columns + mini_cell * 4)) / 2

    intersection = False
    pixel_font = "VT323-Regular.ttf"
    font1 = pygame.font.Font(pixel_font, 25)
    font2 = pygame.font.Font(pixel_font, 40)

    def __init__(self):
        self.screen = None
        self.clock = None

        self.old_block_x = None
        self.old_block_y = None
        self.old_block_rotation = None

        self.limit = False

        self.level = 0

        self.line = 0
        self.total_removed_line = 0

        self.block.x = 3
        self.block.y = 0

        self.score = 0

        self.hold_counter = 0

        self.current_key = None
        self.held_block = None

        self.state = "start"

        self.field = []
        for i in range(self.rows):
            new_line = []
            for j in range(self.columns):
                new_line.append(-1)
            self.field.append(new_line)

    def init_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Tetris")

    def run_game(self):
        counter = 0
        counter_down = 0
        counter_side = 0
        running = True

        # blinking text
        BLINK_EVENT = pygame.USEREVENT + 0
        font = pygame.font.Font(self.pixel_font, 30)
        press_text = font.render("PRESS SPACE TO START", False, Colors.WHITE)
        press_text1 = font.render("PRESS SPACE TO START", False, Colors.GRAY)
        blink_texts = cycle([press_text, press_text1])
        blink_text = next(blink_texts)
        pygame.time.set_timer(BLINK_EVENT, 500)
        press_text_rect = press_text.get_rect(center=(self.width / 2, 400))

        while running:
            if self.state == "start":
                self.screen.fill(Colors.BLACK)
                self.title()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.state = "playing"
                    if event.type == BLINK_EVENT:
                        blink_text = next(blink_texts)
                self.screen.blit(blink_text, press_text_rect)

            elif self.state == "playing":
                self.screen.fill(Colors.BLACK)

                # draw the boards
                self.draw_score_board()
                self.draw_level_board()
                self.draw_board()
                self.draw_next_board()
                self.draw_hold_board()

                # draw blocks and update score
                self.draw_block()
                self.fix_block()
                self.remove_line()
                self.score_system()
                self.game_over()

                # movement
                counter += 1
                counter_side += 1

                if counter % (60 - self.level) == 0:
                    counter = 0
                    self.go_down(1)

                # interaction, event handler
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.rotate()
                        elif event.key == pygame.K_LEFT:
                            self.current_key = "LEFT"
                        elif event.key == pygame.K_RIGHT:
                            self.current_key = "RIGHT"
                        elif event.key == pygame.K_y:
                            self.hold_counter += 1
                            self.hold_block()
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.current_key = None

                if self.current_key == "LEFT":
                    self.go_side(-0.2)
                elif self.current_key == "RIGHT":
                    self.go_side(0.2)
                elif self.current_key is None:
                    self.go_side(0)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_DOWN]:
                    counter_down += 1
                    if counter_down % 3 == 0:
                        counter_down = 0
                        self.go_down(1)

            elif self.state == "gameover":
                self.block.y -= 1
                self.old_block_y = self.block.y
                self.game_over_text()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.__init__()
                            self.init_game()
                            self.state = "playing"
                        if event.key == pygame.K_ESCAPE:
                            self.__init__()
                            self.init_game()

            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()

    def title(self):
        title_blocks = [[0, 1, 2, 4, 7, 10, 13, 16, 19],
                        [0, 1, 2, 3, 6, 9, 10, 11, 12, 15, 18, 19, 20],
                        [0, 1, 2, 4, 7, 10, 13, 16, 19],
                        [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 14, 15, 17, 18, 20],
                        [0, 1, 2, 4, 7, 10, 13, 16, 18, 19, 20],
                        [0, 1, 2, 3, 5, 6, 9, 10, 11, 14, 15, 17, 18, 19, 20]]

        for title_index in range(len(title_blocks)):
            for i in range(7):
                for j in range(3):
                    if i * 3 + j in title_blocks[title_index]:
                        pygame.draw.rect(self.screen, Colors.title_colors[title_index],
                                         [90 + (55 * title_index) + 15 * j, 150 + 15 * i, 14, 14])

    def held_block_data(self):
        return self.block.blocks[self.block.held_type][0]

    def draw_level_board(self):
        score_text = self.font1.render("Lv.", True, Colors.GRAY)
        self.screen.blit(score_text, [self.score_board_x + 5, self.board_y])
        score_number = self.font2.render(f"{self.level}", True, Colors.WHITE)
        self.screen.blit(score_number, [self.score_board_x + 40, self.board_y - 10])

    def draw_score_board(self):
        score_text = self.font1.render("SCORE", True, Colors.GRAY)
        self.screen.blit(score_text, [self.score_board_x + 5, self.board_y + 50])
        score_number = self.font2.render(f"{self.score}", True, Colors.WHITE)
        self.screen.blit(score_number, [self.score_board_x + 5, self.board_y + 70])

    def draw_next_board(self):
        score_text = self.font1.render("NEXT", True, Colors.GRAY)
        self.screen.blit(score_text, [self.next_block_board_x + 10, self.board_y])
        pygame.draw.rect(self.screen, Colors.GRAY, (self.next_block_board_x, self.board_y + self.cell,
                                                    self.mini_cell * 4, self.mini_cell * 4), 1)
        self.draw_next_block()

    def draw_next_block(self):
        if self.next_block.next_block_data() == self.next_block.blocks[6][0]:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.next_block.next_block_data():
                        pygame.draw.rect(self.screen, self.next_block.next_color,
                                         [self.next_block_board_x + 10 + self.mini_cell2 * j,
                                          self.board_y + 55 + self.mini_cell2 * i,
                                          self.mini_cell2 - 1, self.mini_cell2 - 1])
        elif self.next_block.next_block_data() == self.next_block.blocks[0][0]:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.next_block.next_block_data():
                        pygame.draw.rect(self.screen, self.next_block.next_color,
                                         [self.next_block_board_x + 15 + self.mini_cell2 * j,
                                          self.board_y + 40 + self.mini_cell2 * i,
                                          self.mini_cell2 - 1, self.mini_cell2 - 1])
        else:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.next_block.next_block_data():
                        pygame.draw.rect(self.screen, self.next_block.next_color,
                                         [self.next_block_board_x + self.mini_cell2 * j, self.board_y + 50 + self.mini_cell2 * i,
                                          self.mini_cell2 - 1, self.mini_cell2 - 1])

    def draw_hold_board(self):
        score_text = self.font1.render("HOLD", True, Colors.GRAY)
        self.screen.blit(score_text, [self.next_block_board_x + 10, self.board_y + 150])
        pygame.draw.rect(self.screen, Colors.GRAY,
                         (self.next_block_board_x, self.board_y + self.cell + 150, self.mini_cell * 4, self.mini_cell * 4), 1)
        self.draw_held_block()

    def draw_held_block(self):
        if self.block.held_type is not None:
            if self.held_block_data() == self.block.blocks[6][0]:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.held_block_data():
                            pygame.draw.rect(self.screen, Colors.colors[self.block.held_color_number],
                                             [self.next_block_board_x + 10 + self.mini_cell2 * j,
                                              self.board_y + 55 + 150 + self.mini_cell2 * i,
                                              self.mini_cell2 - 1, self.mini_cell2 - 1])
            elif self.held_block_data() == self.block.blocks[0][0]:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.held_block_data():
                            pygame.draw.rect(self.screen, Colors.colors[self.block.held_color_number],
                                             [self.next_block_board_x + 15 + self.mini_cell2 * j,
                                              self.board_y + 40 + 150 + self.mini_cell2 * i,
                                              self.mini_cell2 - 1, self.mini_cell2 - 1])
            else:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.held_block_data():
                            pygame.draw.rect(self.screen, Colors.colors[self.block.held_color_number],
                                             [self.next_block_board_x + self.mini_cell2 * j,
                                              self.board_y + 50 + 150 + self.mini_cell2 * i,
                                              self.mini_cell2 - 1, self.mini_cell2 - 1])
        else:
            pass

    def hold_block(self):
        if self.hold_counter == 1:
            self.block.held_type = self.block.current_type
            self.block.held_color_number = self.block.current_color_number
            self.block.current_type = self.next_block.next_type
            self.block.current_color_number = self.next_block.next_color_number
            self.hold_counter = 4
            self.create_next_block(self.block.x, self.block.y, 0)
        elif self.hold_counter == 2:
            self.block.current_type, self.block.held_type = self.block.held_type, self.block.current_type
            self.block.current_color_number, self.block.held_color_number = self.block.held_color_number, self.block.current_color_number
            self.block.rotation = 0
        elif self.hold_counter == 3:
            self.block.held_type, self.block.current_type = self.block.current_type, self.block.held_type
            self.block.held_color_number, self.block.current_color_number = self.block.current_color_number, self.block.held_color_number
            self.block.rotation = 0
        else:
            pass
        self.frame_limit()
        if self.limit:
            self.block.x = self.old_block_x
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.block.current_block_data():
                        if j + round(self.block.x) > self.columns - 1:
                            self.block.x -= 1
                        elif j + round(self.block.x) < 0:
                            self.block.x = self.old_block_x

    def draw_board(self):
        for i in range(self.rows + 1):
            for j in range(self.columns + 1):
                pygame.draw.rect(self.screen, Colors.GRAY, (self.board_x, self.board_y, self.cell * j, self.cell * i), 1)

    def draw_block(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.current_block_data():
                    pygame.draw.rect(self.screen, Colors.colors[self.block.current_color_number],
                                     [self.board_x + self.cell * (j + round(self.block.x)),
                                      self.board_y + self.cell * (i + self.block.y), self.cell - 2,
                                      self.cell - 2])

    def create_next_block(self, x, y, n):
        self.block.x = x
        self.block.y = y
        self.block.current_type = self.next_block.next_type
        self.block.current_color = self.next_block.next_color
        self.block.current_color_number = self.next_block.next_color_number
        self.block.rotation = n
        self.next_block = Blocks(3, 0)

    def go_side(self, n):
        self.old_block_x = self.block.x
        self.block.x += n
        self.frame_limit()
        if self.limit:
            self.block.x = self.old_block_x

    def go_down(self, n):
        self.block.y += n
        self.frame_limit()
        if self.limit:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.block.current_block_data():
                        self.field[i + self.block.y - 1][j + round(self.block.x)] = self.block.current_color_number
            self.create_next_block(3, 0, 0)
            if self.hold_counter != 0:
                self.hold_counter = 2

    def rotate(self):
        self.old_block_rotation = self.block.rotation
        self.block.rotate()
        self.frame_limit()
        if self.limit:
            self.block.x = self.old_block_x
            self.block.y = self.block.y - 1
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.block.current_block_data():
                        if j + round(self.block.x) > self.columns - 1:
                            self.block.x -= 2
                        elif j + round(self.block.x) < 0:
                            self.block.x += 1

    def frame_limit(self):
        self.limit = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.current_block_data():
                    if i + self.block.y > self.rows - 1 or \
                            j + round(self.block.x) > self.columns - 1 or \
                            j + round(self.block.x) < 0 or \
                            self.field[i + self.block.y][j + round(self.block.x)] > -1:
                        self.limit = True

    def fix_block(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.field[i][j] > -1:
                    pygame.draw.rect(self.screen, Colors.colors[self.field[i][j]],
                                     [self.board_x + self.cell * j, self.board_y + self.cell * i,
                                      self.cell - 2, self.cell - 2])

    def remove_line(self):
        for i in range(self.rows):
            if -1 not in self.field[i]:
                self.field.remove(self.field[i])
                self.line += 1
                self.field.insert(0, [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
        return self.line

    def score_system(self):
        removed_line = self.remove_line()
        self.total_removed_line += removed_line
        if removed_line == 1:
            self.score += 40 * (self.level + 1)
        elif removed_line == 2:
            self.score += 100 * (self.level + 1)
        elif removed_line == 3:
            self.score += 300 * (self.level + 1)
        elif removed_line >= 4:
            self.score += removed_line * 300 * (self.level + 1)
        self.level_system()
        self.line = 0

    def level_system(self):
        if self.level < 5:
            while self.total_removed_line > 2:
                self.level_up()
        elif self.level < 10:
            while self.total_removed_line > 5:
                self.level_up()
        elif self.level >= 10:
            while self.total_removed_line > 9:
                self.level_up()

    def level_up(self):
        self.level += 1
        self.total_removed_line = 0

    def game_over(self):
        if self.field[0].count(-1) != 10:
            self.state = "gameover"

    def game_over_text(self):
        game_over_font = pygame.font.Font(self.pixel_font, 65)
        game_over_text = game_over_font.render("G A M E  O V E R", True, Colors.GRAY)
        self.screen.blit(game_over_text, [40, self.height / 2 - 100])
        start_again_font = pygame.font.Font(self.pixel_font, 35)
        start_again_text = start_again_font.render("PRESS SPACE TO START AGAIN", False, Colors.WHITE)
        self.screen.blit(start_again_text, [70, 360])


if __name__ == '__main__':
    tetris = Tetris()
    tetris.init_game()
    tetris.run_game()
