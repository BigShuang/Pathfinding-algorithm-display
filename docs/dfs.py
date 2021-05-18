def dfs(graph, start):
    visited = []
    stack = [start]

    while stack:
        s = stack.pop()
        neighs = graph[s]
        for x in neighs:
            if x not in visited:
                visited.append(x)
                stack.append(x)
