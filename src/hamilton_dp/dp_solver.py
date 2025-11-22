from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple
from collections import defaultdict

from .intervals import TwoIntervalBipartiteGraph


@dataclass(frozen=True)
class DPState:
    """
    DP state: (k, O, L).

    k  – number of X-vertices already processed (0..n);
    O  – sorted tuple of indices of 'open' Y-vertices (|O| <= 2);
    L  – loose-flag in X (0/1): 1 means there is a loose end in X.
    """
    k: int
    open_set: Tuple[int, ...]
    loose_flag: int


@dataclass
class DPPredecessor:
    prev_state: DPState
    transition_type: str
    added_edges: List[Tuple[str, int, str, int]]


@dataclass
class DPStats:
    total_states: int
    states_per_k: Dict[int, int]
    max_states_per_k: int
    transitions_per_type: Dict[str, int]
    accepted: bool


def check_stack_order(graph: TwoIntervalBipartiteGraph, y1: int, y2: int) -> bool:
    """
    Condition from Lemma 1(b): if y1 was opened earlier and y2 is opened now,
    we require I2_y1 > I1_y2 (in the sense that left(I2_y1) > right(I1_y2)).
    """
    yv1 = graph.y_vertices[y1]
    yv2 = graph.y_vertices[y2]
    if yv1.second.is_empty or yv2.first.is_empty:
        return False
    return yv1.second.l > yv2.first.r


