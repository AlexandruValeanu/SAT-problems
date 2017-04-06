import pycosat
from typing import *

colours = [1, 2, 3]


# for each vertex i, j in [0..n) we have a proposition
# x[i,j] expressing that vertex i is has the jth colour
def var(i: int, j: int, n: int) -> int:
    return i * n + j


def three_colour_clauses(graph: List[List[int]]) -> List[List[int]]:
    n = len(graph)
    clauses = []

    # each vertex has at least one colour
    for i in range(n):
        clauses.append([var(i, c, n) for c in colours])

    # each vertex has at most one colour:
    for c in colours:
        for cc in colours:
            if c != cc:
                for k in range(n):
                    clauses.append([-var(k, c, n), -var(k, cc, n)])

    # adjacent vertices have different colours
    for i in range(n):
        for j in range(n):
            if graph[i][j] == 1:  # (i, j) is an edge in graph
                for c in colours:
                    clauses.append([-var(i, c, n), -var(j, c, n)])

    return clauses


def check_solution(graph: List[List[int]], colouring: List[int]) -> bool:
    n = len(graph)

    for i in range(n):
        for j in range(n):
            if graph[i][j] == 1 and colouring[i] == colouring[j]:
                return False

    return True


def solve(graph: List[List[int]]) -> List[int]:
    solution = set(pycosat.solve(three_colour_clauses(graph)))

    if isinstance(solution, str):
        return []
    else:
        n = len(graph)
        cols = [0 for _ in range(n)]

        for i in range(n):
            for j in colours:
                if var(i, j, n) in solution:
                    cols[i] = j
                    break

        assert check_solution(graph, cols)
        return cols


def itersolve(graph: List[List[int]]) -> Iterable[List[int]]:
    n = len(graph)

    for sol in pycosat.itersolve(three_colour_clauses(graph)):
        solution = set(sol)
        cols = [0 for _ in range(n)]

        for i in range(n):
            for j in colours:
                if var(i, j, n) in solution:
                    cols[i] = j
                    break

        assert check_solution(graph, cols)
        yield cols


def all_solutions(graph: List[List[int]]) -> List[List[int]]:
    solutions = []

    for sol in itersolve(graph):
        solutions.append(sol)

    return solutions
