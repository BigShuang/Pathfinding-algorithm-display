import pygame
import sys

FPS=60 # 游戏帧率

C, R = 45, 20  # 列， 行
CELL_SIZE = 40  # 格子尺寸

PADDING = {
    "left": 0,
    "right": 0,
    "top": 50,
    "bottom": 50,
}


WIN_WIDTH = CELL_SIZE * C + PADDING["left"] + PADDING["right"]  # 窗口宽度
WIN_HEIGHT = CELL_SIZE * R + PADDING["top"] + PADDING["bottom"]  # 窗口高度


pygame.init() # pygame初始化，必须有，且必须在开头
# 创建主窗体
clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption('Basic Board By Big Shuang')

center_surface = pygame.Surface((CELL_SIZE * C, CELL_SIZE * R))

# 大中小三种字体，48,36,24
FONTS = [
    pygame.font.Font(pygame.font.get_default_font(), font_size) for font_size in [48, 36, 24]
]


COLORS = {
    "bg": (150,150,150),
    "board": (200, 200, 200),
    "wall": (50, 50, 50),
    "line": (175, 175, 175),
    "menu": (65, 105, 225)
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
        if ci < 0 or ri < 0 or ci >= self.c or ri >= self.r:
            return
        cell = self.board[ri][ci]

        if cell is None:
            cell = Block(ci, ri, self.size, COLORS["wall"])
            self.add(cell)
            self.board[ri][ci] = cell

    def remove_wall_by_xy(self, x, y):
        ci, ri = x // self.size, y // self.size
        if ci < 0 or ri < 0 or ci >= self.c or ri >= self.r:
            return

        cell = self.board[ri][ci]

        if cell is not None:
            self.remove(cell)
            self.board[ri][ci] = None

    def to_txt(self):
        ss = []
        for row in self.board:
            row_str = []
            for cell in row:
                if cell is None:
                    row_str.append("0")
                else:
                    row_str.append("1")
            ss.append(" ".join(row_str))

        return "\n".join(ss)

    def load_txt(self, filename):
        with open(filename, 'r') as f:
            fl = f.read()
        lines = fl.split("\n")
        if len(lines) != R:
            print("txt r is not valid")
            return

        for line in lines:
            line = line.replace(" ", "")
            if len(line) != C:
                print("txt c is not valid")
                return

        self.empty()

        for ri, line in enumerate(lines):
            line = line.replace(" ", "")
            for ci, cell in enumerate(line):
                if cell == "1":
                    cell = Block(ci, ri, self.size, COLORS["wall"])
                    self.add(cell)
                    self.board[ri][ci] = cell
                elif cell == "0":
                    self.board[ri][ci] = None
                else:
                    self.board[ri][ci] = None


def draw_lines(c, r, win):
    for ci in range(c):
        cx = CELL_SIZE * ci
        pygame.draw.line(win, COLORS["line"], (cx, 0), (cx, r * CELL_SIZE))

    for ri in range(r):
        ry = CELL_SIZE * ri
        pygame.draw.line(win, COLORS["line"], (0, ry), (c * CELL_SIZE, ry))


def draw_menu_1(left, top, font):
    save = font.render("Ctrl+S to Save. Ctrl+D to load", True, COLORS["menu"])
    text_rect = save.get_rect(midleft=(left, top / 2))
    win.blit(save, text_rect)


def save_to_txt(board, filename):
    try:
        with open(filename, 'w') as f:
            f.write(board.to_txt())
        print("Saved to %s." % filename)
    except Exception as e:
        print("save failed:", e)



board = Board(win, C, R, CELL_SIZE)


draw_menu_1(PADDING["left"], PADDING["top"], FONTS[1])


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
                board.draw_wall_by_xy(ex - PADDING["left"], ey - PADDING["top"])
            elif event.button == 3:
                board.remove_wall_by_xy(ex - PADDING["left"], ey - PADDING["top"])

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                ex, ey = event.pos
                board.draw_wall_by_xy(ex - PADDING["left"], ey - PADDING["top"])
            elif event.buttons[2] == 1:
                ex, ey = event.pos
                board.remove_wall_by_xy(ex - PADDING["left"], ey - PADDING["top"])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    filename = input("Please input file name: ")
                    save_to_txt(board, filename)
            elif event.key == pygame.K_d:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    filename = input("Please input file name:")
                    try:
                        board.load_txt(filename)
                    except Exception as e:
                        print("Load failed:", e)

    center_surface.fill(COLORS["board"])
    board.draw(center_surface)
    draw_lines(C, R, center_surface)
    win.blit(center_surface, (PADDING["left"], PADDING["top"]))

    clock.tick(FPS) # 控制循环刷新频率,每秒刷新FPS对应的值的次数
    pygame.display.update()