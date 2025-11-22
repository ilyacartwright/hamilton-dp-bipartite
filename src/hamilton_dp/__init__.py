"""
Public API for the hamilton_dp package.
"""

from .intervals import TwoInterval, YVertex, TwoIntervalBipartiteGraph
from .dp_solver import (
    DPState,
    DPPredecessor,
    DPStats,
    HamiltonianDPSolver,
)
from .backtracking import HamiltonianBacktracking
from .visualization import plot_interval_structure, plot_cycle
from .report import generate_markdown_report, run_full_report

__all__ = [
    "TwoInterval",
    "YVertex",
    "TwoIntervalBipartiteGraph",
    "DPState",
    "DPPredecessor",
    "DPStats",
    "HamiltonianDPSolver",
    "HamiltonianBacktracking",
    "plot_interval_structure",
    "plot_cycle",
    "generate_markdown_report",
    "run_full_report",
]
