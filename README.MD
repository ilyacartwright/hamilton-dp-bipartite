# hamilton-dp — Dynamic Programming Algorithm for Hamiltonian Cycles in 2-Interval Bipartite Graphs

This repository contains a reference implementation of a polynomial-time dynamic programming algorithm for detecting Hamiltonian cycles in 2-interval bipartite graphs, based on the theoretical model described in the associated research manuscript.

The project includes:

- A 2-interval graph data model (bipartite: X-side with natural ordering, Y-side with two disjoint intervals);
- A DP solver implementing transitions (T1–T5) from the paper;
- A backtracking exponential solver for constructing explicit Hamiltonian cycles in small graphs;
- Visualization tools (interval diagram, bipartite cycle layout);
- Automatic report generation (Markdown + PNG figures).

The repository is designed both for academic reproducibility and for practical exploration of the theory.

------------------------------------------------------------

## Installation

Clone the repository:

`git clone https://github.com/ilyacartwright/hamilton-dp-bipartite.git`  
`cd hamilton-dp-bipartite`

Install in editable mode:

`pip install -e .`

Requirements: Python ≥ 3.10, matplotlib.

------------------------------------------------------------

## Project Structure

hamilton-dp-bipartite/  
  README.md  
  LICENSE  
  pyproject.toml  
  src/  
    hamilton_dp/  
      __init__.py  
      intervals.py  
      dp_solver.py  
      backtracking.py  
      visualization.py  
      report.py  
  examples/  
    example_n3.py  
  tests/  
    test_small_graphs.py  

------------------------------------------------------------

## Quick Start

Run the example:

`python examples/example_n3.py`

This will:

1. Construct a small 2-interval bipartite graph with n = 3;
2. Run the DP algorithm;
3. Run the backtracking constructor (if DP accepts);
4. Produce:

example_report_true.md  
example_report_true_intervals.png  
example_report_true_cycle.png  

------------------------------------------------------------

## Usage as a Library

from hamilton_dp.intervals import TwoInterval, YVertex, TwoIntervalBipartiteGraph  
from hamilton_dp.dp_solver import HamiltonianDPSolver  
from hamilton_dp.backtracking import HamiltonianBacktracking  
from hamilton_dp.report import run_full_report  

n = 3  
y_vertices = [  
    YVertex(first=TwoInterval(0, 1), second=TwoInterval(None, None)),  
    YVertex(first=TwoInterval(1, 2), second=TwoInterval(None, None)),  
    YVertex(first=TwoInterval(0, 0), second=TwoInterval(2, 2)),  
]  

g = TwoIntervalBipartiteGraph(n=n, y_vertices=y_vertices)

solver = HamiltonianDPSolver(g)  
stats = solver.run()  
print("DP accepted:", stats.accepted)

back = HamiltonianBacktracking(g)  
cycle = back.find_cycle()  
print("Cycle:", cycle)

run_full_report(g, prefix="my_graph")

------------------------------------------------------------

## Theory Summary

A 2-interval bipartite graph consists of:

- X = {x0, x1, ..., x(n-1)} (totally ordered);
- Y = {y0, ..., y(n-1)};
- Each y_j has two disjoint intervals I1_j, I2_j;
- Edge (x_i, y_j) exists iff i ∈ I1_j ∪ I2_j.

DP state:

(k, O, L)

k — number of processed X vertices  
O — up to two “open” Y vertices  
L — loose X-end flag  

DP accepts a Hamiltonian cycle iff:

(k = n, O = ∅, L = 0)

------------------------------------------------------------

## Testing

`pytest tests`

------------------------------------------------------------

## Visualization

Automatically generated:

- Interval structure: *_intervals.png  
- Hamiltonian cycle layout: *_cycle.png

------------------------------------------------------------

## Contact

Author: Mihails Iljicevs  
Institution: Immanuel Kant Baltic Federal University  
Email: miilichevs@stud.kantiana.ru

------------------------------------------------------------

## License

MIT License — see LICENSE.