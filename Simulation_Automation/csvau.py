import os
import csv
from collections import defaultdict

# 1. Configuration
base_dir = "output"
categories = ["MOTHER", "ROB", "ORGANS"]

# Data structures: dictionaries storing Run -> Organ -> Value
edep_data = defaultdict(dict)
unc_data = defaultdict(dict)
all_organs = set()

# 2. Rummage through the directories
for category in categories:
    cat_path = os.path.join(base_dir, category)
    if not os.path.exists(cat_path):
        continue
        
    # Dynamically find any folder starting with "Run_"
    run_folders = [f for f in os.listdir(cat_path) if f.startswith("Run_")]
    
    for run_folder in run_folders:
        run_path = os.path.join(cat_path, run_folder)
        
        for file in os.listdir(run_path):
            if not file.endswith(".txt"):
                continue
                
            # Ignore the "Squared" files
            if "Squared" in file:
                continue
                
            file_path = os.path.join(run_path, file)
            
            # 3. Extract the exact value from Line 7
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    if len(lines) >= 7:
                        val = lines[6].strip()
                    else:
                        val = "0"
            except Exception:
                continue

            # 4. Parse the Organ Name from the filename
            clean_name = file.replace(".txt", "")
            organ_name = clean_name.split("-")[0]
            all_organs.add(organ_name)
            
            # 5. Sort into the correct dictionary
            if "Uncertainty" in file:
                unc_data[run_folder][organ_name] = val
            elif "Edep" in file:
                edep_data[run_folder][organ_name] = val

# 6. Format and Export to CSV (TRANSPOSED)
sorted_runs = sorted(list(set(list(edep_data.keys()) + list(unc_data.keys()))))
sorted_organs = sorted(list(all_organs))

def write_to_csv(filename, data_dictionary):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the Header row: [ORGAN NAME, Run_01, Run_02, Run_03...]
        writer.writerow(["ORGAN NAME"] + sorted_runs)
        
        # Write the Data rows
        for organ in sorted_organs:
            row = [organ]  # Start the row with the organ's name
            for run in sorted_runs:
                # Ask the dictionary for this specific run and organ
                row.append(data_dictionary[run].get(organ, "0"))
            writer.writerow(row)

# Save with updated filenames so you don't overwrite your old format if you need it
write_to_csv("Master_Edep_Transposed.csv", edep_data)
write_to_csv("Master_Edep_Unc_Transposed.csv", unc_data)

print(f"Extraction complete! {len(sorted_runs)} runs processed.")
print("Saved Master_Edep_Transposed.csv and Master_Edep_Unc_Transposed.csv to your project folder.")
