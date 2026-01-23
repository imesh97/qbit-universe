from qbitUni import QuantumUniverse
from qbitUni.visuals import plot_histogram

from scipy.optimize import minimize
import math

def vqe_ansatz(u, theta):
    """Creates a trial wavefunction based on angle theta via Rx gate"""
    u.rx(0, theta)
    
def cost_function(theta_list):
    """Returns the energy <Z> for a given angle"""
    u = QuantumUniverse(1)
    
    val = theta_list[0] # Extract float from list
    vqe_ansatz(u, val)
    
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
    optimal_theta = result.x[0]

    print("\n✅ Optimization Complete!")
    print(f"   Ground State Energy: {result.fun:.4f} (Should be near -1.0)")
    print(f"   Optimal Angle:       {optimal_theta:.4f} rads")
    print(f"   -- Note: {math.pi:.4f} rads is PI --")

    # Visualize the Final Result
    print("\n📊 Visualizing Resulting State...")
    u_final = QuantumUniverse(1)
    vqe_ansatz(u_final, optimal_theta)
    
    # Get PROBABILITIES (non-destructive) instead of measuring
    probs = [u_final.get_prob(0), u_final.get_prob(1)]
    plot_histogram(probs)

if __name__ == "__main__":
    run_vqe()