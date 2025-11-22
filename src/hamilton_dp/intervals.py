from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple, Set


@dataclass(frozen=True)
class TwoInterval:
    """
    Closed interval [l, r] on the X side, or empty if l or r is None.

    Indices are 0-based and inclusive: 0 <= l <= r < n.
    """
    l: Optional[int]
    r: Optional[int]

    @property
    def is_empty(self) -> bool:
        return self.l is None or self.r is None

    def contains(self, i: int) -> bool:
        if self.is_empty:
            return False
        return self.l <= i <= self.r

    def is_left_endpoint(self, i: int) -> bool:
        return (not self.is_empty) and self.l == i

    def is_right_endpoint(self, i: int) -> bool:
        return (not self.is_empty) and self.r == i

    def strictly_inside(self, i: int) -> bool:
        if self.is_empty:
            return False
        return self.l < i < self.r


@dataclass
class YVertex:
    """
    Vertex from the Y-part of the bipartite graph.

    first  – first interval I1_y
    second – second interval I2_y (may be empty)
    """
    first: TwoInterval
    second: TwoInterval


@dataclass
class TwoIntervalBipartiteGraph:
    """
    Bipartite graph G = (X, Y, E) with a 2-interval structure on side X.

    Assumptions:
    - |X| = |Y| = n
    - X = {0, 1, ..., n-1}
    - for each y, I1_y and I2_y are non-overlapping intervals with a gap:
      if both non-empty, then r(I1_y) < l(I2_y).
    """
    n: int
    y_vertices: List[YVertex]

    def __post_init__(self) -> None:
        assert len(self.y_vertices) == self.n, "Expected |Y| = n."

        for yv in self.y_vertices:
            for it in (yv.first, yv.second):
                if not it.is_empty:
                    assert 0 <= it.l <= it.r < self.n
            if (not yv.first.is_empty) and (not yv.second.is_empty):
                assert yv.first.r < yv.second.l, "Intervals I1 and I2 must be disjoint and ordered."

        # Build adjacency lists X -> Y and edge set for convenience / reporting.
        self.neighbors_x: List[List[int]] = [[] for _ in range(self.n)]
        self.edges: Set[Tuple[str, int, str, int]] = set()

        for y_idx, yv in enumerate(self.y_vertices):
            for it in (yv.first, yv.second):
                if it.is_empty:
                    continue
                for i in range(it.l, it.r + 1):
                    self.neighbors_x[i].append(y_idx)
                    self.edges.add(("X", i, "Y", y_idx))

    # --- Events E1–E4 -----------------------------------------------------

    def classify_events_at(self, i: int) -> Tuple[Set[int], Set[int], Set[int], Set[int]]:
        """
        For vertex x_i return four sets:

        E1: all y such that i is the left endpoint of I1_y;
        E2: all y such that i is the right endpoint of I1_y;
        E3: all y such that i is the left endpoint of I2_y;
        E4: all y such that i is the right endpoint of I2_y.
        """
        E1, E2, E3, E4 = set(), set(), set(), set()

        for y, yv in enumerate(self.y_vertices):
            if yv.first.is_left_endpoint(i):
                E1.add(y)
            if yv.first.is_right_endpoint(i):
                E2.add(y)
            if yv.second.is_left_endpoint(i):
                E3.add(y)
            if yv.second.is_right_endpoint(i):
                E4.add(y)

        return E1, E2, E3, E4

    # --- Neighbourhood helpers -------------------------------------------

    def neighbors_of_x(self, i: int) -> List[int]:
        """Return indices of Y-neighbours of x_i."""
        return self.neighbors_x[i] if 0 <= i < self.n else []

    def is_convex_at(self, y: int, i: int) -> bool:
        """
        'Convex at position i' in the sense used in the DP T4 rule:
        all neighbours of y are contained in {x_0, ..., x_i}.

        In the 2-interval representation this is equivalent to:
            max(r1, r2) <= i   (for all non-empty intervals).
        """
        yv = self.y_vertices[y]
        rs = []
        if not yv.first.is_empty:
            rs.append(yv.first.r)
        if not yv.second.is_empty:
            rs.append(yv.second.r)
        if not rs:
            return False
        return max(rs) <= i
