import os
import csv
from typing import List, Dict
from core.task import Task
from core.cluster import Cluster
from statistics import median;

class MetricsCollector:
    def __init__(self, total_tasks: int, algo: str):
        self.completed_tasks: List[Task] = []
        self.cpu_usage_timeline: List[float] = []
        self.gpu_usage_timeline: List[float] = []
        self.time_ticks: List[float] = []
        self.logs_dir = f"logs/{algo}"
        self.total_tasks = total_tasks

        os.makedirs(self.logs_dir, exist_ok=True)

    def save_all_logs(self):
        self._save_summary_log()
        self._save_task_log()
        self._save_utilization_logs()

    def _save_summary_log(self):
        summary = self.summary()
        with open(f"{self.logs_dir}/summary.log", "w") as f:
            f.write("📊 Scheduler Metrics Summary\n")
            for k, v in summary.items():
                f.write(f"{k}: {v:.2f}\n")

    def _save_task_log(self):
        with open(f"{self.logs_dir}/task_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "submit_time", "cpu", "gpu", "duration", "assigned_node", "start_time", "end_time", "wait_time", "turnaround_time"])
            for t in self.completed_tasks:
                wait = t.start_time - t.submit_time
                turnaround = t.end_time - t.submit_time
                writer.writerow([
                    t.id, t.submit_time, t.cpu, t.gpu, t.duration,
                    t.assigned_node, t.start_time, t.end_time, wait, turnaround
                ])

    def _save_utilization_logs(self):
        with open(f"{self.logs_dir}/cpu_utilization.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "cpu_utilization"])
            for t, val in zip(self.time_ticks, self.cpu_usage_timeline):
                writer.writerow([t, val])

        with open(f"{self.logs_dir}/gpu_utilization.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "gpu_utilization"])
            for t, val in zip(self.time_ticks, self.gpu_usage_timeline):
                writer.writerow([t, val])

    def record_tick(self, cluster: Cluster, current_time: float):
        total_cpu = sum(node.cpu_capacity for node in cluster.get_all_nodes())
        used_cpu = sum(node.cpu_capacity - node.cpu_available for node in cluster.get_all_nodes())
        cpu_util = used_cpu / total_cpu if total_cpu else 0.0

        total_gpu = sum(node.gpu_capacity for node in cluster.get_all_nodes())
        used_gpu = sum(node.gpu_capacity - node.gpu_available for node in cluster.get_all_nodes())
        gpu_util = used_gpu / total_gpu if total_gpu else 0.0

        self.cpu_usage_timeline.append(cpu_util)
        self.gpu_usage_timeline.append(gpu_util)
        self.time_ticks.append(current_time)

    def record_task_completion(self, task: Task):
        self.completed_tasks.append(task)
        compl = len(self.completed_tasks)
        if compl % 100 == 0 or compl == self.total_tasks:
            print(f"Completed {compl}/{self.total_tasks} tasks")

    def summary(self) -> Dict[str, float]:
        if not self.completed_tasks:
            return {}

        wait_times = [t.start_time - t.submit_time for t in self.completed_tasks]
        turnaround_times = [t.end_time - t.submit_time for t in self.completed_tasks]

        avg_wait = sum(wait_times) / len(wait_times)
        median_wait = median(wait_times)
        avg_turnaround = sum(turnaround_times) / len(turnaround_times)
        max_wait = max(wait_times)

        success_rate = len(self.completed_tasks)

        avg_cpu_util = sum(self.cpu_usage_timeline) / len(self.cpu_usage_timeline)
        avg_gpu_util = sum(self.gpu_usage_timeline) / len(self.gpu_usage_timeline)

        return {
            "avg_wait_time_ms": avg_wait,
            "median_wait_time_ms": median_wait,
            "avg_turnaround_time_ms": avg_turnaround,
            "max_wait_time_ms": max_wait,
            "tasks_completed": success_rate,
            "avg_cpu_utilization": avg_cpu_util,
            "avg_gpu_utilization": avg_gpu_util
        }

    def print_summary(self):
        print("\nMetrics Summary:")
        summary = self.summary()
        for k, v in summary.items():
            print(f"  - {k}: {v:.2f}")