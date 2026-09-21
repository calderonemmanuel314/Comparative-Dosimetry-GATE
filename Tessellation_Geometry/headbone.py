import numpy as np
from skimage import measure
from stl import mesh

# ==========================================
# 1. HAN (2006) 10-YEAR-OLD BENCHMARKS
# ==========================================
target_mandible = 139.4    # cm^3
target_teeth = 26.0        # cm^3
target_ufr = 194.854       # cm^3
target_total = target_mandible + target_teeth + target_ufr # 360.254 cm^3

# ==========================================
# 2. CRISTY (1980) GEOMETRY & LOCAL BOUNDS
# ==========================================
a1, b1 = 6.93, 8.90          # Outer axes for the face
z_start, z_end = -3.985, 6.135 # Local Z limits inside Head_Cyl

# Cranium Exclusion Parameters (Local to Head_Cyl)
a_cran, b_cran, c_cran = 7.00, 8.97, 6.16
z_cran_center = 7.59

# ==========================================
# 3. 3D GRID SETUP
# ==========================================
print("Setting up voxel grid (Resolution: 0.2 cm)...")
res = 0.2
x = np.arange(-7.5, 7.5, res)
y = np.arange(-9.5, 0.5, res) # Front half only (Y <= 0)
z = np.arange(-4.5, 6.5, res)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# Base Static Masks
outer_cyl = (X/a1)**2 + (Y/b1)**2 <= 1
z_bounds = (Z >= z_start) & (Z <= z_end)
cranium_scoop = (X/a_cran)**2 + (Y/b_cran)**2 + ((Z - z_cran_center)/c_cran)**2 > 1
base_mask = outer_cyl & z_bounds & cranium_scoop

# ==========================================
# 4. ITERATIVE BONE INFLATION
# ==========================================
print(f"Inflating bone thickness to hit target volume: {target_total:.3f} cm^3...")
d_min, d_max = 0.74, 6.90 # Cristy's base 'd' up to max possible
final_mask = None
final_d = 0

for i in range(25): # Binary search
    d = (d_min + d_max) / 2
    inner_cyl = (X/(a1-d))**2 + (Y/(b1-d))**2 >= 1
    current_mask = base_mask & inner_cyl
    vol = np.sum(current_mask) * (res**3)
    
    if vol < target_total:
        d_min = d # Need more bone -> smaller inner cavity -> increase d
    else:
        d_max = d # Need less bone -> larger inner cavity -> decrease d
        
    final_mask = current_mask
    final_d = d

print(f"Optimization complete. Final bone thickness 'd': {final_d:.3f} cm")
print(f"Total Mesh Volume: {np.sum(final_mask) * (res**3):.3f} cm^3")

# ==========================================
# 5. THE 3-PART Z-AXIS SLICE
# ==========================================
print("Slicing mask into Mandible, Teeth, and Upper Face...")
vol_per_z = np.sum(final_mask, axis=(0, 1)) * (res**3)
cum_vol = np.cumsum(vol_per_z)

# Find array indices where cumulative volume hits the benchmarks
idx_mandible = np.argmax(cum_vol >= target_mandible)
idx_teeth = np.argmax(cum_vol >= (target_mandible + target_teeth))

# Generate isolated masks
mask_mandible = np.zeros_like(final_mask)
mask_mandible[:, :, :idx_mandible] = final_mask[:, :, :idx_mandible]

mask_teeth = np.zeros_like(final_mask)
mask_teeth[:, :, idx_mandible:idx_teeth] = final_mask[:, :, idx_mandible:idx_teeth]

mask_ufr = np.zeros_like(final_mask)
mask_ufr[:, :, idx_teeth:] = final_mask[:, :, idx_teeth:]

import scipy.ndimage as ndi

# ==========================================
# 6. MESH GENERATION & EXPORT
# ==========================================
def export_stl(mask_data, filename):
    if np.sum(mask_data) == 0:
        return
        
    # 1. Pad generously to give the mold enough room to close
    padded = np.pad(mask_data, pad_width=2, mode='constant', constant_values=0)
    
    # 2. THE WATERTIGHT FIX: Gaussian smooth the binary mask
    # This turns blocky voxels into a smooth gradient, preventing Geant4 "hole" errors
    print(f"Applying watertight seal to {filename}...")
    smoothed = ndi.gaussian_filter(padded.astype(float), sigma=0.5)
    
    # 3. Extract the surface
    verts, faces, normals, values = measure.marching_cubes(smoothed, level=0.5)
    
    # Flip triangles outward
    faces = np.flip(faces, axis=1)
    
    # Convert back to physical cm coords (Subtract 2 due to pad_width=2)
    verts = (verts - 2) * res + np.array([x[0], y[0], z[0]])
    verts *= 10.0 # Scale to mm
    
    # Construct STL
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            mesh_data.vectors[i][j] = verts[f[j], :]
            
    mesh_data.save(filename)
    vol_cm3 = np.sum(mask_data) * (res**3)
    print(f"Exported {filename} | Final Tally: {vol_cm3:.3f} cm^3")

print("All facial structures successfully exported!")
