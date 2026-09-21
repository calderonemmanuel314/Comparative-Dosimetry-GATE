#!/bin/bash

# ==================================================
# 1. DEFINE YOUR 30 EXACT SEEDS HERE
# ==================================================
SEEDS=(
12345 23456 34567 45678 56789
67890 13579 24680 98765 87654
76543 65432 54321 43210 11223
33445 55667 77889 99001 10293
38475 56473 82736 91827 47586
65748 83746 29384 10294 58674
)

# ==================================================
# 2. CREATE THE .TXT LOG FILE WITH TABLE HEADERS
# ==================================================
echo "Trial   | Seed    | Runtime (s)" > runtime_log.txt
echo "-----------------------------------" >> runtime_log.txt

# ==================================================
# 3. INITIALIZE ROOT DIRECTORIES
# ==================================================
# Ensures the main folders exist before GATE fires the first particle
mkdir -p output/MOTHER
mkdir -p output/ROB
mkdir -p output/ORGANS

# ==================================================
# 4. THE EXECUTION LOOP
# ==================================================
for i in {0..0}
do
    # Calculate the Trial Number (1 to 30) and pad it with a zero (01, 02, etc.) for clean sorting
    trial_num=$(printf "%02d" $((i+1)))
    
    # Pull the exact seed from your list
    current_seed=${SEEDS[$i]}

    echo "======================================"
    echo "Starting Trial $trial_num of 30 (Seed: $current_seed)"
    echo "======================================"

    # Run GATE, pass the seed, and capture the real time
    runtime=$(/usr/bin/time -f "%e" Gate -a "[my_seed,$current_seed]" main.mac 2>&1 >/dev/null | tail -n 1)

    # Save the runtime data into your .txt file
    echo -e "$trial_num\t| $current_seed\t| $runtime" >> runtime_log.txt
    
    # --------------------------------------------------
    # FOLDER CREATION & FILE ROUTING
    # --------------------------------------------------
    # 1. Create the specific Run folders inside your sub-directories
    mkdir -p output/MOTHER/Run_${trial_num}
    mkdir -p output/ROB/Run_${trial_num}
    mkdir -p output/ORGANS/Run_${trial_num}

    # 2. Move all generated .txt files from that run into their new Run folders
    # The 2>/dev/null hides the terminal error just in case a folder happens to be empty
    mv output/MOTHER/*.txt output/MOTHER/Run_${trial_num}/ 2>/dev/null
    mv output/ROB/*.txt output/ROB/Run_${trial_num}/ 2>/dev/null
    mv output/ORGANS/*.txt output/ORGANS/Run_${trial_num}/ 2>/dev/null

done

echo "======================================"
echo "ALL 30 RUNS COMPLETE. TEXT LOG GENERATED."
echo "======================================"

# TO RUN, TYPE ./runbatch.sh
