from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: str                       # Unique task ID
    submit_time: float            # When the task is submitted (in seconds or ms since epoch/zero)
    cpu: float                    # CPU units requested
    gpu: int                      # Number of GPUs requested
    duration: float               # Duration the task will run (in seconds)

    start_time: Optional[float] = None  # When the task actually starts
    end_time: Optional[float] = None    # When it ends
    assigned_node: Optional[str] = None # Node ID (if scheduled)

    def is_running(self, current_time: float) -> bool:
        """Check if task is currently running at the given simulation time."""
        return self.start_time is not None and self.start_time <= current_time < self.end_time

    def is_completed(self, current_time: float) -> bool:
        """Check if task has completed."""
        return self.end_time is not None and current_time >= self.end_time

    def __str__(self):
        return f"<Task {self.id}: CPU={self.cpu}, GPU={self.gpu}, Time={self.duration}s>"