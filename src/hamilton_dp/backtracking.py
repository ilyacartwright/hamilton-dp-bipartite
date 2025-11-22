from __future__ import annotations
from typing import List, Optional, Tuple
from .intervals import TwoIntervalBipartiteGraph


class HamiltonianBacktracking:
    """
    Exponential-time Hamiltonian cycle constructor for bipartite graphs
    induced by a 2-interval structure.

    Used mainly to test / validate the DP algorithm on small graphs.
    """

    def __init__(self, graph: TwoIntervalBipartiteGraph) -> None:
        self.g = graph
        self.n = graph.n

    def find_cycle(self) -> Optional[List[Tuple[str, int]]]:
        """
        Try to construct a Hamiltonian cycle as an alternating sequence
        ('X', i), ('Y', j), ..., of length 2n. Returns the sequence or None.
        """
        n = self.n
        if n == 0:
            return []

        x_neighbors = self.g.neighbors_x
        y_neighbors: List[List[int]] = [[] for _ in range(n)]
        for i in range(n):
            for y in x_neighbors[i]:
                y_neighbors[y].append(i)

        visited_x = [False] * n
        visited_y = [False] * n
        path: List[Tuple[str, int]] = []

        def is_edge(i: int, y: int) -> bool:
            return y in x_neighbors[i]

        def dfs(current_is_x: bool, current_idx: int) -> bool:
            # Full alternating path reached
            if len(path) == 2 * n:
                first_type, first_idx = path[0]
                if current_is_x == (first_type == "X"):
                    return False
                if current_is_x:
                    return is_edge(current_idx, first_idx)
                else:
                    return is_edge(first_idx, current_idx)

            if current_is_x:
                # X -> Y
                for y in x_neighbors[current_idx]:
                    if visited_y[y]:
                        continue
                    visited_y[y] = True
                    path.append(("Y", y))
                    if dfs(False, y):
                        return True
                    path.pop()
                    visited_y[y] = False
            else:
                # Y -> X
                for i in y_neighbors[current_idx]:
                    if visited_x[i]:
                        continue
                    visited_x[i] = True
                    path.append(("X", i))
                    if dfs(True, i):
                        return True
                    path.pop()
                    visited_x[i] = False

            return False

        # Try starting from each X-vertex
        for start in range(n):
            for i in range(n):
                visited_x[i] = False
                visited_y[i] = False
            path.clear()
            visited_x[start] = True
            path.append(("X", start))
            if dfs(True, start):
                return path

        return None
