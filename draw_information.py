
import pygame
import random
import math

pygame.init()

class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    GREEN_CYAN = (0, 100, 100)
    CYAN = (255, 0, 120)

    BACKGROUND_COLOR = (37, 37, 37)
    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst, clock_tick=60):
        self.width = width
        self.height = height
        self.clock_tick = clock_tick
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("I LOVE PASTULA <3")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

    def get_gradient(self, val, type):
        val %= 256
        val += 1
        if type == 1:
            return ((val + 50) % 256, 100, (10 // val + 120) % 256)
        if type == 2:
            return (200, (val + 50) % 256, (5 // val + 120) % 256)
        if type == 3:
            return ((val + 50) % 256, (5 // val + 120) % 256, 200)
        return (val, val, val)

def check_commands():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type != pygame.KEYDOWN:
            return True
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_r:
            return False
    return True

def draw(draw_info: DrawInformation, algo_name, ascending=True):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(f"{algo_name}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting", 1, draw_info.WHITE)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))
    sorting = draw_info.FONT.render("I - Insertion Sort | Q - Quick Sort | D - Intro Sort | H - Heap Sort", 1, draw_info.WHITE)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info: DrawInformation, color_positions=None, clear_bg=False):
    if color_positions is None:
        color_positions = {}
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i in range(len(lst)):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (lst[i] - draw_info.min_val) * draw_info.block_height
        color = draw_info.get_gradient(lst[i], 1)
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    if clear_bg:
        pygame.display.update()
    pygame.time.wait(1000 // draw_info.clock_tick)
    if check_commands() is False:
        return False

def generate_starting_list(n, min_val=0, max_val=100):
    lst = list(range(n))
    random.shuffle(lst)
    return lst

def go_through(draw_info: DrawInformation, begin=0, end=None, color=(0, 255, 0)):
    draw_list(draw_info, clear_bg=True)
    lst = draw_info.lst
    if end is None:
        end = len(lst) - 1
    for i in range(begin, end + 1):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (lst[i] - draw_info.min_val) * draw_info.block_height
        pygame.time.wait(10)
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
        pygame.display.update()
        if check_commands() is False:
            return False
