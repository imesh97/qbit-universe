def plot_histogram(counts, total_shots=None, width=50):
    """
    Draws a text-based histogram of measurement results.
    counts: dict {state_index: count} or list of probabilities
    """
    print("\n📊 QUANTUM HISTOGRAM")
    print("─" * (width + 15))
    
    # Handle Input: Normalize list or dict to probability 0.0-1.0
    if isinstance(counts, dict):
        if total_shots is None:
            total_shots = sum(counts.values())
        data = {k: v/total_shots for k, v in counts.items()}
    elif isinstance(counts, list):
        data = {i: prob for i, prob in enumerate(counts) if prob > 0.001}
    else:
        print("❌ Error: plot_histogram expects a list of probabilities or a dict of counts.")
        return

    # Sort keys to print in order |00>, |01>...
    sorted_keys = sorted(data.keys())
    
    # Calculate how many bits we need for the label (e.g. 3 qubits = 000)
    if sorted_keys:
        max_idx = max(k for k in sorted_keys if isinstance(k, int))
        n_qubits = max(1, (max_idx).bit_length())
    else:
        n_qubits = 1

    for state in sorted_keys:
        prob = data[state]
        bar_len = int(prob * width)
        
        # Create Binary Label (e.g., |011>)
        if isinstance(state, int):
            label_bin = format(state, f'0{n_qubits}b')
            label = f"|{label_bin}>"
        else:
            label = str(state)
            
        # Draw Bar
        bar = "█" * bar_len
        # Add a half-block for extra precision if needed
        if (prob * width) - bar_len > 0.5:
            bar += "▌"
            
        print(f"{label} : {bar} {prob:.1%}")
        
    print("─" * (width + 15))

def _get_bar(val, width=20):
    """Helper: Draws a horizontal bar from -1 to +1 (Used for Bloch Sphere)"""
    # Map value -1.0..+1.0 to index 0..20
    center = width // 2
    idx = int((val + 1) / 2 * width)
    idx = max(0, min(width, idx))
    
    chars = [" "] * (width + 1)
    chars[center] = "|" # Center line
    
    # Fill based on whether we are positive or negative relative to center
    if idx > center:
        for i in range(center + 1, idx + 1):
            chars[i] = "▓"
    elif idx < center:
        for i in range(idx, center):
            chars[i] = "▓"
        
    return f"[{''.join(chars)}]"

def print_bloch_vector(alpha, beta):
    """
    Calculates and prints the X, Y, Z coordinates of a qubit state.
    State = alpha|0> + beta|1>
    """
    # Calculate Expectation Values (Pauli X, Y, Z)
    # <X> = 2*Real(a*b)
    # <Y> = 2*Imag(a*b)
    # <Z> = |a|^2 - |b|^2
    x = 2 * (alpha.conjugate() * beta).real
    y = 2 * (alpha.conjugate() * beta).imag
    z = (abs(alpha)**2 - abs(beta)**2)
    
    print("🌐 BLOCH SPHERE")
    print(f"   x: {x:+.4f} ", _get_bar(x))
    print(f"   y: {y:+.4f} ", _get_bar(y))
    print(f"   z: {z:+.4f} ", _get_bar(z))