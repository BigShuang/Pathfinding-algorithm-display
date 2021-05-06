from basic_animation import read_graph_from_txt, Animation, COLORS


def dfs(start, end, anime_graph, line=False):
    anime_graph.display(anime_graph.draw_start_end,
                        start, end)
    anime_graph.delay(15)

    visited, stack = list(), [start]

    while len(stack) != 0:
        point = stack.pop(len(stack) - 1)
        anime_graph.display(anime_graph.draw_points,
                            point, line=line)
        if end == point:
            return
        if point not in visited:
            visited.append(point)
            neigh = anime_graph.get_neighbours(point)
            for nv in neigh:
                if nv not in stack and \
                        nv not in visited:
                    stack.append(nv)
                    anime_graph.set_prev(nv, point)


def main(filename, start, end, **kwargs):
    graph = read_graph_from_txt(filename)
    anime_graph = Animation(graph, fps=10,
                            title="DFS of Path-finding Animation by BigShuang")
    anime_graph.init()

    dfs(start, end, anime_graph, **kwargs)

    anime_graph.done()


if __name__ == '__main__':
    filename = "txt/big_shuang.txt"
    # filename = "sanlian2.txt"
    start = (2, 2)
    end = (33, 5)
    main(filename, start, end)



