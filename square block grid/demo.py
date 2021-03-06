from dfs import main as dfs_solve
from bfs import main as bfs_solve

# for dfs
filename = "txt/big_shuang.txt"
start, end = (0, 2), (32, 4)
# dfs_solve(filename, start, end)
dfs_solve(filename, start, end, line=True)

# filename = "txt/sanlian2.txt"
# start, end = (0, 2), (33, 5)
# dfs_solve(filename, start, end, line=True)

# for bfs
# filename = "big_shuang.txt"
# start, end = (0, 2), (33, 5)
# bfs_solve(filename, start, end, line=True)
# bfs_solve(filename, start, end)

# filename = "txt/sanlian2.txt"
# start, end = (0, 2), (33, 5)
# bfs_solve(filename, start, end, line=True)
# bfs_solve(filename, start, end)