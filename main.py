# Sudoku Game
import time
from get_nums_board import get_nums_board
from classes import Cell, NewGameButton, HelpButton, NumberButton, SolveButton
import random
import pygame

pygame.init()
pygame.font.init()


# Screen
WIDTH, HEIGHT = 620, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Colors
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
LIGHT_RED, LIGHT_BLUE = (247, 207, 214), (187, 222, 251)
LIGHT_GREY = (226, 235, 243)
GREY = (195, 215, 234)
RED, GREEN, BLUE = (229, 92, 108), (0, 255, 0), (0, 114, 227)
PSEUDO_WHITE = tuple(random.randint(200, 255) for _ in range(3))

# Vars
w, h = WIDTH * (3 / 4), HEIGHT * (3 / 4)
x_margin, y_margin = WIDTH / 8, HEIGHT / 8 + 20

# Functions
random_color = lambda a, b: tuple(random.randint(a, b) for _ in range(3))


def draw_lines():
    def draw_line(start: tuple, end: tuple, color, width):
        pygame.draw.line(screen, color, start, end, width=width)

    # Draw horizontal and vertical external lines
    for hor_line in range(4):
        draw_line((x_margin, y_margin + (HEIGHT / 4) * hor_line),
                  (x_margin + w, y_margin + (HEIGHT / 4) * hor_line), BLACK, 2)
    for ver_line in range(4):
        draw_line((x_margin + (WIDTH / 4) * ver_line, y_margin),
                  (x_margin + (WIDTH / 4) * ver_line, y_margin + h), BLACK, 2)

    # Draw horizontal and vertical internal lines
    for hor in range(3):
        for hor_line in range(2):
            draw_line((x_margin, y_margin + (HEIGHT / 4) * hor + (HEIGHT / 12) * (hor_line + 1)),
                      (x_margin + w, y_margin + (HEIGHT / 4) * hor + (HEIGHT / 12) * (hor_line + 1)), BLACK, 1)
    for ver in range(3):
        for ver_line in range(2):
            draw_line((x_margin + (WIDTH / 4) * ver + (WIDTH / 12) * (ver_line + 1), y_margin),
                      (x_margin + (WIDTH / 4) * ver + (WIDTH / 12) * (ver_line + 1), y_margin + h), BLACK, 1)


def get_selected_cell():
    def get_block_pos(nb):
        block_x = x_margin
        if nb in [0, 3, 6]:
            block_x += 0
        elif nb in [1, 4, 7]:
            block_x += w / 3
        else:
            block_x += w * (2 / 3)

        block_y = y_margin
        if nb in [0, 1, 2]:
            block_y += 0
        elif nb in [3, 4, 5]:
            block_y += h / 3
        else:
            block_y += h * (2 / 3)

        return block_x, block_y

    # In which block and which cell
    for block_num, block in enumerate(board):
        block_x, block_y = get_block_pos(block_num)

        # Which block
        if block_x <= mouse_x < block_x + w / 3 and block_y <= mouse_y < block_y + h / 3:
            for cell_num, cell in enumerate(block):
                if cell.x <= mouse_x < cell.x + cell.size and cell.y <= mouse_y < cell.y + cell.size:
                    return cell


def draw_choice():
    screen.fill(PSEUDO_WHITE)

    font = pygame.font.SysFont("comicsans", 70)
    wlcm_txt = font.render("WELCOME TO", True, BLACK)
    game_name_txt = font.render(pygame.display.get_caption()[0], True, random_color(0, 255))
    game_txt = font.render("GAME", True, BLACK)

    screen.blit(wlcm_txt, ((WIDTH - wlcm_txt.get_width()) / 2, HEIGHT / 8))
    screen.blit(game_name_txt, ((WIDTH - game_name_txt.get_width()) / 2, HEIGHT * (1 / 2 - 1 / 9)))
    screen.blit(game_txt, ((WIDTH - game_txt.get_width()) / 2, HEIGHT * (2 / 3)))

    pygame.display.flip()


