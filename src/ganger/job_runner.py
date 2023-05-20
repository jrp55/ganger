from enum import Enum, auto
from ganger.job import Job
from typing import Optional
from abc import abstractmethod

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