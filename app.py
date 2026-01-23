import streamlit as st
import pandas as pd

import math
import cmath
import matplotlib.pyplot as plt


from qbitUni import QuantumUniverse

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="qbitUni Studio", 
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR POPS OF COLOR ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
        text-align: center;
    }
    h1 { color: #5dade2; }
    h2, h3 { color: #2e86c1; }
</style>
""", unsafe_allow_html=True)

st.title("⚛️ qbitUni Studio")
st.caption("Quantum Universe Simulator (Qbit's C-Engine)")

# --- SESSION STATE ---
if "circuit" not in st.session_state:
    st.session_state.circuit = []
if "qubits" not in st.session_state:
    st.session_state.qubits = 3

# --- SIDEBAR: CONTROLS ---
with st.sidebar:
    st.header("🎛️ Circuit Builder")
    
    # Qubit Count
    new_n = st.number_input("System Size (Qubits)", min_value=1, max_value=12, value=st.session_state.qubits)
    if new_n != st.session_state.qubits:
        st.session_state.qubits = new_n
        st.session_state.circuit = []
        st.rerun()
    
    st.markdown("---")
    
    # Gate Selection
    st.subheader("Add Operation")
    
    # Group gates logically
    gate_category = st.radio("Category", ["Single Qubit", "Multi Qubit", "Parametric"], horizontal=True)
    
    op = {}
    
    if gate_category == "Single Qubit":
        gate_type = st.selectbox("Gate", ["H (Hadamard)", "X (NOT)", "Z (Phase Flip)", "Y (Bit+Phase)", "S (Phase 90°)", "T (Phase 45°)"])
        op['target'] = st.number_input("Target Qubit", 0, new_n-1, 0)
        
    elif gate_category == "Multi Qubit":
        gate_type = st.selectbox("Gate", ["CNOT (Entangle)", "CZ (Controlled-Phase)", "SWAP", "Toffoli (CCNOT)"])
        
        if gate_type == "Toffoli (CCNOT)":
            op['c1'] = st.number_input("Control 1", 0, new_n-1, 0)
            op['c2'] = st.number_input("Control 2", 0, new_n-1, 1)
            op['target'] = st.number_input("Target", 0, new_n-1, 2)
        else:
            op['control'] = st.number_input("Control", 0, new_n-1, 0)
            op['target'] = st.number_input("Target", 0, new_n-1, min(1, new_n-1))
            
    elif gate_category == "Parametric":
        gate_type = st.selectbox("Gate", ["RX (Rotate X)", "Phase (Rotate Z)"])
        op['target'] = st.number_input("Target Qubit", 0, new_n-1, 0)
        angle_deg = st.slider("Angle (Degrees)", -360.0, 360.0, 90.0, step=15.0)
        op['angle'] = math.radians(angle_deg)

    op['gate'] = gate_type

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add Gate", type="primary", use_container_width=True):
            st.session_state.circuit.append(op)
            st.rerun()
    with col2:
        if st.button("Undo Last", use_container_width=True):
            if st.session_state.circuit:
                st.session_state.circuit.pop()
                st.rerun()

    st.markdown("---")
    if st.button("🗑️ Reset All", use_container_width=True):
        st.session_state.circuit = []
        st.rerun()

# --- SIMULATION ENGINE ---
# Instantiate fresh C-Universe
u = QuantumUniverse(st.session_state.qubits)
dim = 1 << st.session_state.qubits

# Replay History
hist_str = []
for op in st.session_state.circuit:
    g = op['gate']
    # Mapping
    if "H" in g: u.h(op['target'])
    elif "X" in g: u.x(op['target'])
    elif "Y" in g: u.y(op['target'])
    elif "Z" in g: u.z(op['target'])
    elif "S" in g: u.s(op['target'])
    elif "T" in g: u.t(op['target'])
    elif "CNOT" in g: u.cnot(op['control'], op['target'])
    elif "CZ" in g: u.cz(op['control'], op['target'])
    elif "SWAP" in g: u.swap(op['control'], op['target'])
    elif "Toffoli" in g: u.toffoli(op['c1'], op['c2'], op['target'])
    elif "RX" in g: u.rx(op['target'], op['angle'])
    elif "Phase" in g: u.phase(op['target'], op['angle'])
    
    # String building
    short_name = g.split(' ')[0]
    if 'angle' in op:
        deg = math.degrees(op['angle'])
        hist_str.append(f"**{short_name}**({deg:.0f}° on q{op['target']})")
    elif 'c1' in op:
        hist_str.append(f"**{short_name}**({op['c1']},{op['c2']}→{op['target']})")
    elif 'control' in op:
        hist_str.append(f"**{short_name}**({op['control']}→{op['target']})")
    else:
        hist_str.append(f"**{short_name}**({op['target']})")

# --- UI: MAIN DASHBOARD ---

# 1. Circuit View
st.info(f"**Circuit Pipeline:** {' → '.join(hist_str) if hist_str else 'Start adding gates...'}")

# 2. Main Visuals Area (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Probabilities", "🌐 Bloch Spheres", "🧠 State Math", "📜 Python Code"])

# --- TAB 1: PROBABILITIES (The Standard View) ---
with tab1:
    col_chart, col_exp = st.columns([2, 1])
    
    with col_chart:
        st.subheader("Measurement Outcomes")
        # Get Data
        probs = [u.get_prob(i) for i in range(dim)]
        labels = [f"|{format(i, f'0{st.session_state.qubits}b')}⟩" for i in range(dim)]
        
        # Filter sparse
        clean_data = [{"State": l, "Probability": p} for l, p in zip(labels, probs) if p > 0.0001]
        df_probs = pd.DataFrame(clean_data)
        
        if not df_probs.empty:
            st.bar_chart(df_probs, x="State", y="Probability", color="#2e86c1", use_container_width=True)
        else:
            st.warning("State vector has vanished (Prob=0). Check logic.")

    with col_exp:
        st.subheader("Energy Levels <Z>")
        st.caption("1.0 = Ground |0⟩, -1.0 = Excited |1⟩")
        
        for i in range(st.session_state.qubits):
            z_val = u.get_expectation(i)
            
            # Dynamic Color Logic
            delta_color = "normal"
            if z_val > 0.9: delta_color = "off"   # Gray/Normal
            elif z_val < -0.9: delta_color = "inverse" # Red/Inverse
            
            st.metric(f"Qubit {i}", f"{z_val:.3f}")

# --- TAB 2: BLOCH SPHERES (The Physics View) ---
with tab2:
    st.subheader("Single Qubit Projections")
    st.caption("Visualizing the state of each qubit individually (averaging out entanglement).")
    
    # We can't do true 3D Bloch spheres easily in Streamlit without heavy libs,
    # but we can show the X, Y, Z components!
    
    b_cols = st.columns(st.session_state.qubits)
    
    for i in range(st.session_state.qubits):
        with b_cols[i]:
            st.markdown(f"#### Qubit {i}")
            
            # Since we don't have get_expectation('x') yet, let's just use <Z> for now
            # To do X and Y, you would need to add u.get_expectation_x(i) in C!
            # For now, let's fake the visualization slightly using Z
            
            z = u.get_expectation(i)
            # Create a simple matplotlib gauge
            fig, ax = plt.subplots(figsize=(2, 2))
            circle = plt.Circle((0, 0), 1, color='lightgray', fill=False, linewidth=2)
            ax.add_artist(circle)
            
            # Arrow pointing based on Z (Up/Down)
            # We assume X=0 for drawing since we lack data, but Z is accurate.
            # Purely visual approximation for Z-axis
            ax.arrow(0, 0, 0, z*0.9, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
            
            ax.set_xlim(-1.1, 1.1)
            ax.set_ylim(-1.1, 1.1)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.text(-0.2, 1.2, "|0⟩", fontsize=8)
            ax.text(-0.2, -1.3, "|1⟩", fontsize=8)
            
            st.pyplot(fig)
            st.metric("Z-Component", f"{z:.2f}")

# --- TAB 3: STATE MATH (The Explainer) ---
with tab3:
    st.subheader("Complex Amplitudes")
    st.caption("The exact complex numbers stored in the C-Engine RAM.")
    
    # Prepare Data Table
    rows = []
    for i in range(dim):
        amp = u.get_amplitude(i)
        if abs(amp) > 0.001:
            # Polar Form
            r, phi = cmath.polar(amp)
            deg = math.degrees(phi)
            
            rows.append({
                "Basis State": f"|{format(i, f'0{st.session_state.qubits}b')}⟩",
                "Amplitude (Rect)": f"{amp.real:.3f} {'+' if amp.imag >=0 else '-'} {abs(amp.imag):.3f}j",
                "Magnitude": f"{r:.3f}",
                "Phase (Deg)": f"{deg:.1f}°",
                "Probability": f"{r**2:.1%}"
            })
    
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    
    st.divider()
    
    # --- MATH EXPLAINER ---
    with st.expander("📚 Explain the Math: What is happening here?"):
        st.markdown("""
        ### 1. Superposition
        If you see multiple rows in the table above, the universe is in a **Superposition**.
        Instead of being just `|00...0>`, it exists in several states at once, weighted by complex numbers (Amplitudes).
        
        ### 2. Probability
        Nature doesn't let us see the complex numbers. When we measure, we only see **Probability**.
        $$ P(x) = |Amplitude|^2 $$
        
        ### 3. Entanglement
        Try adding a **Hadamard** on Q0, then a **CNOT** (Control 0, Target 1).
        You will see the table shrink to only two rows: `|00⟩` and `|11⟩`.
        Since `|01⟩` and `|10⟩` are missing, Q0 and Q1 are perfectly linked.
        """)

# --- TAB 4: CODE GENERATOR ---
with tab4:
    st.subheader("Export to Python")
    st.caption("Copy this code to run this exact circuit in your terminal.")
    
    code = f"""from qbitUni import QuantumUniverse
import math

# Initialize
u = QuantumUniverse({st.session_state.qubits})

print("🚀 Running Simulation...")
"""
    for op in st.session_state.circuit:
        g = op['gate']
        short = g.split(' ')[0].lower()
        
        if 'c1' in op: # Toffoli
            line = f"u.toffoli({op['c1']}, {op['c2']}, {op['target']})"
        elif 'control' in op:
            if short == "cnot": short = "cnot" # mapping fix
            elif short == "cz": short = "cz"
            elif short == "swap": short = "swap"
            line = f"u.{short}({op['control']}, {op['target']})"
        elif 'angle' in op:
            short = "rx" if "RX" in g else "phase"
            line = f"u.{short}({op['target']}, {op['angle']:.4f}) # {math.degrees(op['angle']):.0f} deg"
        else:
            line = f"u.{short}({op['target']})"
        
        code += line + "\n"

    code += """
# Results
u.print_state()
"""
    st.code(code, language="python")