def draw_help():
    screen.fill(PSEUDO_WHITE)

    instructions = ["Use 'New Game' to display a brand new sudoku board.",
                    "To write a number on an empty cell, click on it, then press the number.",
                    "To erase a number you wrote, press Delete or Backspace.",
                    "This game is basic and is not a fast one so wait a second if it seems not to respond.",
                    "You might need to press the number more than once.",
                    "This program uses Backtracking to solve the sudoku grid."
                    ]

    font = pygame.font.SysFont("comicsans", 15)
    for num, instruction in enumerate(instructions):
        txt = font.render(instruction, True, BLACK)
        screen.blit(txt, ((WIDTH-txt.get_width())/2, (HEIGHT/(len(instructions)+1))*(num+1)))

    pygame.display.flip()


def draw_time():
    dt = int(time.time() - t0)
    minutes, seconds = 0, dt
    while seconds >= 60:
        minutes += 1
        seconds -= 60

    font = pygame.font.SysFont("comicsans", 20)
    txt = font.render(f"""{minutes if len(str(minutes)) != 1
                            else '0'+str(minutes)}:{seconds if len(str(seconds)) != 1 else 
                                                     '0'+str(seconds)}""", True, BLACK)
    screen.blit(txt, (WIDTH - txt.get_width() - 10, 10))


def is_empty():
    for block in board:
        for cell in block:
            if cell.value == 0:
                return True
    return False


def get_next(c):
    for num, block in enumerate(board):
        if c in block:
            b_index, c_index = num, block.index(c)

    if b_index not in [2, 5, 8]:
        if c_index in [2, 5, 8]:
            return b_index+1, c_index-2
        else:
            return b_index, c_index+1
    else:
        if c_index in [2, 5]:
            return b_index-2, c_index+1
        elif c_index == 8:
            return b_index+1, 0
        else:
            return b_index, c_index+1


def get_previous(c):
    for num, block in enumerate(board):
        if c in block:
            b_index, c_index = num, block.index(c)

    if b_index == 0:
        if c_index in [3, 6]:
            return b_index+2, c_index-1
        else:
            return b_index, c_index-1
    elif b_index not in [3, 6]:
        if c_index in [0, 3, 6]:
            return b_index-1, c_index+2
        else:
            return b_index, c_index-1
    else:
        if c_index in [3, 6]:
            return b_index+2, c_index-1
        elif c_index == 0:
            return b_index-1, 8
        else:
            return b_index, c_index-1


def get_repeated_cells():
    repeated_cells = []
    for same_value_cell in same_value_cells:
        if same_value_cell in hor_cells or same_value_cell in ver_cells:
            repeated_cells.append(same_value_cell)
    for block in board:
        if selected_cell in block:
            for cell in block:
                if cell in same_value_cells:
                    repeated_cells.append(cell)
    return repeated_cells


def get_same_value_cells():
    same_value_cells = []
    if selected_cell.value != 0:
        for block in board:
            for cell in block:
                if cell.value == selected_cell.value and cell != selected_cell:
                    same_value_cells.append(cell)
    return same_value_cells


def draw_screen():
    screen.fill(WHITE)
    new_game_btn.draw(screen)
    help_btn.draw(screen)
    solve_btn.draw(screen)

    draw_time()

    for number_btn in number_btns:
        if times_num.get(number_btn.number) == 9:  # Unknown origin error 'KeyError: 5', so I just put the method .get()
            number_btn.color = GREEN
        else:
            number_btn.color = RED
        number_btn.draw(screen)

    for a in board:
        for b in a:
            b.bg_color = WHITE
            if b.readonly:
                b.font_color = BLACK
            else:
                b.font_color = BLUE

    for hor in hor_cells:
        hor.bg_color = LIGHT_GREY
    for ver in ver_cells:
        ver.bg_color = LIGHT_GREY

    for same_value in same_value_cells:
        same_value.bg_color = GREY

    for repeated_cell in repeated_cells:
        repeated_cell.bg_color = LIGHT_RED

    selected_cell.bg_color = LIGHT_BLUE
    selected_cell.font_color = BLACK

    if repeated_cells:
        selected_cell.font_color = RED

    for a in board:
        for b in a:
            b.draw(screen)

    draw_lines()

    pygame.display.flip()


