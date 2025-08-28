#include <vector>
#include <iostream>
#include <cmath>
#include <random>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // Needed to automatically convert std::vector <-> Python list

namespace py = pybind11;

// core finction
std::vector<double> generate_single_path(double S0, double r, double sigma, double T, int steps){

    // time step
    double dt = T / steps;

    // vector store
    std::vector<double> path;
    path.push_back(S0);
    
    // random number generator for standard normal distribution
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<> d(0.0,1.0); // produces random numbers with mean = 0 and standard deviation 1

    // The main simulation loop
    for (int i = 1; i <= steps; ++i) {
        // Generate a random number Z from the standard normal distribution
        double Z = d(gen);

        // Get the previous price from the path
        double St_minus_1 = path.back();

        // Apply the GBM formula to get the next price
        double St = St_minus_1 * exp((r - 0.5 * sigma * sigma) * dt + sigma * sqrt(dt) * Z);

        // Add the new price to our path
        path.push_back(St);
    }

    return path;
}

// pybind 11 wrapper

PYBIND11_MODULE(mc_engine_cpp, m) {
    m.doc() = "High-performance Monte Carlo path generation engine written in C++"; // Optional module docstring

    m.def("generate_single_path", &generate_single_path, "A function that generates a single stock price path using GBM",
          py::arg("S0"), py::arg("r"), py::arg("sigma"), py::arg("T"), py::arg("steps"));
}