from core.cluster import Cluster
from core.scheduler import Scheduler
from core.simulator import Simulator
from core.task import Task
import yaml
from algorithms.best_fit import BestFitScheduler
from algorithms.round_robin import RoundRobinScheduler
from algorithms.bin_packing import BinPackingScheduler
from trace.parser import load_trace
import matplotlib.pyplot as plt
from typing import List
import os

def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_algorithm(name: str, cluster):
    name = name.lower()
    if name == "best_fit":
        return BestFitScheduler(cluster)
    elif name == "round_robin":
        return RoundRobinScheduler(cluster)
    elif name == "bin_packing":
        return BinPackingScheduler(cluster)
    else:
        raise ValueError(f"Unknown algorithm: {name}")

def plots(tasks: List[Task]):
    durations = [t.duration for t in tasks]
    plt.hist(durations, bins=30)
    plt.title("Task Duration Distribution")
    plt.xlabel("Duration (ms)")
    plt.ylabel("Count")
    plt.show()

    cpu = [t.cpu for t in tasks]
    plt.hist(cpu, bins=20)
    plt.title("vCPU request distribution")
    plt.xlabel("vCPU")
    plt.ylabel("Count of Requests")
    plt.show()

def main():
    config = load_config("config.yaml")
    print(config)

    cluster = Cluster(config["cluster"])

    algorithm = get_algorithm(config["algorithm"], cluster)
    scheduler = Scheduler(strategy=algorithm)

    tasks = load_trace(config["trace_file"])
    # plots(tasks)
    
    input("Press any key to begin the simulation")
    sim = Simulator(cluster, scheduler, tasks, config)
    sim.run()

    os.system("python3 logs/plot_logs.py")

if __name__ == "__main__":
    main()