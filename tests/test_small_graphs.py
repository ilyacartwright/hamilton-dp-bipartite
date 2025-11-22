import pytest

from hamilton_dp.intervals import TwoInterval, YVertex, TwoIntervalBipartiteGraph
from hamilton_dp.dp_solver import HamiltonianDPSolver
from hamilton_dp.backtracking import HamiltonianBacktracking


def build_hamiltonian_n3_graph() -> TwoIntervalBipartiteGraph:
    """
    Graph from example_n3:
        X0 – Y0 – X1 – Y1 – X2 – Y2 – X0
    """
    n = 3
    y_vertices = [
        YVertex(first=TwoInterval(0, 1), second=TwoInterval(None, None)),
        YVertex(first=TwoInterval(1, 2), second=TwoInterval(None, None)),
        YVertex(first=TwoInterval(0, 0), second=TwoInterval(2, 2)),
    ]
    return TwoIntervalBipartiteGraph(n=n, y_vertices=y_vertices)


def build_non_hamiltonian_n3_graph() -> TwoIntervalBipartiteGraph:
    """
    Simple non-Hamiltonian example: remove one crucial edge.

    For instance, remove edge X2–Y2 by shortening I2_y2.
    """
    n = 3
    y_vertices = [
        YVertex(first=TwoInterval(0, 1), second=TwoInterval(None, None)),
        YVertex(first=TwoInterval(1, 2), second=TwoInterval(None, None)),
        # y2 only adjacent to X0, not to X2
        YVertex(first=TwoInterval(0, 0), second=TwoInterval(None, None)),
    ]
    return TwoIntervalBipartiteGraph(n=n, y_vertices=y_vertices)


def test_hamiltonian_graph_dp_and_backtracking_agree():
    g = build_hamiltonian_n3_graph()

    dp_solver = HamiltonianDPSolver(g)
    stats = dp_solver.run()
    assert stats.accepted, "DP should accept Hamiltonian graph."

    back = HamiltonianBacktracking(g)
    cycle = back.find_cycle()
    assert cycle is not None, "Backtracking should find an explicit Hamiltonian cycle."
    assert len(cycle) == 2 * g.n


def test_non_hamiltonian_graph_dp():
    g = build_non_hamiltonian_n3_graph()

    dp_solver = HamiltonianDPSolver(g)
    stats = dp_solver.run()
    # In a perfect implementation we expect False here;
    # depending on the minimalistic T5, this test can be adapted or extended
    # for more robust non-Hamiltonian examples.
    assert not stats.accepted, "DP should reject clearly non-Hamiltonian instance (for this small example)."


def test_backtracking_detects_absence_of_cycle():
    g = build_non_hamiltonian_n3_graph()
    back = HamiltonianBacktracking(g)
    cycle = back.find_cycle()
    assert cycle is None, "Backtracking should not find a Hamiltonian cycle in a non-Hamiltonian graph."
