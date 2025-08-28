import time
import numpy as np

#.pyd file 
import mc_engine_cpp # type: ignore

# --- Version 1: Pure Python/NumPy Implementation ---
def generate_single_path_python(S0, r, sigma, T, steps):
    dt = T / steps
    path = np.zeros(steps + 1)
    path[0] = S0
    for i in range(1, steps + 1):
        Z = np.random.standard_normal()
        path[i] = path[i-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    return path.tolist() # Return as a list to match C++ version

# --- Simulation Parameters ---
S0 = 100.0
r = 0.05
sigma = 0.2
T = 1.0
steps = 252
num_simulations = 100_000 

# --- Benchmark Python Version ---
print(f"Running {num_simulations:,} simulations in pure Python...")
start_time_py = time.time()
for _ in range(num_simulations):
    path_py = generate_single_path_python(S0, r, sigma, T, steps)
end_time_py = time.time()
python_duration = end_time_py - start_time_py
print(f"Python version took: {python_duration:.4f} seconds")

print("-" * 30)

# --- Benchmark C++ Version ---
print(f"Running {num_simulations:,} simulations in C++...")
start_time_cpp = time.time()
for _ in range(num_simulations):
    # Here we call the C++ function directly from Python
    path_cpp = mc_engine_cpp.generate_single_path(S0, r, sigma, T, steps)
end_time_cpp = time.time()
cpp_duration = end_time_cpp - start_time_cpp
print(f"C++ version took: {cpp_duration:.4f} seconds")

print("-" * 30)

# --- Calculate and Display the Speedup ---
speedup = python_duration / cpp_duration
print(f"C++ version is {speedup:.2f}x faster than the Python version.")