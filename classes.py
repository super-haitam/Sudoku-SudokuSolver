import pygame

WIDTH, HEIGHT = 620, 620
w, h = WIDTH * (3 / 4), HEIGHT * (3 / 4)
x_margin, y_margin = WIDTH/8, HEIGHT / 8 + 20

# Colors
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
BLUE = (0, 114, 227)
GREY = (195, 215, 234)
RED = (229, 92, 108)
YELLOW = (200, 200, 0)


class Cell:
    def __init__(self, value):
        self.size = WIDTH/12
        self.surface = pygame.Surface((self.size, self.size))

        self.bg_color = WHITE
        self.value = value

        self.readonly = True
        self.font_color = BLACK
        if self.value == 0:
            self.readonly = False
            self.font_color = BLUE

        self.x: int
        self.y: int

    def get_pos_in_board(self, board):
        for num, block in enumerate(board):
            if self in block:
                return num, block.index(self)

    def get_x_y(self, board):
        block_pos, cell_pos = self.get_pos_in_board(board)

        if 0 <= block_pos <= 2:
            y = y_margin
        elif 3 <= block_pos <= 5:
            y = y_margin + h/3
        else:
            y = y_margin + h*(2/3)
        if block_pos in [0, 3, 6]:
            x = x_margin
        elif block_pos in [1, 4, 7]:
            x = x_margin + w/3
        else:
            x = x_margin + w*(2/3)

        if 3 <= cell_pos <= 5:
            y += self.size
        elif not 0 <= cell_pos <= 2:
            y += 2 * self.size
        if cell_pos in [1, 4, 7]:
            x += self.size
        elif cell_pos not in [0, 3, 6]:
            x += 2 * self.size

        return x, y

    def draw(self, screen):
        self.surface.fill(self.bg_color)
        screen.blit(self.surface, (self.x, self.y))

        font = pygame.font.SysFont("comicsans", 30)
        txt = font.render(str(self.value), True, self.font_color) if self.value != 0 \
            else font.render(' ', True, self.font_color)
        screen.blit(txt, (self.x + txt.get_width(), self.y + (txt.get_height())/5))


class Button:
    def __init__(self, x, y, width, height, text, txt_color, bg_color, font_size, bold=False):
        font = pygame.font.SysFont("comicsans", font_size, bold=bold)
        self.txt = font.render(text, True, txt_color)

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.bg = pygame.Surface((width, height))
        self.bg.fill(bg_color)

    def is_collision(self, ms_x, ms_y):
        if self.x < ms_x < self.x + self.width and self.y < ms_y < self.y + self.height:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.bg, (self.x, self.y))
        screen.blit(self.txt, ((self.x+self.width/2) - self.txt.get_width()/2,
                               (self.y+self.height/2) - self.txt.get_height()/2))


class NewGameButton(Button):
    def __init__(self):
        width, height = WIDTH * (2 / 3), HEIGHT / 10
        x, y = (WIDTH-width)/2, 0

        super().__init__(x, y, width, height, "New Game", WHITE, BLUE, 30)

        self.wait = True

    def is_collision(self, ms_x, ms_y):
        if super().is_collision(ms_x, ms_y):
            self.wait = True
            return True
        return False

    def draw_wait(self, screen):
        font = pygame.font.SysFont("comicsans", 30)
        txt = font.render("wait...", True, BLACK)

        screen.blit(txt, ((self.x + self.width/2) - txt.get_width()/2, self.y + self.height))

    def draw(self, screen):
        super().draw(screen)

        if self.wait:
            self.draw_wait(screen)
            self.wait = False


class HelpButton(Button):
    def __init__(self):
        x, y = 10, 20
        width, height = WIDTH / 12, HEIGHT / 12

        super().__init__(x, y, width, height, "Help ?", BLACK, GREY, 15, bold=True)


class NumberButton(Button):
    def __init__(self, x, y, num: int):
        width, height = WIDTH/13, HEIGHT/13

        self.color = RED
        self.number = num

        super().__init__(x, y, width, height, str(self.number), WHITE, self.color, 15)

    def draw(self, screen):
        self.bg.fill(self.color)

        super().draw(screen)


class SolveButton(Button):
    def __init__(self):
        x, y = WIDTH - x_margin*(7/8), y_margin + h/9
        width, height = x_margin*(3/4), h*(7/9)

        super().__init__(x, y, width, height, "Solve", WHITE, YELLOW, 20)
