from basic_animation import read_graph_from_txt, AStarAnimation, COLORS


COLORS["visit-line"] = (0, 255, 0)
# COLORS["visited"] = (135, 206, 250)


def heuristic(a, b):
    # Manhattan distance on a square grid
    ac, ar = a
    bc, br = b
    # return (ac - bc) ** 2 + (ar - br) ** 2
    return abs(ac - bc) + abs(ar - br)


def add_pri_vertex(queue, point, priority):
    if queue:
        for i, pi in enumerate(queue):
            if pi[1] >= priority:
                queue.insert(i, (point, priority))
                return

    queue.append((point, priority))


def a_star(start, end, anime_graph, line=False):
    anime_graph.display(anime_graph.draw_start_end,
                        start, end)
    anime_graph.delay(5)

    pri_queue = [(start, 0)]
    cost_so_far = {
        start: 0
    }

    while len(pri_queue) != 0:
        current, priority = pri_queue.pop(0)
        current_data = [cost_so_far[current], heuristic(end, current), priority]
        anime_graph.add_node_data(current, current_data, "used")

        if end == current:
            anime_graph.update()
            return

        neigh = anime_graph.get_neighbours(current)
        for next_v in neigh:
            new_cost = cost_so_far[current] + 1
            if next_v not in cost_so_far or new_cost < cost_so_far[next_v]:
                cost_so_far[next_v] = new_cost
                next_v_priority = new_cost + heuristic(end, next_v)
                add_pri_vertex(pri_queue, next_v, next_v_priority)
                next_data = [new_cost, heuristic(end, next_v), next_v_priority]

                anime_graph.set_prev(next_v, current)
                anime_graph.add_node_data(next_v, next_data, "neigh")

        anime_graph.update()


def main(filename, start, end, **kwargs):
    graph = read_graph_from_txt(filename)
    anime_graph = AStarAnimation(graph, fps=5, size=44,
                            title="A Star Path-finding Animation by BigShuang")
    anime_graph.init()

    a_star(start, end, anime_graph, **kwargs)

    anime_graph.draw_path()
    anime_graph.done()


if __name__ == '__main__':
    filename = "txt/a003.txt"
    start = (10, 10)
    end = (20, 4)

    # start = (1, 1)
    # end = (6, 5)

    main(filename, start, end)
    # main(filename, start, end, line=True)