# Board
nums_board = get_nums_board()
board = [[Cell(nums_board[j][i]) for i in range(9)] for j in range(9)]
for block in board:
    for cell in block:
        cell.x, cell.y = cell.get_x_y(board)

# Buttons
new_game_btn = NewGameButton()
help_btn = HelpButton()
number_btns = [NumberButton(10, HEIGHT/6 + (HEIGHT/12)*i, i+1) for i in range(9)]
solve_btn = SolveButton()

# Timer
t0 = time.time()

# Vars
next, previous = True, False
selected_cell = board[0][0]
num_keys = {
    1: pygame.K_1,
    2: pygame.K_2,
    3: pygame.K_3,
    4: pygame.K_4,
    5: pygame.K_5,
    6: pygame.K_6,
    7: pygame.K_7,
    8: pygame.K_8,
    9: pygame.K_9
}

# Pygame Clock
clock = pygame.time.Clock()

# Mainloop
running = True
is_started = False
is_help = False
is_solving = False
while running:
    clock.tick(15)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN and not is_started:
            is_started = True

        if event.type == pygame.MOUSEBUTTONDOWN and is_started and not is_solving:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if is_help:
                is_help = False
            elif x_margin < mouse_x < x_margin + w and y_margin < mouse_y < y_margin + h:
                selected_cell = get_selected_cell()
            elif new_game_btn.is_collision(mouse_x, mouse_y):
                new_game_btn.draw(screen)
                pygame.display.flip()

                nums_board = get_nums_board()
                board = [[Cell(nums_board[j][i]) for i in range(9)] for j in range(9)]
                for block in board:
                    for cell in block:
                        cell.x, cell.y = cell.get_x_y(board)

                selected_cell = board[0][0]
                t0 = time.time()
            elif help_btn.is_collision(mouse_x, mouse_y):
                is_help = True
            elif solve_btn.is_collision(mouse_x, mouse_y):
                is_solving = True
                selected_cell = board[0][0]

        # Change cell value
        keys = pygame.key.get_pressed()
        for num_key in num_keys:
            if keys[num_keys[num_key]] and not selected_cell.readonly:
                selected_cell.value = num_key
        if keys[pygame.K_BACKSPACE]:
            if selected_cell.value != 0 and not selected_cell.readonly:
                selected_cell.value = 0

    if not is_started:
        draw_choice()
        continue

    if is_help:
        draw_help()
        continue

    # Do a 2 lists where are stored the hor and ver cells to change their bg_color
    hor_cells = ver_cells = []
    for block in board:
        for cell in block:
            if cell.x == selected_cell.x and cell != selected_cell:
                hor_cells.append(cell)
            if cell.y == selected_cell.y and cell != selected_cell:
                ver_cells.append(cell)

    # Select the cell that have the same value as the selected_cell
    same_value_cells = []
    if selected_cell.value != 0:
        for block in board:
            for cell in block:
                if cell.value == selected_cell.value and cell != selected_cell:
                    same_value_cells.append(cell)

    repeated_cells = get_repeated_cells()

    # How many cells have each number
    times_num = {}
    for block in board:
        for cell in block:
            if cell.value != 0:
                if times_num.get(cell.value) is None:
                    times_num[cell.value] = 0
                times_num[cell.value] += 1

    draw_screen()

    if is_solving:
        if selected_cell == board[0][0]:
            next = True
        if selected_cell.readonly:
            if next:
                nxt = get_next(selected_cell)
                selected_cell = board[nxt[0]][nxt[1]]
            elif previous:
                prev = get_previous(selected_cell)
                selected_cell = board[prev[0]][prev[1]]
        else:
            selected_cell.value += 1

            same_value_cells = get_same_value_cells()

            if selected_cell.value > 9:
                previous = True
                next = False

                selected_cell.value = 0
                prev = get_previous(selected_cell)
                selected_cell = board[prev[0]][prev[1]]
            elif not get_repeated_cells():
                next = True
                previous = False

                nxt = get_next(selected_cell)
                selected_cell = board[nxt[0]][nxt[1]]

    if selected_cell == board[8][8]:
        if not selected_cell.readonly:
            for num in times_num:
                if times_num[num] != 9:
                    selected_cell.value = num
        is_solving = False
        