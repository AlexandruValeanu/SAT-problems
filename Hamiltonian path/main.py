import ham_path_solver
import pprint

grdodec = {0: [1, 4, 5],
           1: [0, 7, 2],
           2: [1, 9, 3],
           3: [2, 11, 4],
           4: [3, 13, 0],
           5: [0, 14, 6],
           6: [5, 16, 7],
           7: [6, 8, 1],
           8: [7, 17, 9],
           9: [8, 10, 2],
           10: [9, 18, 11],
           11: [10, 3, 12],
           12: [11, 19, 13],
           13: [12, 14, 4],
           14: [13, 15, 5],
           15: [14, 16, 19],
           16: [6, 17, 15],
           17: [16, 8, 18],
           18: [10, 19, 17],
           19: [18, 12, 15]}

grherschel = {0: [1, 9, 10, 7],
              1: [0, 8, 2],
              2: [1, 9, 3],
              3: [2, 8, 4],
              4: [3, 9, 10, 5],
              5: [4, 8, 6],
              6: [5, 10, 7],
              7: [6, 8, 0],
              8: [1, 3, 5, 7],
              9: [2, 0, 4],
              10: [6, 4, 0]}


def build_graph(gr):
    n = len(grdodec)
    g = [[0 for _ in range(n)] for _ in range(n)]

    for (v, ls) in gr.items():
        for u in ls:
            g[v][u] = 1

    return g


gg = [[0, 1, 0],
      [1, 0, 1],
      [0, 1, 0]]

for sol in ham_path_solver.itersolve(gg):
    print(sol)
