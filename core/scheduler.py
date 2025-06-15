from core.task import Task
from algorithms.base import ISchedulerAlgorithm

class Scheduler:
    def __init__(self, strategy: ISchedulerAlgorithm):
        self.strategy = strategy

    def schedule(self, task: Task, current_time: float) -> str:
        """
        Attempt to schedule a task using the chosen strategy.
        Returns the ID of the assigned node or raises an exception.
        """
        assigned_node_id = self.strategy.select_node(task)
        if assigned_node_id is None:
            raise RuntimeError(f"No suitable node found for Task {task.id}")

        node = self.strategy.cluster.get_node_by_id(assigned_node_id)
        node.assign_task(task, current_time)
        return assigned_node_id