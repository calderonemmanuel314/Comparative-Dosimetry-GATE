import numpy as np

# 1. Input the Relative Errors (%) as decimals for all 4 runs [10M, 25M, 50M, 100M]
R_LL = np.array([0.0051, 0.0032, 0.0023, 0.0016])
R_LHP = np.array([0.0096, 0.0061, 0.0043, 0.0030])
R_RL = np.array([0.0054, 0.0034, 0.0024, 0.0017])
R_RHP = np.array([0.0201, 0.0127, 0.0090, 0.0064])

# 2. Input the exact Edep values for all 4 runs [10M, 25M, 50M, 100M]
E_LL = np.array([1438.538113, 3609.726978, 7212.718443, 14418.24493])  # Insert Left Gross Lung Edep array
E_LHP = np.array([395.6976456, 995.9916633, 1984.250746, 3957.43893]) # Insert Left Heart Pocket Edep array
E_RL = np.array([1253.601503, 3138.471159, 6283.848063, 12565.20018])  # Insert Right Gross Lung Edep array
E_RHP = np.array([86.52531647, 216.4309103, 431.7106636, 855.8651155]) # Insert Right Heart Pocket Edep array

# 3. Calculate Total Net Energy per run
E_net_total = (E_LL - E_LHP) + (E_RL - E_RHP)

# 4. Calculate Pooled Absolute Uncertainty per run (Variances add in quadrature)
sigma_pooled = np.sqrt((R_LL * E_LL)**2 +
                       (R_LHP * E_LHP)**2 +
                       (R_RL * E_RL)**2 +
                       (R_RHP * E_RHP)**2)

# 5. Calculate Final Combined Relative Error (%) per run
R_net_total_percent = (sigma_pooled / E_net_total) * 100

print("Combined Net Lung Relative Errors for [10M, 25M, 50M, 100M]:")
print(np.round(R_net_total_percent, 3))
