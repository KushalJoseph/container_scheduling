from algorithms.base import ISchedulerAlgorithm
from core.task import Task
from core.cluster import Cluster
from core.node import Node
from typing import List, Optional

class RoundRobinScheduler(ISchedulerAlgorithm):
    def __init__(self, cluster: Cluster):
        super().__init__(cluster)
        self.nodes = self.cluster.get_all_nodes()
        self.current_index = 0  # Keeps track of where to start next

    def select_node(self, task: Task) -> Optional[str]:
        num_nodes = len(self.nodes)
        attempts = 0

        while attempts < num_nodes:
            node = self.nodes[self.current_index]
            self.current_index = (self.current_index + 1) % num_nodes
            attempts += 1

            if node.can_fit(task):
                return node.id

        return None