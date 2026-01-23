from qbitUni import QuantumUniverse
from qbitUni.visuals import plot_histogram, print_bloch_vector
import math

def test_visuals():
    print("🎨 TESTING VISUALIZATION")
    
    # 1. Histogram Test [create a superposition on 3 qubits]
    n = 3
    u = QuantumUniverse(n)
    u.h(0)
    u.h(1) # Equal superposition on states 0, 1, 2, 3
    
    print("\n[1] Probability Distribution:")
    
    dim = 1 << n 
    
    # Get all probabilities
    probs = [u.get_prob(i) for i in range(dim)]
    
    # Draw the histogram
    plot_histogram(probs)
    
    # 2. Bloch Sphere Test
    # Let's rotate a qubit around the Y axis
    print("\n[2] Bloch Vector Tracking (Rotating |0> to |1>)...")
    
    # We will simulate a rotation in 5 steps: 0 -> 45 -> 90 -> 135 -> 180 degrees
    steps = 5
    for i in range(steps + 1):
        theta = (math.pi * i) / steps
        # State = cos(theta/2)|0> + sin(theta/2)|1>
        # This corresponds to a rotation around the Y-axis
        alpha = math.cos(theta/2)
        beta  = math.sin(theta/2)
        
        print(f"\n--- Angle: {math.degrees(theta):.0f}° ---")
        print_bloch_vector(alpha, beta)

if __name__ == "__main__":
    test_visuals()