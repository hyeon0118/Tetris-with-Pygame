import pygame
import random
import time
from itertools import cycle

pygame.init()


class Colors:
    colors = [(255, 255, 255), (100, 100, 100), (255, 0, 0), (255, 127, 0), (255, 247, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
    title_colors = [(255, 0, 0), (255, 127, 0), (255, 247, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (80, 80, 80)


class Fonts:
    default_font = "VT323-Regular.ttf"

    font25 = pygame.font.Font(default_font, 25)
    font30 = pygame.font.Font(default_font, 30)
    font40 = pygame.font.Font(default_font, 40)
    font65 = pygame.font.Font(default_font, 65)
    font100 = pygame.font.Font(default_font, 100)

    def render_text(self, txt, size, boolX, color):
        match size:
            case 'XS':
                self.font25.render(txt, boolX, color)
            case 'S':
                self.font30.render(txt, boolX, color)
            case 'M':
                self.font40.render(txt, boolX, color)
            case 'L':
                self.font65.render(txt, boolX, color)
            case 'XL':
                self.font100.render(txt, boolX, color)


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

    title_blocks = [[0, 1, 2, 4, 7, 10, 13, 16, 19],
                    [0, 1, 2, 3, 6, 9, 10, 11, 12, 15, 18, 19, 20],
                    [0, 1, 2, 4, 7, 10, 13, 16, 19],
                    [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 14, 15, 17, 18, 20],
                    [0, 1, 2, 4, 7, 10, 13, 16, 18, 19, 20],
                    [0, 1, 2, 3, 5, 6, 9, 10, 11, 14, 15, 17, 18, 19, 20]]

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # type variables
        self.next_type = random.randint(0, len(self.blocks) - 1)
        self.current_type = random.randint(0, len(self.blocks) - 1)
        self.held_type = None

        # color number variables
        self.next_color_number = random.randint(2, len(Colors.colors) - 1)
        self.current_color_number = random.randint(2, len(Colors.colors) - 1)
        self.held_color_number = None

        # color variables
        self.next_color = Colors.colors[self.next_color_number]
        self.current_color = Colors.colors[self.current_color_number]

        self.rotation = 0

    def current_block_data(self):
        """
        get numbers of the current block as a list (ex. [1, 5, 9, 13])
        :return: self.blocks[self.current_type][self.rotation]
        """
        return self.blocks[self.current_type][self.rotation]

    def next_block_data(self):
        """
        get numbers of the next block's first position as a list (ex. [2, 3, 5, 6])
        :return: self.blocks[self.next_type][0]
        """
        return self.blocks[self.next_type][0]

    def rotate(self):
        """
        it repeats the length of the current block's list, so that we can get correct index for rotation
        :return:
        """
        self.rotation = (self.rotation + 1) % len(self.blocks[self.current_type])


class Tetris:
    # screen size
    width = 500
    height = 700

    screen = pygame.display.set_mode((width, height))
    #main_screen = MainScreen(pygame.display.set_mode((width, height)))

    # number of rows and columns of the play field
    rows = 20
    columns = 10
    field = []

    # cell (size for one cell in play field, side board and side board blocks)
    field_cell = 30
    small_field_cell = 20
    small_block_cell = 15

    # set clock and frame for seconds
    clock = pygame.time.Clock()
    fps = 60

    # play field margin (position play field in the center of the screen)
    board_x = (width / 2) - (field_cell * columns / 2)
    board_y = (height / 2) - (field_cell * rows / 2)

    # class setting
    block = Blocks(3, 0)
    next_block = Blocks(3, 0)

    # x position (left margin) of each side board
    left_side_board_margin = (width - board_x - (field_cell * columns + small_field_cell * 4)) / 2
    right_side_board_margin = board_x + (field_cell * columns) + (width - (board_x + field_cell * columns + small_field_cell * 4)) / 2

    # go_side tempo and input backspace tempo set (get_pressed())
    last_time = 0
    interval = 100

    # count down variables
    count_down_text = "3"

    # input variables (text)
    login_input_text = ""
    login_name = ""

    # basic font
    default_font = "VT323-Regular.ttf"

    # font
    font25 = pygame.font.Font(default_font, 25)
    font30 = pygame.font.Font(default_font, 30)
    font40 = pygame.font.Font(default_font, 40)
    font65 = pygame.font.Font(default_font, 65)
    font100 = pygame.font.Font(default_font, 100)

    # input variables (color-rect)
    input_rect = pygame.Rect(200, 200, 140, 32)
    input_rect_color_active = pygame.Color("lightskyblue3")
    input_rect_color_passive = pygame.Color("gray15")
    input_rect_color = input_rect_color_passive
    input_active = False

    # music variables
    game_over_sound = pygame.mixer.Sound("game_over.mp3")
    menu_effect_sound = pygame.mixer.Sound("menu_sound.mp3")
    tetris_music_sound = pygame.mixer.Sound("Tetris.mp3")
    game_over_channel = pygame.mixer.Channel(1)
    tetris_music_channel = pygame.mixer.Channel(2)

    # user event
    TITLE_EVENT = pygame.USEREVENT + 0
    BLINK_EVENT = pygame.USEREVENT + 1
    COUNT_DOWN = pygame.USEREVENT + 2
    GAME_OVER = pygame.USEREVENT + 3
    pygame.time.set_timer(TITLE_EVENT, 5)
    pygame.time.set_timer(BLINK_EVENT, 500)
    pygame.time.set_timer(COUNT_DOWN, 1000)
    pygame.time.set_timer(GAME_OVER, 50)

    # render
    press_text = font30.render("PRESS SPACE TO START", False, Colors.WHITE)
    press_text1 = font30.render("PRESS SPACE TO START", False, Colors.GRAY)
    login_text1 = font40.render("ENTER YOUR NAME", True, Colors.colors[0])
    login_text2 = font40.render("AND PRESS ENTER", True, Colors.colors[0])
    game_over_text = font65.render("G A M E  O V E R", True, pygame.color.Color("brown3"))
    start_again_text = font30.render("PRESS ENTER TO START AGAIN", False, Colors.WHITE)

    # BLINK_EVENT
    blink_texts = cycle([press_text, press_text1])
    blink_text = next(blink_texts)
    press_text_rect = press_text.get_rect(center=(width / 2, 310))

    def __init__(self):
        # block's previous position and rotation to fix the block at the end of the falling
        self.old_block_x = None
        self.old_block_y = None
        self.old_block_rotation = None
        self.preview_y = 0

        # returns True if the block touch the end of frame or another block)
        self.limit = False

        # variables for level and score
        self.level = 0
        self.line = 0
        self.total_removed_line = 0
        self.score = 0

        # Initialized position of the block
        self.block.x = 3
        self.block.y = 0

        # counter
        self.title_y = 0
        self.game_over_counter = 20
        self.count_down_counter = 3
        self.counter_go_down = 0
        self.counter_go_down_accel = 0
        self.hold_counter = "empty"  # check, whether a block is held for the first time or for the next time or not

        # game state
        self.state = "start"
        self.block_statu = "going"
        self.paused_statu = 0
        self.running = True

        # data for the field as a list (to get rows and columns)
        self.field = []
        for i in range(self.rows):
            new_line = []
            for j in range(self.columns):
                new_line.append(-1)
            self.field.append(new_line)

    def init_game(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.block.held_type = None
        self.game_over_channel.stop()
        self.tetris_music()

    def run_game(self):
        while self.running:
            if self.state == "start":
                self.start()

            elif self.state == "login":
                self.login()

            elif self.state == "countdown":
                self.countdown()

            elif self.state == "playing":
                self.playing()

            elif self.state == "gameover":
                self.tetris_music_channel.stop()
                self.game_over_music()
                self.draw_fixed_block()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.__init__()
                            self.init_game()
                            self.state = "playing"
                        if event.key == pygame.K_ESCAPE:
                            self.__init__()
                            self.init_game()
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == self.GAME_OVER:
                        self.game_over_counter -= 1
                        if self.game_over_counter > -1:
                            self.field[self.game_over_counter] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

                self.screen.blit(self.game_over_text, [40, self.height / 2 - 100])
                self.screen.blit(self.start_again_text, [70, 360])

            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()

    def playing(self):
        self.screen.fill(Colors.BLACK)
        # draw all the boards
        self.draw_score()
        self.draw_level()
        self.draw_board()
        self.draw_next_block_board()
        self.draw_next_block()
        self.draw_hold_block_board()
        # draw blocks
        self.draw_block(self.block.x, self.block.y, self.block.current_color_number, 0)
        self.preview()
        self.draw_fixed_block()
        self.remove_line()
        self.score_system()
        self.level_system()
        self.draw_paused()
        self.game_over()
        # movement
        self.counter_go_down += 1
        if self.block_statu == "going":
            if self.counter_go_down % (60 - self.level) == 0:
                self.counter_go_down = 0
                self.go_down(1)
        elif self.block_statu == "stop":
            self.go_down(0)
        # interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.paused_statu == 0:
                        self.block_statu = "stop"
                        self.paused_statu = 1
                    elif self.paused_statu == 1:
                        self.block_statu = "going"
                        self.paused_statu = 0
                elif event.key == pygame.K_UP:
                    self.rotate()
                elif event.key == pygame.K_y:
                    self.hold_block()
                    self.hold_counter = "occupied"
                elif event.key == pygame.K_SPACE:
                    self.drop()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.go_side(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.counter_go_down_accel += 1
            if self.counter_go_down_accel % 3 == 0:
                self.counter_go_down_accel = 0
                self.go_down(1)
        elif keys[pygame.K_LEFT] and (pygame.time.get_ticks() > self.last_time + self.interval):
            self.go_side(-1)
            self.last_time = pygame.time.get_ticks()
        elif keys[pygame.K_RIGHT] and (pygame.time.get_ticks() > self.last_time + self.interval):
            self.go_side(1)
            self.last_time = pygame.time.get_ticks()

    def countdown(self):
        self.screen.fill(Colors.BLACK)
        self.draw_score()
        self.draw_level()
        self.draw_board()
        self.draw_next_block_board()
        self.draw_hold_block_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.COUNT_DOWN:
                self.count_down_counter -= 1
                if self.count_down_counter > 0:
                    self.count_down_text = str(self.count_down_counter)
                elif self.count_down_counter == 0:
                    self.count_down_text = "GO!"
                else:
                    self.state = "playing"
        count_down = self.font100.render(self.count_down_text, True, (255, 255, 255))
        count_down_rect = count_down.get_rect(center=(self.width / 2, self.height / 2))
        self.screen.blit(count_down, count_down_rect)

    def login(self):
        self.screen.fill(Colors.BLACK)
        self.screen.blit(self.login_text1, [130, 110])
        self.screen.blit(self.login_text2, [130, 140])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False
            if event.type == pygame.KEYDOWN:
                if self.input_active:
                    self.login_input_text += event.unicode
                if event.key == pygame.K_RETURN:
                    self.login_name = self.login_input_text
                    self.state = "countdown"
                if event.key == pygame.K_BACKSPACE:
                    self.login_input_text = self.login_input_text[:-1]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE] and (pygame.time.get_ticks() > self.last_time + self.interval):
            self.last_time = pygame.time.get_ticks()
            self.login_input_text = self.login_input_text[:-1]
        self.draw_login_input()

    def start(self):
        background = pygame.image.load("background.jpg")
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.blink_text, self.press_text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.menu_effect_sound.set_volume(0.1)
                    self.menu_effect_sound.play(0)
                    self.state = "login"
                    time.sleep(0.3)
            if event.type == self.BLINK_EVENT:
                self.blink_text = next(self.blink_texts)
            if event.type == self.TITLE_EVENT:
                self.title_y += 1
                if self.title_y < 151:
                    self.draw_title(self.title_y)
                elif self.title_y >= 150:
                    self.title_y = 150
                    self.draw_title(self.title_y)

    def tetris_music(self):
        if not self.tetris_music_channel.get_busy():
            self.tetris_music_channel.set_volume(0.1)
            self.tetris_music_channel.play(self.tetris_music_sound, loops=-1)

    def game_over_music(self):
        if not self.game_over_channel.get_busy():
            self.game_over_channel.set_volume(0.1)
            self.game_over_channel.play(self.game_over_sound, loops=-1)

    def draw_title(self, y):
        """
        draw title "TETRIS"
        :param y: y position of each alphabet
        :return:
        """
        for alphabet in range(len(self.block.title_blocks)):
            for i in range(7):
                for j in range(3):
                    if i * 3 + j in self.block.title_blocks[alphabet]:
                        pygame.draw.rect(self.screen, Colors.title_colors[alphabet],
                                         [90 + (55 * alphabet) + 15 * j, y + 15 * i, 14, 14])

    def draw_login_input(self):
        """
        draw input box, if it's clicked, the frame turns into blue, if it's not, it's remained gray
        :return:
        """
        if self.input_active:
            self.input_rect_color = self.input_rect_color_active
        else:
            self.input_rect_color = self.input_rect_color_passive

        pygame.draw.rect(self.screen, self.input_rect_color, self.input_rect, 2)

        text_surface = self.font30.render(self.login_input_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def draw_board(self):
        for i in range(1, self.rows + 1):
            for j in range(1, self.columns + 1):
                pygame.draw.rect(self.screen, Colors.GRAY, (self.board_x, self.board_y,
                                                            self.field_cell * j, self.field_cell * i), 1)

    def draw_level(self):
        score_text = self.font25.render("Lv.", True, Colors.GRAY)
        self.screen.blit(score_text, [self.left_side_board_margin + 5, self.board_y])
        score_number = self.font40.render(f"{self.level}", True, Colors.WHITE)
        self.screen.blit(score_number, [self.left_side_board_margin + 40, self.board_y - 10])

    def draw_score(self):
        score_text = self.font25.render("SCORE", True, Colors.GRAY)
        self.screen.blit(score_text, [self.left_side_board_margin + 5, self.board_y + 50])
        score_number = self.font40.render(f"{self.score}", True, Colors.WHITE)
        self.screen.blit(score_number, [self.left_side_board_margin + 5, self.board_y + 70])
        player_name = self.font40.render(f"{self.login_name}", True, Colors.WHITE)
        self.screen.blit(player_name, [10, 5])

    def draw_next_block_board(self):
        score_text = self.font25.render("NEXT", True, Colors.GRAY)
        self.screen.blit(score_text, [self.right_side_board_margin + 10, self.board_y])
        pygame.draw.rect(self.screen, Colors.GRAY, (self.right_side_board_margin, self.board_y + self.field_cell, self.small_field_cell * 4, self.small_field_cell * 4), 1)

    def draw_next_block(self):
        if self.next_block.next_block_data() == self.next_block.blocks[6][0]:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.next_block.next_block_data():
                        pygame.draw.rect(self.screen, self.next_block.next_color,
                                         [self.right_side_board_margin + 10 + self.small_block_cell * j,
                                          self.board_y + 55 + self.small_block_cell * i,
                                          self.small_block_cell - 1, self.small_block_cell - 1])
        elif self.next_block.next_block_data() == self.next_block.blocks[0][0]:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.next_block.next_block_data():
                        pygame.draw.rect(self.screen, self.next_block.next_color,
                                         [self.right_side_board_margin + 15 + self.small_block_cell * j,
                                          self.board_y + 40 + self.small_block_cell * i,
                                          self.small_block_cell - 1, self.small_block_cell - 1])
        else:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.next_block.next_block_data():
                        pygame.draw.rect(self.screen, self.next_block.next_color,
                                         [self.right_side_board_margin + self.small_block_cell * j, self.board_y + 50 + self.small_block_cell * i,
                                          self.small_block_cell - 1, self.small_block_cell - 1])

    def draw_hold_block_board(self):
        font3 = pygame.font.Font(self.default_font, 25)
        score_text = font3.render("HOLD", True, Colors.GRAY)
        self.screen.blit(score_text, [self.right_side_board_margin + 10, self.board_y + 150])
        pygame.draw.rect(self.screen, Colors.GRAY,
                         (self.right_side_board_margin, self.board_y + self.field_cell + 150, self.small_field_cell * 4, self.small_field_cell * 4), 1)
        self.draw_held_block()

    def draw_held_block(self):
        if self.block.held_type is None:
            pass
        else:
            if self.held_block_data() == self.block.blocks[6][0]:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.held_block_data():
                            pygame.draw.rect(self.screen, Colors.colors[self.block.held_color_number],
                                             [self.right_side_board_margin + 10 + self.small_block_cell * j,
                                              self.board_y + 55 + 150 + self.small_block_cell * i,
                                              self.small_block_cell - 1, self.small_block_cell - 1])
            elif self.held_block_data() == self.block.blocks[0][0]:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.held_block_data():
                            pygame.draw.rect(self.screen, Colors.colors[self.block.held_color_number],
                                             [self.right_side_board_margin + 15 + self.small_block_cell * j,
                                              self.board_y + 40 + 150 + self.small_block_cell * i,
                                              self.small_block_cell - 1, self.small_block_cell - 1])
            else:
                for i in range(4):
                    for j in range(4):
                        if i * 4 + j in self.held_block_data():
                            pygame.draw.rect(self.screen, Colors.colors[self.block.held_color_number],
                                             [self.right_side_board_margin + self.small_block_cell * j,
                                              self.board_y + 50 + 150 + self.small_block_cell * i,
                                              self.small_block_cell - 1, self.small_block_cell -   1])

    def draw_block(self, x, y, color_number, n):
        """
        this function is for drawing current falling block and preview block
        :param x: x position
        :param y: y position
        :param color_number: index number for colors list
        :param n: full square(0) or just frame(1)
        :return:
        """
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.current_block_data():
                    pygame.draw.rect(self.screen, Colors.colors[color_number],
                                     [self.board_x + self.field_cell * (j + round(x)),
                                      self.board_y + self.field_cell * (i + y), self.field_cell - 2,
                                      self.field_cell - 2], n)

    def draw_fixed_block(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.field[i][j] > -1:
                    pygame.draw.rect(self.screen, Colors.colors[self.field[i][j]],
                                     [self.board_x + self.field_cell * j, self.board_y + self.field_cell * i,
                                      self.field_cell - 2, self.field_cell - 2])

    def preview(self):
        """
        (check if other block or bottom exist under the block)
        see the lines under the falling block  (from the top to the bottom) until limit == True (touch the ground or already existing block)
        and then on the line over the y position, where preview_y stops gaining, draw preview square
        :return:
        """
        self.preview_y = self.block.y + 1
        while self.preview_y < self.rows:
            if self.frame_limit(self.block.x, self.preview_y):
                break
            self.preview_y += 1
        self.draw_block(self.block.x, self.preview_y - 1, 0, 1)

    def drop(self):
        """
        if the space is pressed, draw block immediately on the position of the preview
        :return:
        """
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.current_block_data():
                    self.field[i + self.preview_y - 1][j + round(self.block.x)] = self.block.current_color_number
        effect = pygame.mixer.Sound("block.wav")
        effect.play(0)
        # because it touches the bottom set the hold_counter to 2
        self.create_next_block(3, 0)
        if self.hold_counter != "empty":
            self.hold_counter = "change"

    def go_side(self, n):
        self.old_block_x = self.block.x
        self.block.x += n
        self.frame_limit(self.block.x, self.block.y)
        if self.limit:
            self.block.x = self.old_block_x  # if it touches the side of the field, set x position to previous position

    def go_down(self, n):
        self.block.y += n
        self.frame_limit(round(self.block.x), self.block.y)
        # if it touches the ground (bottom) of the field or any other blocks, fix it
        # (fill the corresponding list with the current color's number, so that it can be drawn on the field)
        if self.limit:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.block.current_block_data():
                        self.field[i + self.block.y - 1][j + round(self.block.x)] = self.block.current_color_number

            effect = pygame.mixer.Sound("block.wav")
            effect.play(0)
            self.create_next_block(3, 0)
            if self.hold_counter != "empty":
                self.hold_counter = "change"

    def rotate(self):
        self.block.rotate()
        self.frame_limit(self.block.x, self.block.y)
        if self.limit:
            self.block.x = self.old_block_x
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.block.current_block_data():
                        if j + round(self.block.x) > self.columns - 1:
                            self.block.x -= 1
                        elif j + round(self.block.x) < 0:
                            self.block.x += 1

    def frame_limit(self, x, y):
        """
        :param x: block's x position
        :param y: block's y position / preview's y position
        :return: self.limit, whether the block touches the field's frame(side, bottom) or any other blocks
        """
        self.limit = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.current_block_data():
                    if i + y > self.rows - 1 or \
                            j + round(x) > self.columns - 1 or \
                            j + round(x) < 0 or \
                            self.field[i + y][j + round(x)] > -1:
                        self.limit = True
        return self.limit

    def held_block_data(self):
        return self.block.blocks[self.block.held_type][0]

    def hold_block(self):
        """
        holding block should be:
        1. at the first holding, the held block should be replaced with the next block.
        2. from the second holding, the held block should be replaced with the current block.
        3. just once executed during one flow(a block falls from the top to the bottom of the field)

        * hold_counter == 1 means any block has been not held yet, so if users press y button, to keep the button,
        all the held block's info will contain current block's info and next block will come after on the field.
        * hold_counter == 2 or 3 executes exchange between current and held block's data (type and color, and set rotation to 0)
        * every time the block stops moving (touch the ground or another block), hold_counter set to 2 if the block has been already once held

        :return:
        """
        if self.hold_counter == "empty":
            self.block.held_type = self.block.current_type
            self.block.held_color_number = self.block.current_color_number
            self.block.current_type = self.next_block.next_type
            self.block.current_color_number = self.next_block.next_color_number
            self.create_next_block(self.block.x, self.block.y)
        elif self.hold_counter == "change":
            self.block.held_type, self.block.current_type = self.block.current_type, self.block.held_type
            self.block.held_color_number, self.block.current_color_number = self.block.current_color_number, self.block.held_color_number
            self.block.rotation = 0
        elif self.hold_counter == "occupied":
            pass
        self.frame_limit(self.block.x, self.block.y)
        if self.limit:
            self.block.x = self.old_block_x
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.block.current_block_data():
                        if j + round(self.block.x) > self.columns - 1:
                            self.block.x -= 1
                        elif j + round(self.block.x) < 0:
                            self.block.x = self.old_block_x

    def create_next_block(self, x, y):
        """
        not the next block on the next block
        but the next falling block
        :param x: x position
        :param y: y position
        :return:
        """
        self.block.x = x
        self.block.y = y
        self.block.current_type = self.next_block.next_type
        self.block.current_color = self.next_block.next_color
        self.block.current_color_number = self.next_block.next_color_number
        self.block.rotation = 0
        self.next_block = Blocks(3, 0)

    def remove_line(self):
        """
        -1 not in self.field[i] means it's blanked, the line is full of blocks == it should be removed.
        remove that line, and then insert new line on the top (at the first of the field list)
        """
        for i in range(self.rows):
            if -1 not in self.field[i]:
                self.field.remove(self.field[i])
                self.line += 1
                self.field.insert(0, [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

    def score_system(self):
        """
        score is calculated according to the number of removed lines at once
        the more lines are removed at once, the more score the user gets
        :return:
        """
        self.remove_line()
        self.total_removed_line += self.line
        if self.line == 1:
            self.score += 40 * (self.level + 1)
        elif self.line == 2:
            self.score += 100 * (self.level + 1)
        elif self.line == 3:
            self.score += 300 * (self.level + 1)
        elif self.line >= 4:
            self.score += self.line * 300 * (self.level + 1)

        self.line = 0

    def level_system(self):
        """
        level is calculated according to the total number of removed lines
        the higher the level becomes, the more lines need for level up
        :return:
        """
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
        """
        level + 1
        after level up, total removed line should be newly calculated
        :return:
        """
        self.level += 1
        effect = pygame.mixer.Sound("level.wav")
        effect.play(0)
        self.total_removed_line = 0

    def draw_paused(self):
        """
        inform the user that the game is paused (text render)
        :return:
        """
        if self.block_statu == "stop":
            font = pygame.font.Font(self.default_font, 65)
            paused_text = font.render("P A U S E D", True, Colors.GRAY)
            self.screen.blit(paused_text, [110, self.height / 2 - 100])
            font1 = pygame.font.Font(self.default_font, 35)
            start_again_text = font1.render("PRESS ENTER TO START AGAIN", False, Colors.WHITE)
            self.screen.blit(start_again_text, [70, 360])

    def game_over(self):
        """
        if there is any fixed block on the top of the field, game is over
        :return:
        """
        if self.field[0].count(-1) != 10:
            self.store_name_and_score()
            self.state = "gameover"

    def store_name_and_score(self):
        """
        store user's name and score in the txt file
        :return:
        """
        with open("name_and_score.txt", "a") as file:
            file.write(self.login_name.rstrip() + ", " + str(self.score) + "\n")


if __name__ == '__main__':
    tetris = Tetris()
    tetris.init_game()
    tetris.run_game()
