import pygame
import os


pygame.init()
FONTS = [
    pygame.font.Font(pygame.font.get_default_font(), font_size) for font_size in [48, 36, 16, 12]
]
DEFAULT_FONT = 2


COLORS = {
    "bg": (200, 200, 200),  # 背景颜色
    "select": (0, 139, 139),
    "current": (255, 192, 203),
    "line": (175, 175, 175),
    "wall": (50, 50, 50),
    "start": (65, 105, 225),  # RoyalBlue
    "end": (0, 128, 0),
    "visited":(153, 50, 204),
    "current-text": (255,255,255),
    "visited-text": (255,255,255),
    "visit-line": (0, 255, 0),

    "cost-text": (255, 255, 255),
    "heuristic-text": (255, 255, 255),
    "priority-text": (255,255,0),
}


COLORS["current"] = (135, 206, 250)
COLORS["visited"] = (100, 100, 125)
COLORS["wall"] = (251, 114, 153)

DIRECTIONS = {
    "UP": (0, -1),
    "RIGHT": (1, 0),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
}

pos_x, pos_y = 40, 50


class NodeValueError(Exception):
    pass


def read_graph_from_txt(filename):
    with open(filename, 'r') as f:
        lines = f.read().split("\n")
    graph = []
    for line in lines:
        row = []
        line = line.replace(" ", "")
        for cell in line:
            if cell == "0":
                row.append("0")
            elif cell == "1":
                row.append("1")
            else:
                raise NodeValueError("Invalid cell value: %s" % cell)
        if row:
            graph.append(row)

    return graph


