import pandas as pd
import matplotlib.pyplot as plt
import yaml
import os

def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
# Load data
config = load_config('config.yaml')
algorithm = config["algorithm"]
logs_dir = f"logs/{algorithm}"
os.makedirs(f"{logs_dir}/plots", exist_ok=True)

cpu_df = pd.read_csv(f"{logs_dir}/cpu_utilization.csv")
gpu_df = pd.read_csv(f"{logs_dir}/gpu_utilization.csv")

# Plot CPU utilization
plt.figure(figsize=(10, 4))
plt.plot(cpu_df["time"], cpu_df["cpu_utilization"], label="CPU Utilization", color="blue")
plt.title("CPU Utilization Over Time")
plt.xlabel("Time (ms)")
plt.ylabel("CPU Utilization")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{logs_dir}/plots/cpu_utilization_plot.png")
plt.show()

# Plot GPU utilization
plt.figure(figsize=(10, 4))
plt.plot(gpu_df["time"], gpu_df["gpu_utilization"], label="GPU Utilization", color="green")
plt.title("GPU Utilization Over Time")
plt.xlabel("Time (ms)")
plt.ylabel("GPU Utilization")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{logs_dir}/plots/gpu_utilization_plot.png")
plt.show()