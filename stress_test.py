#!/usr/bin/env python3
import subprocess
import time
import csv
import os
from datetime import datetime
import re

def run_command(command, duration=1800, log_interval=1):
    start_time = time.time()
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    results = []
    pattern = re.compile(r'T:\s*\d+\s*\(\s*\d+\)\s*P:\d+\s*I:\s*\d+\s*C:\s*\d+\s*Min:\s*(\d+)\s*Act:\s*\d+\s*Avg:\s*(\d+)\s*Max:\s*(\d+)')
    
    while time.time() - start_time < duration:
        output = process.stdout.readline()
        if output:
            match = pattern.search(output)
            if match:
                results.append({
                    'time': time.time() - start_time,
                    'min': int(match.group(1)),
                    'avg': int(match.group(2)),
                    'max': int(match.group(3))
                })
        if process.poll() is not None:
            break
        time.sleep(log_interval)
    
    process.terminate()
    return results

def log_to_csv(results, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['time', 'min', 'avg', 'max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def run_test(name, command, duration=1800):
    print(f"Running {name}...")
    results = run_command(command, duration)
    safe_name = name.lower().replace(' ', '_').replace('/', '_')
    csv_filename = os.path.join(results_dir, f"{safe_name}_results.csv")
    log_to_csv(results, csv_filename)
    print(f"{name} completed. Results saved to {csv_filename}")

# Ensure we're running as root
if os.geteuid() != 0:
    print("Please run as root")
    exit(1)

# Create results directory
results_dir = f"stress_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(results_dir)

# Run tests
run_test("Baseline Test", "cyclictest -l1800000 -p99 -m")
run_test("CPU Stress Test", "stress-ng --cpu $(nproc) --cpu-method all --timeout 1800 & cyclictest -l1800000 -p99 -t -a -m")
run_test("I/O Stress Test", "stress-ng --io $(nproc) --timeout 1800 & cyclictest -l1800000 -p99 -t -a -m")

# GPU Stress Test
gpu_burn_dir = "/home/jetson/jetson-gpu-burn"
gpu_burn_duration = 1800 # 30 minutes
run_test("GPU Stress Test", f"cd {gpu_burn_dir} && ./gpu_burn {gpu_burn_duration} & cyclictest -l1800000 -p99 -t -a -m")

# Full Stress Test
run_test("Full Stress Test", f"stress-ng --cpu $(nproc) --cpu-method all --io $(nproc) --timeout 1800 & (cd {gpu_burn_dir} && ./gpu_burn 1800) & cyclictest -l1800000 -p99 -t -a -m")

print(f"All tests completed. Results are in the directory: {results_dir}")
