from basic_animation import read_graph_from_txt, Animation, COLORS
# from collections import deque

def bfs(start, end, anime_graph, line=False): #
    anime_graph.display(anime_graph.draw_start_end, start, end)
    anime_graph.delay(5)

    visited, queue = list(), list()
    queue.append(start)

    while len(queue) != 0:
        neighbours = []
        for point in queue:
            neigh = anime_graph.get_neighbours(point)
            for nv in neigh:
                if nv not in queue and nv not in visited and nv not in neighbours:
                    neighbours.append(nv)
                    anime_graph.set_prev(nv, point)

            visited.append(point)

        anime_graph.display(anime_graph.draw_points, *neighbours, line=line)

        if end in neighbours:
            return

        queue = neighbours


def main(filename, start, end, **kwargs):
    graph = read_graph_from_txt(filename)
    anime_graph = Animation(graph, fps=3,
                            title="VFS of Path-finding Animation by BigShuang")
    anime_graph.init()



    bfs(start, end, anime_graph, **kwargs)

    anime_graph.done()


if __name__ == '__main__':
    filename = "big_shuang.txt"
    # filename = "sanlian2.txt"
    start = (2, 2)
    end = (33, 5)
    main(filename, start, end)



