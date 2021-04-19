import pygame
import sys

FPS=60 # 游戏帧率

C, R = 20, 20  # 11列， 20行
CELL_SIZE = 40  # 格子尺寸

WIN_WIDTH = CELL_SIZE * C  # 窗口宽度
WIN_HEIGHT = CELL_SIZE * R  # 窗口高度


pygame.init() # pygame初始化，必须有，且必须在开头
# 创建主窗体
clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption('Basic Board By Big Shuang')


COLORS = {
    "bg": (200, 200, 200),
    "wall": (50, 50, 50),
    "line": (175, 175, 175)
}

win.fill(COLORS["bg"])


class Block(pygame.sprite.Sprite):
    def __init__(self, c, r, size, color):
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill(color)

        self.rect = self.image.get_rect()

        x, y = c * size, r * size
        self.rect.move_ip(x, y)

class Board(pygame.sprite.Group):
    def __init__(self, master, c, r, size):
        super().__init__()
        self.master = master
        self.c = c
        self.r = r
        self.size = size

        self.board = [
            [None for i in range(c)] for j in range(r)
        ]

    def draw_wall_by_xy(self, x, y):
        ci, ri = x // self.size, y // self.size
        cell = self.board[ri][ci]

        if cell is None:
            cell = Block(ci, ri, self.size, COLORS["wall"])
            self.add(cell)
            self.board[ri][ci] = cell

    def remove_wall_by_xy(self, x, y):
        ci, ri = x // self.size, y // self.size
        cell = self.board[ri][ci]

        if cell is not None:
            self.remove(cell)
            self.board[ri][ci] = None


def draw_lines(c, r, win):
    for ci in range(c):
        cx = CELL_SIZE * ci
        pygame.draw.line(win, COLORS["line"], (cx, 0), (cx, r * CELL_SIZE))

    for ri in range(r):
        ry = CELL_SIZE * ri
        pygame.draw.line(win, COLORS["line"], (0, ry), (c * CELL_SIZE, ry))


board = Board(win, C, R, CELL_SIZE)

while True:
    # 获取所有事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 判断当前事件是否为点击右上角退出键
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Set the x, y postions of the mouse click
            ex, ey = event.pos
            if event.button == 1:
                board.draw_wall_by_xy(ex, ey)
            elif event.button == 3:
                board.remove_wall_by_xy(ex, ey)

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                ex, ey = event.pos
                board.draw_wall_by_xy(ex, ey)
            elif event.buttons[2] == 1:
                ex, ey = event.pos
                board.remove_wall_by_xy(ex, ey)


    win.fill(COLORS["bg"])
    board.draw(win)

    draw_lines(C, R, win)

    clock.tick(FPS) # 控制循环刷新频率,每秒刷新FPS对应的值的次数
    pygame.display.update()