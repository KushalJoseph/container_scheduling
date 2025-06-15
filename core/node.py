from typing import List
from core.task import Task

class Node:
    def __init__(self, id: str, cpu_capacity: float, gpu_capacity: int, verbose: bool=False):
        self.id = id
        self.cpu_capacity = cpu_capacity
        self.gpu_capacity = gpu_capacity
        self.cpu_available = cpu_capacity
        self.gpu_available = gpu_capacity
        self.running_tasks: List[Task] = []
        self.verbose = verbose

    def log(self, string: str):
        if self.verbose:
            print(string)

    def can_fit(self, task: Task) -> bool:
        """Check if the node can fit the task's CPU and GPU requirements."""
        return task.cpu <= self.cpu_available and task.gpu <= self.gpu_available

    def assign_task(self, task: Task, current_time: float):
        """Assign a task to this node and update resource availability."""
        if not self.can_fit(task):
            raise ValueError(f"Node {self.id} cannot accommodate Task {task.id}")
        
        self.cpu_available -= task.cpu
        self.gpu_available -= task.gpu
        task.start_time = current_time
        task.end_time = current_time + task.duration
        task.assigned_node = self.id
        self.running_tasks.append(task)

    def release_completed_tasks(self, current_time: float):
        """Release resources of tasks that have completed."""
        still_running = []
        for task in self.running_tasks:
            if task.is_completed(current_time):
                self.cpu_available += task.cpu
                self.gpu_available += task.gpu
                self.log(f"Task {task.id} completed on Node {self.id} by {current_time:.1f}s")
            else:
                still_running.append(task)
                self.log(f"Task {task.id} still running on Node {self.id} by {current_time:.1f}s")
        self.running_tasks = still_running

    def __str__(self):
        return f"<Node {self.id}: CPU {self.cpu_available}/{self.cpu_capacity}, GPU {self.gpu_available}/{self.gpu_capacity}>"