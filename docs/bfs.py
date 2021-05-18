def bfs(graph, start):
    visited = []
    queue = [start]

    while queue:
        s = queue.pop(0)
        neighs = graph[s]
        for x in neighs:
            if x not in visited:
                visited.append(x)
                queue.append(x)
