import csv

with open("raw/raw_trace_alibaba.csv", newline='') as infile, \
     open("alibaba_trace.csv", "w", newline='') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["id", "submit_time", "cpu", "gpu", "duration"])

    for row in reader:
        try:
            task_id = row["instance_sn"]
            submit_time = float(row["creation_time"])
            scheduled_time = float(row["scheduled_time"])
            deletion_time = float(row["deletion_time"])
            cpu = float(row["cpu_request"])
            gpu = int(row["gpu_request"])
            duration = deletion_time - scheduled_time

            if duration > 300_000:
                continue
            writer.writerow([task_id, scheduled_time, cpu, gpu, duration])
        except Exception:
            continue  