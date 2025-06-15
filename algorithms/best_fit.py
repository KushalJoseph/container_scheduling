from algorithms.base import ISchedulerAlgorithm
from core.task import Task

class BestFitScheduler(ISchedulerAlgorithm):
    def select_node(self, task: Task) -> str:
        """
        Selects the node where the remaining CPU+GPU after assignment is minimized,
        while still fitting the task.
        """
        best_node_id = None
        best_score = float('inf')

        for node in self.cluster.get_all_nodes():
            if not node.can_fit(task):
                continue
            # Calculate how "tight" the fit is
            cpu_remain = node.cpu_available - task.cpu
            gpu_remain = node.gpu_available - task.gpu
            score = cpu_remain + gpu_remain  # Lower is better

            if score < best_score:
                best_score = score
                best_node_id = node.id
                
        return best_node_id