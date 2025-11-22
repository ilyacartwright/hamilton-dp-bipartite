from __future__ import annotations

from typing import List, Optional, Tuple, Dict
import os

from .intervals import TwoIntervalBipartiteGraph
from .dp_solver import DPStats, HamiltonianDPSolver
from .backtracking import HamiltonianBacktracking
from .visualization import plot_interval_structure, plot_cycle


def generate_markdown_report(
    graph: TwoIntervalBipartiteGraph,
    dp_stats: DPStats,
    cycle: Optional[List[Tuple[str, int]]],
    md_filename: str = "report.md",
    intervals_png: str = "intervals.png",
    cycle_png: Optional[str] = "cycle.png",
) -> str:
    """
    Generate a Markdown report summarizing DP results, statistics, and
    the (optional) Hamiltonian cycle found by backtracking.
    """
    n = graph.n
    m = len(graph.edges)

    lines: List[str] = []

    lines.append("# Отчёт по гамильтонову циклу в 2-интервальном двудольном графе\n")
    lines.append("## 1. Общая информация о графе\n")
    lines.append(f"- Число вершин в каждой доле: `n = {n}`")
    lines.append(f"- Число рёбер: `m = {m}`\n")

    lines.append("## 2. Результаты DP-алгоритма\n")
    lines.append(
        f"- Состояние приёмки: `{dp_stats.accepted}` "
        "(существует ли гамильтонов цикл по DP)."
    )
    lines.append(
        f"- Общее число достижимых состояний DP: `{dp_stats.total_states}`"
    )
    lines.append(
        f"- Максимальное число состояний на одном слое по k: "
        f"`{dp_stats.max_states_per_k}`\n"
    )

    lines.append("### 2.1. Распределение числа состояний по k\n")
    lines.append("| k | # состояний |")
    lines.append("|---|-------------|")
    for k in sorted(dp_stats.states_per_k.keys()):
        lines.append(f"| {k} | {dp_stats.states_per_k[k]} |")
    lines.append("")

    lines.append("### 2.2. Использование типов переходов (T1–T5)\n")
    lines.append("| Тип | Количество применений |")
    lines.append("|-----|------------------------|")
    for ttype in sorted(dp_stats.transitions_per_type.keys()):
        lines.append(f"| {ttype} | {dp_stats.transitions_per_type[ttype]} |")
    lines.append("")

    lines.append("## 3. Интервальная структура графа\n")
    if intervals_png and os.path.exists(intervals_png):
        lines.append(f"![Интервальная структура]({intervals_png})\n")
    else:
        lines.append("_Файл с интервалами не найден, рисунок не встроен._\n")

    lines.append("## 4. Гамильтонов цикл\n")

    if cycle is None:
        lines.append(
            "По backtracking-алгоритму гамильтонов цикл **не найден**.\n"
        )
    else:
        lines.append(
            "По backtracking-алгоритму гамильтонов цикл **найден**.\n"
        )
        lines.append("### 4.1. Последовательность вершин цикла\n")
        pretty = " → ".join(f"{t}{i}" for t, i in cycle)
        if cycle:
            first_t, first_i = cycle[0]
            pretty += f" → {first_t}{first_i}"
        lines.append(f"`{pretty}`\n")

        if cycle_png and os.path.exists(cycle_png):
            lines.append("### 4.2. Графическая визуализация цикла\n")
            lines.append(f"![Гамильтонов цикл]({cycle_png})\n")

    text = "\n".join(lines)
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(text)

    return text


def run_full_report(
    graph: TwoIntervalBipartiteGraph,
    prefix: str = "hamilton_report",
) -> None:
    """
    End-to-end pipeline:

    1. Run DP algorithm and collect statistics;
    2. Visualize interval structure;
    3. If DP accepts, run backtracking to construct a Hamiltonian cycle;
    4. If a cycle is found, visualize it;
    5. Generate a Markdown report.

    Produces:
        {prefix}.md
        {prefix}_intervals.png
        (optionally) {prefix}_cycle.png
    """
    dp_solver = HamiltonianDPSolver(graph)
    dp_stats = dp_solver.run()

    intervals_png = f"{prefix}_intervals.png"
    plot_interval_structure(graph, intervals_png)

    cycle = None
    cycle_png = None
    if dp_stats.accepted:
        back = HamiltonianBacktracking(graph)
        cycle = back.find_cycle()
        if cycle is not None:
            cycle_png = f"{prefix}_cycle.png"
            plot_cycle(graph, cycle, cycle_png)

    md_filename = f"{prefix}.md"
    generate_markdown_report(
        graph=graph,
        dp_stats=dp_stats,
        cycle=cycle,
        md_filename=md_filename,
        intervals_png=intervals_png,
        cycle_png=cycle_png,
    )

    print("Готово. Сгенерированы файлы:")
    print(f"  - {md_filename}")
    print(f"  - {intervals_png}")
    if cycle_png is not None:
        print(f"  - {cycle_png}")
    else:
        print("  - цикл не найден или не визуализирован.")
