from qbitUni import QuantumUniverse
from qbitUni.visuals import plot_histogram

from scipy.optimize import minimize
import math

def vqe_ansatz(theta, u):
    """Creates a trial wavefunction based on angle theta"""
    u.h(0)
    u.rx(0, theta)
    
    plot_histogram([u.measure_qubit(i) for i in range(0)])
    plot_histogram([u.measure_qubit(i) for i in range(8)])

def cost_function(theta):
    """Returns the energy <Z> for a given angle"""
    u = QuantumUniverse(8)
    
    # 1. Fake Rx gate (Hadamard sandwich) -[{ $$R_x(\theta) \approx H \cdot Phase(\theta) \cdot H$$ }]-
    u.h(0) 
    u.phase(0, theta[0]) # Using Phase as a tunable parameter
    u.h(0)
    
    # 2. Measure Energy (Expectation of Hamiltonian)
    # E = <Z>
    energy = u.get_expectation(0)
    
    # Clean up (Optional if you rely on Python GC)
    return energy

def run_vqe():
    print("🧪 Running VQE Simulation...")
    # Start with a random guess (e.g., 3.0 radians)
    initial_guess = [3.0]
    
    # Classical Optimizer drives the Quantum Engine
    result = minimize(cost_function, initial_guess, method='COBYLA', tol=1e-4)
    
    print("\n✅ Optimization Complete!")
    print(f"   Ground State Energy: {result.fun:.4f} (Should be near -1.0)")
    print(f"   Optimal Angle:       {result.x[0]:.4f} rads")
    print(f"   -- Note: {math.pi:.4f} rads is PI --")

if __name__ == "__main__":
    u = QuantumUniverse(8)
    theta = 3.0

    vqe_ansatz(theta, u)
    run_vqe()