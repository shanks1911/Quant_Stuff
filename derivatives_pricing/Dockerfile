# Stage 1: The Base Environment
# Start with a standard Python 3.12 slim image. This is our Linux OS.
FROM python:3.12-slim

# Install system-level dependencies.
# 'build-essential' includes the g++ compiler needed to build our C++ module.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Set the working directory inside the container.
WORKDIR /app

# Copy and install Python requirements. This is done first to leverage Docker's caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code.
COPY . .

# Stage 2: The Build
# Compile the C++ module *inside the Linux container*.
RUN g++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` cpp_src/mc_engine.cpp -o mc_engine_cpp`python3-config --extension-suffix`

# Stage 3: The Execution
# Expose the port Streamlit uses.
EXPOSE 8501

# The command to run when the container starts.
CMD ["streamlit", "run", "interface.py", "--server.port=8501", "--server.address=0.0.0.0"]