from enum import Enum, auto
from job import Job
from time import time
from typing import Dict, Optional, Literal
from abc import abstractmethod
from random import randrange

class JobRunner:

    class JobStatus(Enum):
        NotStarted = auto()
        Running = auto()
        Succeeded = auto()
        Error = auto()
    
    @abstractmethod
    def submit_job(self, job_id: str, job: Job) -> JobStatus:
        pass

    @abstractmethod
    def get_job_status(self, job_id: str) -> Optional[JobStatus]:
        pass

class TestJobRunner(JobRunner):

    def __init__(self) -> None:
        self.submitted_jobs: Dict[str, float] = {}

    def submit_job(self, job_id: str, job: Job) -> Literal[JobRunner.JobStatus.NotStarted]:
        self.submitted_jobs.setdefault(job_id, time() + 10.0 + float(randrange(-5, 5)))
        return JobRunner.JobStatus.NotStarted

    def get_job_status(self, job_id: str) -> Optional[JobRunner.JobStatus]:
        target_time: float | None = self.submitted_jobs.get(job_id)
        if target_time is None:
            return None
        
        if time() >= target_time:
            return JobRunner.JobStatus.Succeeded
        return JobRunner.JobStatus.Running

