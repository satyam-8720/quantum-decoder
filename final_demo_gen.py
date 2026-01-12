"""
LDPC Error-Correction Demonstration Input Generator
---------------------------------------------------

This script generates a controlled error-injection test case to
demonstrate the error-correction capability of an LDPC decoder.

What this file does:
1. Assumes an all-zero codeword as the correct transmitted data.
2. Creates a 576-bit LLR input stream initialized to strong logic '0'
   (+127 / 0x7F in 8-bit two’s complement format).
3. Injects deliberate, high-confidence errors by flipping selected
   LLR values to strong logic '1' (-127 / 0x81).
4. Writes the corrupted LLR stream to a memory file
   (llr_input_qutip.mem) for Vivado/FPGA simulation.
5. Writes the corresponding ground-truth bit file
   (true_bits_qutip.txt), containing all zeros.

Purpose:
This test verifies that the LDPC decoder can correctly recover the
original codeword even when multiple bits are strongly corrupted.
Successful decoding (all-zero output) confirms proper soft-decision
message passing and parity-check enforcement.

Context:
Used as part of the end-to-end quantum readout to LDPC decoding
pipeline.
"""



import numpy as np

def generate_error_correction_demo():
    print("--- GENERATING ERROR CORRECTION DEMO ---")
    
    num_bits = 576
    
    # 1. THE TRUTH (Answer Key)
    # We know [0, 0, 0...] is a valid codeword.
    true_bits = np.zeros(num_bits, dtype=int)
    
    # 2. THE INPUT (With Noise/Errors)
    # Start with perfect "Strong 0" votes (+127 / Hex 7F)
    llr_values = np.full(num_bits, 127, dtype=int)
    
    # 3. INJECT ERRORS (The "Actual Signal" part)
    # We flip 10 specific bits to "Strong 1" (-127 / Hex 81)
    # This simulates a massive noise spike or data corruption.
    error_indices = [10, 50, 100, 150, 200, 250, 300, 350, 400, 450]
    
    print(f"Injecting Errors at indices: {error_indices}")
    for idx in error_indices:
        llr_values[idx] = -127 # Flip to Logic 1
        
    # 4. SAVE FILES
    def to_hex(val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))[2:].upper().zfill(2)

    with open("llr_input_qutip.mem", "w") as f:
        for val in llr_values:
            f.write(f"{to_hex(val, 8)}\n")
            
    np.savetxt("true_bits_qutip.txt", true_bits, fmt='%d')
    
    print("SUCCESS: Files Generated.")
    print("  > Input File has 10 deliberate errors.")
    print("  > True Bits file is perfect Zeros.")
    print("  > If Vivado Output is All Zeros, the Decoder WORKED.")

if __name__ == "__main__":
    generate_error_correction_demo()
