from dfs import main as dfs_solve
from bfs import main as bfs_solve

# for dfs
filename = "big_shuang.txt"
start, end = (0, 2), (33, 5)
# dfs_solve(filename, start, end)

bfs_solve(filename, start, end)