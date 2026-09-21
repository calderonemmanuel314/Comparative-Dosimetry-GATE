import trimesh
import os

def calculate_stl_volume(file_path):
    # Load the STL file
    mesh = trimesh.load(file_path)
    
    # Check if the mesh is watertight (closed). GATE hates open meshes!
    if not mesh.is_watertight:
        print(f"⚠️ WARNING: {os.path.basename(file_path)} is NOT watertight. Volume may be inaccurate and GATE might crash.")
    
    # Trimesh calculates volume based on the units of your STL. 
    # If your STL was exported in millimeters (mm), the volume is in mm³.
    # To convert mm³ to cm³, divide by 1000.
    volume_units = mesh.volume 
    volume_cm3 = volume_units / 1000.0  # Adjust this if your STL is already in cm!
    
    print(f"File: {os.path.basename(file_path)}")
    print(f"Exact Mesh Volume: {volume_cm3:.4f} cm³\n")

# Just drop the path to your STL file here
calculate_stl_volume("Ribcage.stl")
calculate_stl_volume("UpperFace.stl")
calculate_stl_volume("Teeth.stl")
calculate_stl_volume("Mandible.stl")
