import pycosat
from typing import *


# for each vertex i, j in [0..n) we have a proposition
# x[i,j] expressing that vertex i is the jth vertex in the Hamiltonian path
def var(i: int, j: int, n: int) -> int:
    """
    :param i: index of the vertex
    :param j: position of the vertex in the path
    :param n: number of nodes in graph
    :return: encoding of x(i, j) - number in [1..n*n]
    """
    return i * n + j + 1  # 1-indexed for pycosat


def ham_path_clauses(graph: List[List[int]]) -> List[List[int]]:
    """
    Encode this given instance of the hamiltonian path problem into SAT
    :param graph: adjacency matrix of the graph
    :return: encoding as a CNF formula
    """
    n = len(graph)
    clauses = []

    # each node i must appear in the path
    for i in range(n):
        clauses.append([var(i, j, n) for j in range(n)])

    # no node i appears twice in the path
    for j in range(n):
        for k in range(n):
            if j < k:
                for i in range(n):
                    clauses.append([-var(i, j, n), -var(i, k, n)])

    # every position j on the path must be occupied
    for j in range(n):
        clauses.append([var(i, j, n) for i in range(n)])

    # no two nodes i and j occupy the same position in the path
    for i in range(n):
        for j in range(n):
            if i < j:
                for k in range(n):
                    clauses.append([-var(i, k, n), -var(j, k, n)])

    # nonadjacent nodes i and j cannot be adjacent in the path
    for i in range(n):
        for j in range(n):
            if graph[i][j] == 0:  # (i, j) is not an edge in graph
                for k in range(n - 1):
                    clauses.append([-var(i, k, n), -var(j, k + 1, n)])

    return clauses


def solve(graph: List[List[int]]) -> List[int]:
    """
    Returns a hamiltonian path of the empty list, [], if none exists.
    :param graph: adjacency matrix of the graph
    :return: hamiltonian path as a list
    """
    solution = set(pycosat.solve(ham_path_clauses(graph)))

    if isinstance(solution, str):
        return []
    else:
        n = len(graph)
        path = []
        for i in range(n):
            for j in range(n):
                if var(i, j, n) in solution:
                    path.append(i)
                    break

        return path


def itersolve(graph: List[List[int]]) -> Iterable[List[int]]:
    n = len(graph)

    for sol in pycosat.itersolve(ham_path_clauses(graph)):
        solution = set(sol)
        path = [None for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if var(i, j, n) in solution:
                    path[j] = i
                    break

        yield path


def all_solutions(graph: List[List[int]]) -> List[List[int]]:
    solutions = []

    for sol in itersolve(graph):
        solutions.append(sol)

    return solutions
