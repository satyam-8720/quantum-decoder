# End-to-End Superconducting Qubit Readout and LDPC Decoding Pipeline

This repository contains an end-to-end design-to-decode simulation pipeline for superconducting transmon qubits.  
This work was carried out as a **group project for VLSID 2026**.

The project connects quantum device physics with classical digital signal processing and VLSI decoding, demonstrating how physical readout design impacts classical error-correction performance.

---

## Project Motivation

Superconducting qubits do not directly produce digital bits. Instead, they generate weak and noisy microwave signals that must be amplified, processed, and statistically interpreted. Reliable quantum systems therefore require a realistic and hardware-aware readout chain extending from millikelvin quantum devices to room-temperature electronics.

This project models the complete measurement and decoding pipeline instead of relying on idealized assumptions.

---

## End-to-End Workflow

QuantumPro (Qubit + Resonator Design)  
→ EM Simulation & Energy Participation Analysis  
→ QuTiP Quantum Readout Simulation (4 mK)  
→ Cryogenic Amplifier Modeling (4–10 K)  
→ Digital Signal Processing (Integration & IQ Rotation)  
→ Log-Likelihood Ratio (LLR) Generation & Quantization  
→ LDPC Soft-Decision Decoder  

---

## Key Technical Components

### 1. Transmon Qubit and Readout Resonator Design
- Geometry-based design using Keysight QuantumPro
- Optimization of interdigital capacitors, CPW lines, and coupling structures
- Extraction of qubit frequency, resonator frequency, anharmonicity, quality factor, and T₁

---

### 2. Energy Participation and S-Parameter Analysis
- Electromagnetic extraction of participation ratios
- Identification of dominant loss mechanisms
- Verification of dispersive regime operation

---

### 3. Quantum Readout Simulation (QuTiP)
- Dispersive readout simulation at 4 mK
- Time-domain resonator ring-up and decay
- Single-shot measurement trajectory generation

---

### 4. Cryogenic Amplifier Modeling
- Gain scaling to hardware-realistic signal levels
- Effective noise temperature modeling
- Finite bandwidth effects
- Transition from quantum-limited to classical Gaussian noise

---

### 5. Digital Signal Processing (DSP)
- Time-domain integration of noisy measurement traces
- IQ demodulation and phase rotation
- Projection onto the optimal measurement axis

---

### 6. Log-Likelihood Ratio (LLR) Generation
- Soft-decision representation of qubit states
- Noise-aware confidence estimation
- Quantization to 8-bit two’s complement format

---

### 7. LDPC Decoder Integration
- Full soft-decision LDPC decoding
- Validation using all-zero codeword and error-injection tests
- Demonstration of error correction under noisy readout conditions

---

## LDPC Decoder Source

## LDPC Decoder Source

This project integrates an open-source LDPC decoder implementation:
https://github.com/biren15/Design-and-Verification-of-LDPC-Decoder

The LDPC decoder RTL and core algorithm logic were adopted from the above repository.
This project focuses on system–level integration, fixed-point LLR interfacing,
verification using Vivado simulations, and demonstration of error-correction
performance under controlled test cases.

## Challenges and Limitations

- Simplified cryogenic amplifier nonlinearity modeling
- Partial ADC non-idealities
- Limited parameter sweeps due to simulation complexity
- Hardware constraints such as latency and fixed-point precision

---

## Future Work

- Improved amplifier and ADC modeling
- Machine-learning-based LLR generation
- Multi-qubit and multi-channel readout
- FPGA/ASIC implementation of the LDPC decoder
- Automated EM → quantum → decoding workflow

---

## Team – VLSID 2026 Group Project

- SATYAM CHAUHAN  
- PRIYAM MISHRA  
- TUSHAR GARG  
- AMAN RAJ SAURAV  

---

## References

- J. Koch et al., Phys. Rev. A, 2007  
- A. Wallraff et al., Nature, 2004  
- J. R. Johansson et al., Computer Physics Communications, 2012  
- J. Chen and M. Fossorier, IEEE Transactions on Communications, 2002  

---

## License

For academic and research use only.
