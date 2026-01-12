import os

def generate_printer_tb():
    filename = "tb_decoder_printer.v"
    print(f"--- GENERATING PRINTER TESTBENCH ---")
    
    with open(filename, "w") as f:
        f.write("`timescale 1ns / 1ps\n")
        f.write("module tb_decoder_printer;\n")
        
        # Signals
        f.write("    reg clk; reg rst;\n")
        # Generate 576 Inputs and Outputs
        for i in range(1, 577): f.write(f"    reg signed [31:0] L{i};\n")
        for i in range(1, 577): f.write(f"    wire P{i};\n")

        # Memory
        f.write("\n    reg signed [7:0] raw_memory [0:575];\n    integer i;\n")

        # Instantiate Decoder
        f.write("\n    LDPC_decoder_TOP dut (\n")
        f.write("        .clk(clk), .rst(rst),\n")
        for i in range(1, 577): f.write(f"        .L{i}(L{i}),\n")
        for i in range(1, 577): 
            comma = "," if i < 576 else ""
            f.write(f"        .P{i}(P{i}){comma}\n")
        f.write("    );\n")

        # Clock
        f.write("\n    initial begin clk=0; forever #5 clk=~clk; end\n")

        # Main Process
        f.write("\n    initial begin\n")
        f.write("        rst=0;\n")
        f.write('        $readmemh("llr_input_qutip.mem", raw_memory);\n')
        f.write("        #20;\n")
        
        # Load Data
        for i in range(1, 577):
            f.write(f"        L{i} = {{{{24{{raw_memory[{i-1}][7]}}}}, raw_memory[{i-1}]}};\n")
            
        # Reset Pulse
        f.write("\n        #100; rst=1; #200; rst=0;\n")
        f.write("        $display(\"--- Decoding Started... ---\");\n")
        f.write("        #20000; // Wait 20us for decoder to finish\n\n")
        
        # --- THE PRINTER SECTION ---
        f.write("        $display(\"--- START CODEWORD COPY ---\");\n")
        f.write("        $display(\"true_bits = np.array([\");\n")
        
        # Print outputs in groups of 10 for readability, formatted for Python
        for i in range(1, 577):
            # We use a bit of trickery to print P1, P2...
            # Note: We print a comma after every bit except the last one
            suffix = "," if i < 576 else ""
            f.write(f"        $write(\"%b{suffix} \", P{i});\n")
            if i % 20 == 0: f.write("        $write(\"\\n\");\n") # Newline every 20 bits
            
        f.write("\n        $display(\"]);\");\n")
        f.write("        $display(\"--- END CODEWORD COPY ---\");\n")
        f.write("        $finish;\n")
        f.write("    end\n")
        f.write("endmodule\n")

    print(f"SUCCESS: Created '{filename}' in {os.getcwd()}")

if __name__ == "__main__":
    generate_printer_tb()