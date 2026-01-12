import os

def generate_testbench_fixed():
    current_path = os.getcwd()
    filename = "tb_decoder_generated.v"
    
    print(f"--- GENERATING FIXED VERILOG TESTBENCH ---")
    
    with open(filename, "w") as f:
        # --- HEADER ---
        f.write("`timescale 1ns / 1ps\n\n")
        f.write("module tb_decoder_generated;\n\n")
        
        # --- SIGNALS ---
        f.write("    reg clk;\n")
        f.write("    reg rst;\n")
        
        # Inputs L1..L576
        for i in range(1, 577):
            f.write(f"    reg signed [31:0] L{i};\n")
            
        # Outputs P1..P576
        for i in range(1, 577):
            f.write(f"    wire P{i};\n")

        # Memory
        f.write("\n    reg signed [7:0] raw_memory [0:575];\n")
        f.write("    integer i;\n\n")

        # --- INSTANTIATE ---
        # IMPORTANT: Using the correct module name "LDPC_decoder_TOP"
        f.write("    LDPC_decoder_TOP dut (\n")
        f.write("        .clk(clk),\n")
        f.write("        .rst(rst),\n")
        
        for i in range(1, 577):
            f.write(f"        .L{i}(L{i}),\n")
            
        for i in range(1, 577):
            if i == 576:
                f.write(f"        .P{i}(P{i})\n")
            else:
                f.write(f"        .P{i}(P{i}),\n")
        f.write("    );\n\n")

        # --- CLOCK ---
        f.write("    initial begin\n")
        f.write("        clk = 0;\n")
        f.write("        forever #5 clk = ~clk;\n")
        f.write("    end\n\n")

        # --- MAIN TEST (THE FIX IS HERE) ---
        f.write("    initial begin\n")
        f.write("        // 1. Initialize Everything\n")
        f.write("        clk = 0;\n")
        f.write("        rst = 0;\n")
        f.write('        $readmemh("llr_input.mem", raw_memory);\n')
        f.write("        #20;\n\n")
        
        f.write("        // 2. Apply Data FIRST (While Reset is Low)\n")
        f.write("        // This ensures 'L' is valid before we tell the chip to read it.\n")
        for i in range(1, 577):
            f.write(f"        L{i} = {{{{24{{raw_memory[{i-1}][7]}}}}, raw_memory[{i-1}]}};\n")
            
        f.write("\n        // 3. NOW Pulse Reset\n")
        f.write("        // The chip will wake up, see the valid L data, and load it.\n")
        f.write("        #100;\n")
        f.write("        rst = 1;  // Reset ON\n")
        f.write("        #200;\n")
        f.write("        rst = 0;  // Reset OFF (Start Decoding)\n\n")
        
        f.write("        // 4. Wait for Result\n")
        f.write("        $display(\"--- Decoding Started... ---\");\n")
        f.write("        #20000; // Wait 20us\n\n")
        
        f.write("        $display(\"--- SIMULATION COMPLETE ---\");\n")
        f.write("        $finish;\n")
        f.write("    end\n\n")
        
        f.write("endmodule\n")

    print(f"SUCCESS: Fixed Testbench generated at {current_path}")

if __name__ == "__main__":
    generate_testbench_fixed()