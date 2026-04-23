#!/usr/bin/env python

import time
import torch
import torch_directml

DURATION = 5


def benchmark_nothing(duration=DURATION):
    a, b = 3, 5
    start_time = time.time()
    end_time = start_time + duration

    operations = 0
    while time.time() < end_time:
        c = a * b
        operations += 1

    return operations


def benchmark_device(device, duration=10):
    """benchmark on a given device for a specified duration"""
    tensor_size = (1024, 1024)

    # Create random tensors
    a = torch.randn(tensor_size, device=device)
    b = torch.randn(tensor_size, device=device)

    start_time = time.time()
    end_time = start_time + duration

    operations = 0
    # Perform matrix multiplication to stress the device
    while time.time() < end_time:
        c = torch.matmul(a, b)
        operations += 1

    return operations


# Baseline
no_operations = benchmark_nothing()
print(f"NOOPs: {no_operations} in {DURATION} seconds.")

# Benchmark on CPU
cpu_device = torch.device("cpu")
cpu_operations = benchmark_device(cpu_device, duration=DURATION)
print(f"CPU: {cpu_operations} matrix multiplications in {DURATION} seconds.")

# Check if DirectML is available and benchmark on DirectML device
if torch_directml.is_available():
    dml_device = torch_directml.device()
    dml_operations = benchmark_device(dml_device, duration=DURATION)
    print(f"DirectML: {dml_operations} matrix multiplications in {DURATION} seconds.")
    print(
        f"pseudo-speedup (limited by Python loop): {dml_operations / cpu_operations:.3}x"
    )
else:
    print("DirectML is not available.")
