import numpy as np
from stl import mesh
from skimage import measure

# --- 1. DEFINE CRISTY'S PARAMETERS (10-Year-Old) ---
a = 11.72       # Outer X semi-axis (cm)
b = 8.1     # Outer Y semi-axis (cm)
d = 0.35       # Rib thickness
z1 = 25.43     # Bottom of rib cage
z2 = 48.89     # Top of rib cage
c = 1.02       # Spacing parameter

# --- 2. SETUP THE 3D GRID ---
# We add padding to the boundaries so marching_cubes can close the mesh (watertight!)
resolution = 0.2 # THIS IS THE VOXEL RESOLUTION
x_range = np.arange(-(a + 2), (a + 2), resolution)
y_range = np.arange(-(b + 2), (b + 2), resolution)
z_range = np.arange(z1 - 2, z2 + 2, resolution)

X, Y, Z = np.meshgrid(x_range, y_range, z_range, indexing='ij')

# --- 3. THE SQUISHED TORUS MATH ---
# Condition 1: Must be inside the outer ellipse
outer_ellipse = (X/a)**2 + (Y/b)**2 <= 1

# Condition 2: Must be outside the inner ellipse
inner_ellipse = (X/(a-d))**2 + (Y/(b-d))**2 >= 1

# Condition 3: Z-boundaries
z_bounds = (Z >= z1) & (Z <= z2)

# Condition 4: The "Squished Torus" Z-Slicer
# Cristy used flat integer steps. We use a cosine wave based on 'c' to make it rounded.
# Period is 2*c. When cos() > 0, it's bone. When cos() < 0, it's gap.
# We add a slight threshold (e.g., 0.2) to sculpt the thickness of the rounded torus.
rib_wave = np.cos(np.pi * (Z - z1) / c) > -0.39

# Combine all conditions to carve out the ribs
rib_cage_voxels = outer_ellipse & inner_ellipse & z_bounds & rib_wave

# Convert boolean array to float for marching cubes
rib_cage_matrix = np.asarray(rib_cage_voxels, dtype=float)

# --- 4. GENERATE THE MESH ---
print("Running marching cubes... (This might take a minute)")
# level=0.5 extracts the surface halfway between our 0 (air) and 1 (bone) voxels
verts, faces, normals, values = measure.marching_cubes(rib_cage_matrix, level=0.5, spacing=(resolution, resolution, resolution))

faces = np.flip(faces, axis=1)

# --- 5. EXPORT TO STL ---
# Create the mesh object
rib_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        # We need to shift the vertices back to their true spatial coordinates
        rib_mesh.vectors[i][j] = verts[f[j]] + [x_range[0], y_range[0], z_range[0] - 27.16]
        
# ADD THIS LINE HERE:
rib_mesh.vectors *= 10.0  # Convert all cm coordinates to mm for GATE!
# Save the file
output_filename = 'Ribcage.stl'
rib_mesh.save(output_filename)
print(f"Success! {output_filename} has been generated.")