class BasicAnimation():
    def __init__(self, graph_list, size, title, fps):
        self.clock = pygame.time.Clock()

        self.r = len(graph_list)
        self.c = len(graph_list[0])
        self.cell_size = size

        # 设置窗口位置
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (pos_x, pos_y)
        width, height = self.c * self.cell_size, self.r * self.cell_size
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.graph = graph_list
        self.fps = fps

        self.win.fill(COLORS["bg"])
        self.start = None
        self.end = None

        self.last_points = None
        self.count = 0

    def init(self):
        self.display(self.draw_graph)

    def draw_cell(self, ci, ri, color):
        rect = (ci * self.cell_size, ri * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.win, COLORS[color], rect)

    def draw_graph(self):
        for ri, row in enumerate(self.graph):
            for ci, cell in enumerate(row):
                if cell == "1":
                    self.draw_cell(ci, ri, "wall")

    def draw_line(self, line_color="line"):  # 绘制方格线
        for ci in range(self.c):
            cx = self.cell_size * ci
            pygame.draw.line(self.win, COLORS[line_color], (cx, 0), (cx, self.r * self.cell_size))

        for ri in range(self.r):
            ry = self.cell_size * ri
            pygame.draw.line(self.win, COLORS[line_color], (0, ry), (self.c * self.cell_size, ry))

    def draw_start_end(self, start, end):
        self.start = start
        self.end = end
        sc, sr = self.start
        self.draw_cell(sc, sr, "start")
        ec, er = self.end
        self.draw_cell(ec, er, "end")

    def get_neighbours(self, point):
        neigh = []
        pc, pr = point
        for d in DIRECTIONS:
            dc, dr = DIRECTIONS[d]
            nc, nr = pc + dc, pr + dr
            if nc < 0 or nc >= self.c or nr < 0 or nr >= self.r:
                continue

            if self.graph[nr][nc] == "0":
                neigh.append((nc, nr))

        return neigh

    def display(self, func=None, *args, **kwargs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 判断当前事件是否为点击右上角退出键
                pygame.quit()

        if func:
            func(*args, **kwargs)

        self.draw_line()
        pygame.display.update()
        self.clock.tick(self.fps)

    def update(self):
        pygame.display.update()
        self.clock.tick(self.fps)

    def delay(self, tc):
        for _ in range(tc):
            self.clock.tick(self.fps)
            pygame.display.update()

    def done(self):
        while True:
            # 获取所有事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 判断当前事件是否为点击右上角退出键
                    pygame.quit()
                    return

            self.clock.tick(self.fps)
            pygame.display.update()


class Animation(BasicAnimation):
    def __init__(self, graph_list, size=32, title="Path-finding Animation by BigShuang",
                 fps=30):
        super().__init__(self, graph_list, size, title, fps)

        self.depth_map = [
            [None for i in range(self.c)] for j in range(self.r)  # prev_cr, depth
        ]

    def draw_start_end(self, start, end):
        super().draw_cell(self, start, end)
        self.depth_map[sr][sc] = (None, 0)

    def draw_count(self, ci, ri, kind, size=2):
        text = FONTS[size].render("%s" % self.depth_map[ri][ci][1], True, COLORS[kind+"-text"])
        cx, cy = ci * self.cell_size + self.cell_size // 2, ri * self.cell_size + self.cell_size // 2
        text_rect = text.get_rect(center=(cx, cy))
        self.win.blit(text, text_rect)

    def draw_vline(self, v, prev_v):
        end_pos = (v[0] * self.cell_size + self.cell_size // 2,
                   v[1] * self.cell_size + self.cell_size // 2)
        start_pos = (prev_v[0] * self.cell_size + self.cell_size // 2,
                     prev_v[1] * self.cell_size + self.cell_size // 2)
        pygame.draw.line(self.win, COLORS["visit-line"], start_pos, end_pos, width=3)

    def set_prev(self, v, prev_v):
        vc, vr = v
        pvc, pvr = prev_v
        depth = self.depth_map[pvr][pvc][1] + 1
        self.depth_map[vr][vc] = (prev_v, depth)

    def draw_points(self, *points, **kwargs):
        size = kwargs.get("size", DEFAULT_FONT)
        draw_line = kwargs.get("line", False)
        # 绘制图形
        if self.last_points:
            for point in self.last_points:
                pc, pr = point
                self.draw_cell(pc, pr, "visited")
                if draw_line:
                    prev_v, depth = self.depth_map[pr][pc]
                    if prev_v:
                        self.draw_vline(point, prev_v)
                else:
                    self.draw_count(pc, pr, "visited", size)

        # 绘制计数
        self.count += 1
        for point in points:
            pc, pr = point
            self.draw_cell(pc, pr, "current")
            if self.depth_map[pr][pc] is not None:
                if draw_line:
                    prev_v, depth = self.depth_map[pr][pc]
                    if prev_v:
                        self.draw_vline(point, prev_v)
                else:
                    self.draw_count(pc, pr, "current", size)

        self.last_points = points


class AStarAnimation(BasicAnimation):
    def __init__(self, graph_list, size=48, title="Path-finding Animation by BigShuang",
                 fps=30):
        super().__init__(graph_list, size, title, fps)

        self.prev_map = {
            # cur_vertex: prev_vertex
        }

    def draw_count(self, ci, ri, kind, values, size=2):
        tlst = [
            FONTS[size].render("%s" % values[0], True, COLORS["cost-text"]),
            FONTS[size].render("%s" % values[1], True, COLORS["heuristic-text"]),
            FONTS[size].render("%s" % values[2], True, COLORS["priority-text"])
        ]

        top, left = ri * self.cell_size, ci * self.cell_size
        quarter = self.cell_size // 4
        cxy_list = [
            (left + quarter, top + quarter),
            (left + 3 * quarter, top + quarter),
            (left + 2 * quarter, top + 3 * quarter),
        ]
        for i in range(3):
            cxy = cxy_list[i]
            text_rect = tlst[i].get_rect(center=cxy)
            self.win.blit(tlst[i], text_rect)

    def draw_astar_points(self, *points, **kwargs):
        size = kwargs.get("size", DEFAULT_FONT)
        kind = kwargs.get("kind")
        draw_line = kwargs.get("line", False)
        values = kwargs.get("values")
        # 绘制
        self.count += 1
        for point in points:
            pc, pr = point
            self.draw_cell(pc, pr, kind)
            self.draw_count(pc, pr, kind, values, size=2)

    def set_prev(self, next_v, current):
        self.prev_map[next_v] = current


if __name__ == '__main__':
    filename = "txt/big_shuang.txt"
    graph = read_graph_from_txt(filename)
    anima = Animation(graph)
    anima.display(anima.init)

    start = (2, 2)
    end = (37, 14)
    anima.display(anima.draw_start_end, start, end)

    anima.done()