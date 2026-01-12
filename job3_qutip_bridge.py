"""
QuTiP-Based Quantum Readout to LLR Generation Script
---------------------------------------------------

This script implements a physics-to-decoder bridge for a superconducting
qubit readout system.

What this file does:
1. Simulates dispersive qubit readout using QuTiP in the time domain
   for qubit states |0> and |1>.
2. Generates noisy single-shot measurement trajectories at millikelvin
   temperature (quantum-limited domain).
3. Integrates time-domain signals to produce IQ measurement points.
4. Rotates the IQ plane to align state separation along a single axis.
5. Converts integrated measurements into Log-Likelihood Ratios (LLRs).
6. Quantizes LLRs into 8-bit fixed-point format suitable for LDPC decoders.
7. Exports LLR data and ground-truth bits for external VLSI/FPGA decoding.
8. Visualizes resonator ring-up dynamics and IQ shot clustering.

Purpose:
This file connects quantum measurement physics (QuTiP simulation)
to classical digital decoding (LDPC), enabling realistic end-to-end
readout and error-correction studies.

Context:
Developed as part of a group project for VLSID 2026.
"""




import numpy as np
import matplotlib.pyplot as plt
from qutip import *

def run_qutip_physics_bridge():
    # ==========================================
    # 1. OPTIMIZED PARAMETERS (Updated from latest ADS run)
    # ==========================================
    chi = 1.57e6 * (2 * np.pi)      # 1.57 MHz (Angular Freq)
    kappa = 2.0e3 * (2 * np.pi)     # 2.0 kHz (Angular Freq)
    
    # Readout Pulse Settings
    readout_time = 2.0e-6  # 2 microseconds
    drive_amp = 0.5        # Drive amplitude
    
    print(f"--- RUNNING QUTIP ADVANCED SIMULATION (v2) ---")
    print(f"  > Chi:   {chi/(2*np.pi)/1e6:.2f} MHz")
    print(f"  > Kappa: {kappa/(2*np.pi)/1e3:.2f} kHz")

    # ==========================================
    # 2. QUTIP SOLVER (Time Domain Physics)
    # ==========================================
    N = 10 
    a = destroy(N)
    
    # Hamiltonian for State 0 (-Chi) and State 1 (+Chi)
    H0 = -chi * a.dag() * a + drive_amp * (a.dag() + a)
    H1 = +chi * a.dag() * a + drive_amp * (a.dag() + a)
    c_ops = [np.sqrt(kappa) * a]
    tlist = np.linspace(0, readout_time, 500)
    
    print("  > Evolving system state (Master Equation)...")
    res0 = mesolve(H0, basis(N, 0), tlist, c_ops, [a])
    res1 = mesolve(H1, basis(N, 0), tlist, c_ops, [a])
    
    trace_0 = res0.expect[0]
    trace_1 = res1.expect[0]

    # ==========================================
    # 3. GENERATE 576 MESSAGE BITS
    # ==========================================
    num_bits = 576
    #true_bits = np.zeros(num_bits, dtype=int) # Sending All Zeros
    true_bits = np.random.randint(0, 2, num_bits) # Random
    
    integrated_signals = np.zeros(num_bits, dtype=complex)
    
    print(f"  > Simulating {num_bits} noisy shots...")
    
    # ==========================================
    # 4. ADD NOISE & INTEGRATE
    # ==========================================
    noise_power = 0.05 
    
    for i in range(num_bits):
        if true_bits[i] == 0:
            current_trace = trace_0
        else:
            current_trace = trace_1
            
        noise_trace = (np.random.normal(0, noise_power, len(tlist)) + 
                       1j * np.random.normal(0, noise_power, len(tlist)))
        
        noisy_signal = current_trace + noise_trace
        integrated_signals[i] = np.mean(noisy_signal)

    # ==========================================
    # 5. DIGITIZE & EXPORT (NEW FILENAMES)
    # ==========================================
    avg_0 = np.mean(integrated_signals[true_bits==0])
    avg_1 = np.mean(integrated_signals[true_bits==1])
    rotation_angle = -np.angle(avg_1 - avg_0)
    rotated_signals = integrated_signals * np.exp(1j * rotation_angle)
    
    # Check polarity to ensure State 0 maps to Positive LLR
    # If State 0 is on the Left (Negative), flip the sign
    if np.real(np.mean(rotated_signals[true_bits==0])) < 0:
        rotated_signals = -rotated_signals

    noise_var = np.var(rotated_signals)
    llr_float = (2 * np.real(rotated_signals)) / noise_var
    llr_fixed = np.clip(llr_float * 16, -127, 127).astype(int)

    def to_hex(val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))[2:].upper().zfill(2)

    # --- WRITING TO NEW FILENAMES ---
    with open("llr_input_qutip.mem", "w") as f:
        for val in llr_fixed:
            f.write(f"{to_hex(val, 8)}\n")
            
    np.savetxt("true_bits_qutip.txt", true_bits, fmt='%d')
    print("\nSUCCESS: Generated files:")
    print("  > llr_input_qutip.mem")
    print("  > true_bits_qutip.txt")

    # ==========================================
    # 6. VISUALIZATION
    # ==========================================
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(tlist*1e6, np.real(trace_0), 'b', linewidth=2, label='State 0 (Real)')
    plt.plot(tlist*1e6, np.real(trace_1), 'r', linewidth=2, label='State 1 (Real)')
    plt.title("Time Domain: Resonator Ring-Up (QuTiP)")
    plt.xlabel("Time (microseconds)")
    plt.ylabel("Signal Amplitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.scatter(np.real(integrated_signals[true_bits==0]), np.imag(integrated_signals[true_bits==0]), 
                s=5, alpha=0.5, color='blue', label='State 0')
    if np.any(true_bits==1):
        plt.scatter(np.real(integrated_signals[true_bits==1]), np.imag(integrated_signals[true_bits==1]), 
                    s=5, alpha=0.5, color='red', label='State 1')
    plt.title("Integrated IQ Shots (With Noise)")
    plt.xlabel("I")
    plt.ylabel("Q")
    plt.axis('equal')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_qutip_physics_bridge()
