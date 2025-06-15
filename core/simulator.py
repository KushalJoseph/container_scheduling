from typing import List
from core.task import Task
from core.cluster import Cluster
from core.scheduler import Scheduler
from core.metrics import MetricsCollector

class Simulator:
    def __init__(self, cluster: Cluster, scheduler: Scheduler, tasks: List[Task], config: dict):
        self.cluster = cluster
        self.scheduler = scheduler
        self.all_tasks = sorted(tasks, key=lambda t: t.submit_time)
        self.pending_tasks: List[Task] = []
        self.current_time = 0.0
        self.task_index = 0
        self.metrics = MetricsCollector(len(self.all_tasks), config["algorithm"])
        self.verbose = config["verbose"]

    def log(self, string: str):
        if self.verbose:
            print(string)

    def run(self):
        while (
            self.task_index < len(self.all_tasks) or                    # if there are still tasks to process
            self.pending_tasks or                                       # if there are still pending tasks
            any(n.running_tasks for n in self.cluster.get_all_nodes())  # if there are still running tasks
        ):
            self.log('----------------------------------------------------------------')
            # print(f"Current simulated time: {self.current_time:.0f} ms")
            self.log("\nCluster state before scheduling:")
            self.cluster.report(self.verbose); self.log('\n')

            # Release completed tasks
            self.cluster.release_resources(self.current_time)
            self.metrics.record_tick(self.cluster, self.current_time)

            # Add newly arrived tasks to pending queue
            while self.task_index < len(self.all_tasks) and self.all_tasks[self.task_index].submit_time <= self.current_time:
                self.log(f"New task arrived: {self.all_tasks[self.task_index].id} (CPU={self.all_tasks[self.task_index].cpu}, GPU={self.all_tasks[self.task_index].gpu}, Duration={self.all_tasks[self.task_index].duration} ms)")
                self.pending_tasks.append(self.all_tasks[self.task_index])
                self.task_index += 1

            # Attempt to schedule all pending tasks
            still_pending = []
            for task in self.pending_tasks:
                try:
                    assigned_node = self.scheduler.schedule(task, self.current_time)
                    self.log(f"✅ Task {task.id} has been assigned to Node {assigned_node}.")
                    self.metrics.record_task_completion(task)
                except RuntimeError:
                    # Task could not be scheduled now; keep it for later
                    self.log(f"❌ Task {task.id} could not be scheduled now; keeping it for later.")
                    still_pending.append(task)
            self.pending_tasks = still_pending

            self.log("\nCluster state after scheduling:")
            self.cluster.report(self.verbose)

            if(self.verbose): input("\nPress Enter to advance to the next simulated time...\n")
            self._advance_time()

        self.log("\nAll tasks processed. Simulation complete\n")
        self.metrics.print_summary()
        self.metrics.save_all_logs()

    def _advance_time(self):
        """Advance to the next interesting event (next arrival or completion)."""
        next_times = []

        if self.task_index < len(self.all_tasks):
            next_times.append(self.all_tasks[self.task_index].submit_time)

        for node in self.cluster.get_all_nodes():
            for task in node.running_tasks:
                if task.end_time and task.end_time > self.current_time:
                    next_times.append(task.end_time)

        if next_times:
            self.current_time = min(next_times)
        else:
            self.current_time += 10000.0