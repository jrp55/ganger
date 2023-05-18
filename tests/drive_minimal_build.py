from job import Job
from job_tracker import JobTracker
from job_runner import TestJobRunner
import networkx as nx
import logging
import sys

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(module)s | %(message)s", stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    graph = nx.digraph.DiGraph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "E")
    graph.add_edge("E", "D")
    graph.add_edge("B", "G")
    graph.add_edge("G", "D")
    graph.add_edge("B", "H")
    graph.add_edge("H", "D")
    graph.add_edge("C", "H")
    graph.add_edge("F", "C")
    graph.add_edge("C", "D")
    graph.add_edge("C", "Z")
    graph.add_edge("D", "Z")

    job_tracker = JobTracker(TestJobRunner(), graph)
    job_tracker.run_minimal_build(target="Z", changed_projects=["B", "C"])


if __name__ == "__main__":
    main()