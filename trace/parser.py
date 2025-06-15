import csv
from typing import List
from core.task import Task

def load_trace(path: str) -> List[Task]:
    """
    Parses a trace CSV file with columns: submit_time, cpu, gpu, duration
    """
    tasks = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task = Task(
                id=str(row["id"]),
                submit_time=float(row["submit_time"]),
                cpu=float(row["cpu"]),
                gpu=int(row["gpu"]),
                duration=float(row["duration"])
            )
            tasks.append(task)
    return tasks