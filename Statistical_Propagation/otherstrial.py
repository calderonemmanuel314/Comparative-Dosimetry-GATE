import numpy as np

# Helper function to combine split organs using quadrature propagation
def combine_organ(E1, U1_pct, E2, U2_pct):
    # Convert percentage to decimal for the variance calculation
    U1, U2 = U1_pct / 100, U2_pct / 100

    E_tot = E1 + E2
    # Absolute uncertainties in quadrature
    sigma_tot = np.sqrt((E1 * U1)**2 + (E2 * U2)**2)

    # Return as combined percentage
    return (sigma_tot / E_tot) * 100

# 1. BRAIN (Lower + Upper)
E_LBrain = np.array([2.78e-10, 6.88e-10, 1.38e-09, 2.76e-09])
U_LBrain = np.array([0.4795, 0.3043, 0.2152, 0.1522])
E_UBrain = np.array([2.47e-10, 6.20e-10, 1.24e-09, 2.49e-09])
U_UBrain = np.array([0.5083, 0.3211, 0.2270, 0.1605])

# 2. ADRENALS (Left + Right)
E_LAdrenal = np.array([1.14e-12, 2.72e-12, 5.47e-12, 1.06e-11])
U_LAdrenal = np.array([6.8405, 4.4080, 3.1461, 2.2365])
E_RAdrenal = np.array([1.08e-12, 2.63e-12, 5.34e-12, 1.05e-11])
U_RAdrenal = np.array([6.9890, 4.4955, 3.1469, 2.2486])

# 3. TESTES (Left + Right)
E_LBall = np.array([1.27e-12, 3.25e-12, 6.56e-12, 1.34e-11])
U_LBall = np.array([6.4472, 4.1213, 2.8981, 2.0339])
E_RBall = np.array([1.31e-12, 3.47e-12, 6.75e-12, 1.32e-11])
U_RBall = np.array([6.5335, 4.0637, 2.8579, 2.0367])

# 4. KIDNEYS (Left + Right)
E_LKidney = np.array([3.92e-11, 9.76e-11, 1.94e-10, 3.88e-10])
U_LKidney = np.array([1.2310, 0.7817, 0.5536, 0.3911])
E_RKidney = np.array([3.83e-11, 9.71e-11, 1.93e-10, 3.88e-10])
U_RKidney = np.array([1.2437, 0.7824, 0.5540, 0.3909])

# 5. OVARIES (Left + Right)
E_LOva = np.array([1.41e-12, 3.66e-12, 7.61e-12, 1.52e-11])
U_LOva = np.array([6.1868, 3.7948, 2.6434, 1.8727])
E_ROva = np.array([1.60e-12, 3.79e-12, 7.44e-12, 1.51e-11])
U_ROva = np.array([5.8562, 3.8379, 2.7113, 1.9043])

# Calculate combinations
brain_combined = combine_organ(E_LBrain, U_LBrain, E_UBrain, U_UBrain)
adrenal_combined = combine_organ(E_LAdrenal, U_LAdrenal, E_RAdrenal, U_RAdrenal)
testes_combined = combine_organ(E_LBall, U_LBall, E_RBall, U_RBall)
kidney_combined = combine_organ(E_LKidney, U_LKidney, E_RKidney, U_RKidney)
ovaries_combined = combine_organ(E_LOva, U_LOva, E_ROva, U_ROva)

# Print cleanly formatted results for the 4 runs [10M, 25M, 50M, 100M]
np.set_printoptions(precision=4, suppress=True)
print("Combined Relative Errors (%) for [10M, 25M, 50M, 100M]:\n")
print(f"Brain:    {brain_combined}")
print(f"Adrenals: {adrenal_combined}")
print(f"Testes:   {testes_combined}")
print(f"Kidneys:  {kidney_combined}")
print(f"Ovaries:  {ovaries_combined}")
