import networkx as nx
from ganger.job import Job
from ganger.job_runner import JobRunner
from typing import List, Dict
from itertools import tee
from time import sleep
from alive_progress import alive_bar
from enum import Enum, auto
from logging import getLogger, Logger

logger: Logger = getLogger(__name__)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

class JobStatus(Enum):
    NotSubmitted = auto()
    NotStarted = auto()
    Running = auto()
    Succeeded = auto()
    Error = auto()

def transform_job_runner_status(status: JobRunner.JobStatus | None) -> JobStatus:
    if status is None:
        raise RuntimeError("Unexpected None status")
    return {
        JobRunner.JobStatus.NotStarted: JobStatus.NotStarted,
        JobRunner.JobStatus.Error: JobStatus.Error,
        JobRunner.JobStatus.Running: JobStatus.Running,
        JobRunner.JobStatus.Succeeded: JobStatus.Succeeded
    }[status]

class JobTracker:

    def __init__(self, job_runner: JobRunner, job_graph: nx.digraph.DiGraph) -> None:
        self.job_runner: JobRunner = job_runner
        self.job_graph: nx.digraph.DiGraph = job_graph

    def run_minimal_build(self, target: str, changed_projects: List[str]) -> None:
        minimal_build_graph = nx.digraph.DiGraph()

        for changed_project in changed_projects:
            for path in nx.simple_paths.all_simple_paths(self.job_graph, changed_project, target):
                for pair in pairwise(path):
                    minimal_build_graph.add_edge(pair[0], pair[1])

        sorted_jobs = list(nx.algorithms.dag.lexicographical_topological_sort(minimal_build_graph))
        logger.info(f"Sorted job plan is {' '.join(sorted_jobs)}")
        job_statuses: Dict[str, JobStatus] = {k: JobStatus.NotSubmitted for k in sorted_jobs}
        finished = False
        with alive_bar(len(sorted_jobs)) as bar:
            while not finished:
                for job in sorted_jobs:
                    if job_statuses[job] is JobStatus.NotSubmitted:
                        # Job not submitted yet
                        waiting_on_jobs = nx.algorithms.dag.ancestors(minimal_build_graph, job)
                        unfinshed_ancestors: List[str] = [waitfor for waitfor in waiting_on_jobs if job_statuses[waitfor]!=JobStatus.Succeeded]
                        if len(unfinshed_ancestors) > 0:
                            pass
                        else:
                            job_statuses[job] = transform_job_runner_status(self.job_runner.submit_job(job, Job(job)))

                    elif job_statuses[job] in [JobStatus.Running, JobStatus.NotStarted]:
                        job_status: JobStatus = transform_job_runner_status(self.job_runner.get_job_status(job))
                        if job_status == JobStatus.Running:
                            pass
                        elif job_status == JobStatus.Succeeded:
                            logger.info(f"{job} finished")
                            bar()
                        elif job_status == JobStatus.Error:
                            msg = f"{job} failed"
                            logger.error(msg)
                            raise RuntimeError(msg)
                        else:
                            msg = "what"
                            logger.error(msg)
                            raise AssertionError(msg)
                        job_statuses[job] = job_status
                    
                    elif job_statuses[job] == JobStatus.Succeeded:
                        pass
                
                finished = job_statuses[target] == JobStatus.Succeeded
                if not finished:
                    bar.text(f"Running {', '.join([k for k,v in job_statuses.items() if v in [JobStatus.Running, JobStatus.NotStarted]])}")
                    sleep(1)