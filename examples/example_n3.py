from hamilton_dp.intervals import TwoInterval, YVertex, TwoIntervalBipartiteGraph
from hamilton_dp.report import run_full_report


def main() -> None:
    """
    Classical small 2-interval bipartite graph (n=3) with a Hamiltonian cycle:

        X0 – Y0 – X1 – Y1 – X2 – Y2 – X0

    Interval structure:
        y0: I1 = [0,1]
        y1: I1 = [1,2]
        y2: I1 = [0,0], I2 = [2,2]
    """
    n = 3
    y_vertices = [
        YVertex(first=TwoInterval(0, 1), second=TwoInterval(None, None)),
        YVertex(first=TwoInterval(1, 2), second=TwoInterval(None, None)),
        YVertex(first=TwoInterval(0, 0), second=TwoInterval(2, 2)),
    ]
    g = TwoIntervalBipartiteGraph(n=n, y_vertices=y_vertices)

    run_full_report(g, prefix="example_report_true")


if __name__ == "__main__":
    main()
