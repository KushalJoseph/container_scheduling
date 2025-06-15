from algorithms.base import ISchedulerAlgorithm
from core.task import Task

class BinPackingScheduler(ISchedulerAlgorithm):
    def select_node(self, task: Task) -> str:
        # Sort nodes by how full they are (descending) to pack tightly
        sorted_nodes = sorted(
            self.cluster.nodes,
            key=lambda node: (node.cpu_capacity - node.cpu_available) + 
                             (node.gpu_capacity - node.gpu_available),
            reverse=True
        )

        for node in sorted_nodes:
            if node.can_fit(task):
                return node.id

        return None