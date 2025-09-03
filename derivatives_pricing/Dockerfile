# Stage 1: The Base Environment
# We start with a lightweight, official Python 3.12 image.
# Using a 'slim' version keeps our final container small.
FROM python:3.12-slim

# Install system-level dependencies.
# 'build-essential' is a meta-package that includes the g++ compiler, make, etc.
# This is the crucial step that provides our C++ environment inside the container.
RUN apt-get update && apt-get install -y build-essential

# Set the working directory inside the container. All subsequent commands
# will be run from this directory.
WORKDIR /app

# Copy and install Python requirements first.
# This is a Docker caching optimization. If requirements.txt doesn't change,
# Docker will reuse the cached layer, making subsequent builds much faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our application source code into the container.
COPY . .

# Stage 2: The Build
# Now that we have the compiler and the code, we compile the C++ module.
# This command runs *inside the Linux container* and creates the .so file.
RUN g++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` cpp_src/mc_engine.cpp -o mc_engine_cpp`python3-config --extension-suffix`

# Stage 3: The Execution
# Expose the port that Streamlit runs on.
EXPOSE 8501

# Define the command to run when the container starts.
# This will launch the Streamlit application.
CMD ["streamlit", "run", "interface.py"]