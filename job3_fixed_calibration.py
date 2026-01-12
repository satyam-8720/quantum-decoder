"""
Forced All-Zero LLR Generator for LDPC Decoder Verification
-----------------------------------------------------------

This script generates a perfect all-zero test input for validating
the correctness of an LDPC decoder.

What this file does:
1. Creates a 576-bit LLR stream where every value represents a
   strong and unambiguous logic '0'.
2. Encodes each LLR as +127 (0x7F), corresponding to maximum
   confidence for bit = 0 in 8-bit two’s complement format.
3. Writes the LLR stream to a memory initialization file
   (llr_input_qutip.mem) for use in Vivado/FPGA simulation.
4. Generates the corresponding ground-truth bit file
   (true_bits_qutip.txt), containing all zeros.

Purpose:
This script is used for baseline verification of the LDPC decoder.
If the decoder is implemented correctly, it must output all zeros
when driven with these ideal, noise-free LLRs.

Context:
Used as part of an end-to-end quantum readout to LDPC decoding
pipeline.
"""



import numpy as np

def generate_forced_zeros():
    print("--- GENERATING PERFECT ALL-ZERO INPUTS ---")
    
    # 1. Create 576 "Strong 0" votes
    # In your system: Positive (+127) = Logic 0
    # Hex for +127 is 7F
    num_bits = 576
    
    # We create an array of purely +127
    llr_fixed = np.full(num_bits, 127, dtype=int)
    
    # 2. Write to file
    def to_hex(val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))[2:].upper().zfill(2)

    with open("llr_input_qutip.mem", "w") as f:
        for val in llr_fixed:
            f.write(f"{to_hex(val, 8)}\n")
            
    # 3. Write True Bits (All 0)
    true_bits = np.zeros(num_bits, dtype=int)
    np.savetxt("true_bits_qutip.txt", true_bits, fmt='%d')
    
    print("SUCCESS: Generated 'llr_input_qutip.mem'")
    print("Every line is now '7F' (Strong 0).")
    print("Go to Vivado -> Reset Simulation -> Run All.")

if __name__ == "__main__":
    generate_forced_zeros()
