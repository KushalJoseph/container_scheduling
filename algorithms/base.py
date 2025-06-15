from abc import ABC, abstractmethod
from core.task import Task
from core.cluster import Cluster

class ISchedulerAlgorithm(ABC):
    def __init__(self, cluster: Cluster):
        self.cluster = cluster

    @abstractmethod
    def select_node(self, task: Task) -> str:
        """Return the ID of a node that can host the task, or None if no fit found."""
        pass