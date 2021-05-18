from basic_animation import read_graph_from_txt, Animation, COLORS


def bfs(start, end, anime_graph, line=False):
    anime_graph.display(anime_graph.draw_start_end,
                        start, end)
    anime_graph.delay(5)

    visited, queue = [start], [start]

    while len(queue) != 0:
        point = queue.pop(0)
        anime_graph.display(anime_graph.draw_points,
                            point, line=line)
        if end == point:
            return

        neigh = anime_graph.get_neighbours(point)
        for nv in neigh:
            if nv not in visited:
                queue.append(nv)
                visited.append(nv)
                anime_graph.set_prev(nv, point)


def main(filename, start, end, **kwargs):
    graph = read_graph_from_txt(filename)
    anime_graph = Animation(graph, fps=12,
                            title="BFS of Path-finding Animation by BigShuang")
    anime_graph.init()

    bfs(start, end, anime_graph, **kwargs)

    anime_graph.done()


if __name__ == '__main__':
    filename = "txt/big_shuang.txt"
    # filename = "sanlian2.txt"
    start = (2, 2)
    end = (33, 5)
    main(filename, start, end)



