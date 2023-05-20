from ganger import job_tracker, job_runner, job
import networkx as nx
import logging
import sys
from typing import Dict, Literal, Optional
from random import randrange
from time import time

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(module)s | %(message)s", stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
class TestJobRunner(job_runner.JobRunner):

    def __init__(self) -> None:
        self.submitted_jobs: Dict[str, float] = {}

    def submit_job(self, job_id: str, job: job.Job) -> Literal[job_runner.JobRunner.JobStatus.NotStarted]:
        self.submitted_jobs.setdefault(job_id, time() + 0.5 + (0.1 * float(randrange(-1, 1))))
        return job_runner.JobRunner.JobStatus.NotStarted

    def get_job_status(self, job_id: str) -> Optional[job_runner.JobRunner.JobStatus]:
        target_time: float | None = self.submitted_jobs.get(job_id)
        if target_time is None:
            return None
        
        if time() >= target_time:
            return job_runner.JobRunner.JobStatus.Succeeded
        return job_runner.JobRunner.JobStatus.Running

def test_basic_flow():
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

    test_tracker = job_tracker.JobTracker(TestJobRunner(), graph)
    test_tracker.run_minimal_build(target="Z", changed_projects=["B", "C"])
    assert True
