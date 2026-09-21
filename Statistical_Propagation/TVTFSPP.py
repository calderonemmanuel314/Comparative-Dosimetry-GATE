import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Input Data
primaries = [10, 25, 50, 100]

# Micro-Organs (High Variance due to small volume)
err_adrenals = [4.8887, 3.1474, 2.2251, 1.5857]
err_testes = [4.5910, 2.8941, 2.0349, 1.4392]
err_ovaries = [4.2532, 2.6996, 1.8929, 1.3354]

# Macro-Organs (Low Variance due to large volume)
err_brain = [0.3488, 0.2209, 0.1562, 0.1104]
err_kidneys = [0.8749, 0.5530, 0.3916, 0.2765]
err_lungs = [0.4900, 0.3090, 0.2190, 0.1540]
# Converting raw decimals to percentages (* 100)
err_spleen = np.array([0.00996, 0.00629, 0.00446, 0.00315]) * 100
err_stomach = np.array([0.00482, 0.00305, 0.00216, 0.00153]) * 100
err_thymus = np.array([0.01035, 0.00652, 0.00461, 0.00326]) * 100
err_bladder = np.array([0.00614, 0.00388, 0.00274, 0.00194]) * 100

# Calculate the mean convergence for each cluster
micro_group = [err_adrenals, err_testes, err_ovaries]
macro_group = [err_brain, err_kidneys, err_lungs, err_spleen, err_stomach, err_thymus, err_bladder]

micro_means = np.mean(micro_group, axis=0)
macro_means = np.mean(macro_group, axis=0)

# Actual Runtime Data
runtime_minutes = [12.08, 43.72, 80.14, 135.41]

# 2. Structure data for Seaborn (Long-form DataFrame)
data = []
all_organs = micro_group + macro_group

for i, primary in enumerate(primaries):
    for organ_err in all_organs:
        data.append({'Primaries (Millions)': primary, 'Relative Error (%)': organ_err[i]})

df = pd.DataFrame(data)

# 3. Plotting Setup
sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
fig, ax1 = plt.subplots(figsize=(10, 6))

# 4. Left Axis: Seaborn Stripplot (Organ Errors)
sns.stripplot(
    data=df,
    x='Primaries (Millions)',
    y='Relative Error (%)',
    color='#5C6B73',
    alpha=0.6,
    jitter=0.1,
    size=7,
    ax=ax1,
    label='Organ Edep Uncertainty'
)

# Plot the lines of best fit (Convergence Curves)
# X-coordinates for the lines correspond to the categorical indices [0, 1, 2, 3]
ax1.plot([0, 1, 2, 3], micro_means, color='#d62728', linestyle='-.', linewidth=2, label='Micro-Organ Trend')
ax1.plot([0, 1, 2, 3], macro_means, color='#2ca02c', linestyle='-.', linewidth=2, label='Macro-Organ Trend')

# Add the 5% threshold line
ax1.axhline(y=5.0, color='red', linestyle='--', alpha=0.8, linewidth=2, label='5% Acceptability Threshold')

# 5. Right Axis: Runtime Line Plot
ax2 = ax1.twinx()
sns.lineplot(
    x=[0, 1, 2, 3],
    y=runtime_minutes,
    color='#861A86',
    marker='s',
    markersize=8,
    linewidth=2.5,
    ax=ax2,
    label='Simulation Runtime'
)

# 6. Formatting and Labels
ax1.set_title('Computational Optimization: Uncertainty vs. Runtime', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Relative Error (%)', fontsize=12, color='black')
ax2.set_ylabel('Runtime (Minutes)', fontsize=12, color='#861A86')

# Adjust y-axis limits
ax1.set_ylim(0, max(df['Relative Error (%)']) + 1)
ax2.set_ylim(0, max(runtime_minutes) + 20)

# Legend Handling
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()

# Clean up duplicate stripplot legends and combine
unique_handles = [lines_1[0], lines_1[-3], lines_1[-2], lines_1[-1], lines_2[0]]
unique_labels = ['Organ Data Points', 'Small-Volume Organs Trend', 'Large-Volume Organs Trend', '5% Threshold', 'Runtime']
ax1.legend(unique_handles, unique_labels, loc='center right', framealpha=0.9, fontsize=10)

plt.tight_layout()
plt.show()
