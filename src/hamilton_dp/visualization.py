from __future__ import annotations

from typing import List, Tuple
import matplotlib.pyplot as plt
from .intervals import TwoIntervalBipartiteGraph


def plot_interval_structure(
    graph: TwoIntervalBipartiteGraph,
    filename: str = "intervals.png",
) -> None:
    """
    Plot 2-interval structure: X indices on the horizontal axis, Y indices vertically.
    """
    n = graph.n
    fig, ax = plt.subplots(figsize=(8, max(3, n * 0.3)))

    for y, yv in enumerate(graph.y_vertices):
        for idx, it in enumerate((yv.first, yv.second), start=1):
            if it.is_empty:
                continue
            ax.hlines(y, it.l, it.r, linewidth=2)
            ax.plot([it.l, it.r], [y, y], "o", markersize=4)
            ax.text(
                (it.l + it.r) / 2,
                y + 0.1,
                f"I{idx}",
                ha="center",
                va="bottom",
                fontsize=7,
            )

    ax.set_xlabel("X-index")
    ax.set_ylabel("Y-index")
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(-1, n)
    ax.set_yticks(range(n))
    ax.set_title("2-interval structure of the graph")
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close(fig)


def plot_cycle(
    graph: TwoIntervalBipartiteGraph,
    cycle: List[Tuple[str, int]],
    filename: str = "cycle.png",
) -> None:
    """
    Simple bipartite layout: X-vertices on the left, Y-vertices on the right,
    with cycle edges drawn as straight segments.
    """
    n = graph.n
    x_positions = {i: (0, n - 1 - i) for i in range(n)}
    y_positions = {j: (2, n - 1 - j) for j in range(n)}

    fig, ax = plt.subplots(figsize=(4, max(3, n * 0.3)))

    # vertices
    for i in range(n):
        x, y = x_positions[i]
        ax.plot(x, y, "o")
        ax.text(x - 0.05, y, f"x{i}", ha="right", va="center", fontsize=8)

    for j in range(n):
        x, y = y_positions[j]
        ax.plot(x, y, "o")
        ax.text(x + 0.05, y, f"y{j}", ha="left", va="center", fontsize=8)

    # edges of the cycle
    for (t1, i1), (t2, i2) in zip(cycle, cycle[1:] + cycle[:1]):
        if t1 == "X" and t2 == "Y":
            x1, y1 = x_positions[i1]
            x2, y2 = y_positions[i2]
        elif t1 == "Y" and t2 == "X":
            x1, y1 = y_positions[i1]
            x2, y2 = x_positions[i2]
        else:
            continue
        ax.plot([x1, x2], [y1, y2], "-", linewidth=1)

    ax.set_axis_off()
    ax.set_title("Hamiltonian cycle (bipartite visualization)")

    plt.tight_layout()
    fig.savefig(filename, dpi=200)
    plt.close(fig)