class HamiltonianDPSolver:
    """
    Dynamic programming algorithm for Hamiltonian cycle existence
    in 2-interval bipartite graphs.

    NOTE: the implementation of T5 is intentionally minimalistic
    (without full degree control); for small graphs and didactic
    purposes this is sufficient, but a fully rigorous implementation
    would carry additional invariants.
    """

    def __init__(self, graph: TwoIntervalBipartiteGraph) -> None:
        self.g = graph
        self.n = graph.n

        self.reachable: Dict[DPState, bool] = {}
        self.predecessor: Dict[DPState, DPPredecessor] = {}
        self.transitions_per_type: Dict[str, int] = defaultdict(int)

    # --- Initialization at k = 1 -----------------------------------------

    def _initial_states(self) -> None:
        """
        Initialize DP after processing x0 (k = 1).

        - State with x0 as a loose endpoint: O = ∅, L = 1;
        - States where x0 is attached to some y ∈ N(x0).
        """
        g = self.g

        base = DPState(k=1, open_set=tuple(), loose_flag=1)
        self.reachable[base] = True

        x0_neighbors = g.neighbors_of_x(0)

        for y in x0_neighbors:
            yv = g.y_vertices[y]
            O: Tuple[int, ...] = tuple()
            # heuristic: y becomes 'open' only if it has a second interval
            # starting strictly to the right of x0
            if (not yv.second.is_empty) and (yv.second.l > 0):
                O = (y,)
            s = DPState(k=1, open_set=O, loose_flag=1)
            if s not in self.reachable:
                self.reachable[s] = True
                prev = DPState(k=0, open_set=tuple(), loose_flag=1)
                self.predecessor[s] = DPPredecessor(
                    prev_state=prev,
                    transition_type="INIT",
                    added_edges=[("X", 0, "Y", y)],
                )
                self.transitions_per_type["INIT"] += 1

    # --- Transitions T1–T5 -----------------------------------------------

    def _enumerate_transitions(
        self,
        state: DPState,
    ) -> Iterable[Tuple[DPState, str, List[Tuple[str, int, str, int]]]]:
        """
        Implement DP transitions (T1–T5) for vertex v = x_i, i = k.
        Returns triples (new_state, transition_type, list_of_added_edges).
        """
        g = self.g
        n = self.n
        k = state.k
        O = list(state.open_set)
        L = state.loose_flag

        if k >= n:
            return []

        i = k
        v_neighbors = g.neighbors_of_x(i)
        if not v_neighbors:
            return []

        E1, E2, E3, E4 = g.classify_events_at(i)
        Oset = set(O)
        results: List[Tuple[DPState, str, List[Tuple[str, int, str, int]]]] = []

        # --- T1: L=1, connect to closing yclose (type E3) -----------------
        if L == 1:
            for yclose in (Oset & E3):
                new_O = tuple(sorted(y for y in O if y != yclose))
                new_state = DPState(k=k + 1, open_set=new_O, loose_flag=0)
                edges = [("X", i, "Y", yclose)]
                results.append((new_state, "T1", edges))

        # --- T2: L=1, connect to new open yopen (E1 or E2) ---------------
        if L == 1:
            candidates_yopen = (E1 | E2) - Oset
            for yopen in candidates_yopen:
                if len(O) >= 2:
                    continue
                if len(O) == 1:
                    y_old = O[0]
                    if not check_stack_order(g, y_old, yopen):
                        continue
                    O_after = {y_old, yopen}
                else:
                    O_after = {yopen}
                new_O = tuple(sorted(O_after))
                new_state = DPState(k=k + 1, open_set=new_O, loose_flag=0)
                edges = [("X", i, "Y", yopen)]
                results.append((new_state, "T2", edges))

        # --- T3: L=0, connect between yclose ∈ O∩E3 and yopen ∈ E2\O -----
        if L == 0:
            for yclose in (Oset & E3):
                for yopen in (E2 - Oset):
                    O_before = [y for y in O if y != yclose]
                    if len(O_before) > 1:
                        continue
                    if len(O_before) == 1:
                        y_old = O_before[0]
                        if not check_stack_order(g, y_old, yopen):
                            continue
                        O_after = {y_old, yopen}
                    else:
                        O_after = {yopen}
                    new_O = tuple(sorted(O_after))
                    new_state = DPState(k=k + 1, open_set=new_O, loose_flag=0)
                    edges = [("X", i, "Y", yclose), ("X", i, "Y", yopen)]
                    results.append((new_state, "T3", edges))

        # --- T4: L=1, convex y at position i ------------------------------
        if L == 1:
            for y in v_neighbors:
                if not g.is_convex_at(y, i):
                    continue
                new_state = DPState(k=k + 1, open_set=tuple(sorted(O)), loose_flag=1)
                edges = [("X", i, "Y", y)]
                results.append((new_state, "T4", edges))

        # --- T5: no interval boundaries in position i ---------------------
        if not (E1 or E2 or E3 or E4):
            new_state = DPState(k=k + 1, open_set=tuple(sorted(O)), loose_flag=L)
            edges: List[Tuple[str, int, str, int]] = []
            results.append((new_state, "T5", edges))

        return results

    # --- Main DP run ------------------------------------------------------

    def run(self) -> DPStats:
        """
        Run DP across X_0, ..., X_{n-1} and collect statistics.

        Returns DPStats with acceptance flag and statistics about the DP layers.
        """
        self.reachable.clear()
        self.predecessor.clear()
        self.transitions_per_type.clear()

        self._initial_states()

        states_per_k: Dict[int, int] = defaultdict(int)

        for k in range(1, self.n):
            current_states = [s for s in self.reachable.keys() if s.k == k]
            states_per_k[k] = len(current_states)

            for state in current_states:
                if not self.reachable.get(state, False):
                    continue
                for new_state, ttype, edges in self._enumerate_transitions(state):
                    if new_state not in self.reachable:
                        self.reachable[new_state] = True
                        self.predecessor[new_state] = DPPredecessor(
                            prev_state=state,
                            transition_type=ttype,
                            added_edges=edges,
                        )
                        self.transitions_per_type[ttype] += 1

        final_state = DPState(k=self.n, open_set=tuple(), loose_flag=0)
        accepted = self.reachable.get(final_state, False)

        total_states = len(self.reachable)
        max_states_per_k = max(states_per_k.values()) if states_per_k else 0

        return DPStats(
            total_states=total_states,
            states_per_k=dict(states_per_k),
            max_states_per_k=max_states_per_k,
            transitions_per_type=dict(self.transitions_per_type),
            accepted=accepted,
        )

    def has_hamiltonian_cycle(self) -> bool:
        """Convenience wrapper: run DP and return acceptance flag."""
        stats = self.run()
        return stats.accepted
