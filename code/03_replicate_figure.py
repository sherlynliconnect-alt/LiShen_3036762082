"""
03_replicate_figure.py
Replicate Figure 1 from Card & Krueger (1994).
Input:  output/cleaned_data.csv
Output: output/figures/figure1.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------- Paths ----------
INPUT_PATH = "output/cleaned_data.csv"
OUTPUT_DIR = "output/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

# ---------- Build long-format data ----------
wave1 = df[['SHEET', 'NJ', 'FTE']].copy()
wave1.columns = ['id', 'NJ', 'FTE']
wave1['POST'] = 0

wave2 = df[['SHEET', 'NJ', 'FTE2']].copy()
wave2.columns = ['id', 'NJ', 'FTE']
wave2['POST'] = 1

long_df = pd.concat([wave1, wave2], ignore_index=True).dropna(subset=['FTE'])

# ---------- Compute group means ----------
means = long_df.groupby(['NJ', 'POST'])['FTE'].mean().reset_index()
means['Group'] = means['NJ'].map({1: 'New Jersey', 0: 'Pennsylvania'})
means['Wave'] = means['POST'].map({0: 'Pre', 1: 'Post'})

print("Group means:")
print(means)

# ---------- Plot Figure 1 ----------
fig, ax = plt.subplots(figsize=(8, 6))

for group in ['New Jersey', 'Pennsylvania']:
    subset = means[means['Group'] == group]
    ax.plot(subset['Wave'], subset['FTE'], marker='o', linewidth=2,
            label=group, markersize=10)

nj_pre = means[(means['Group'] == 'New Jersey') & (means['Wave'] == 'Pre')]['FTE'].values[0]
nj_post = means[(means['Group'] == 'New Jersey') & (means['Wave'] == 'Post')]['FTE'].values[0]
pa_pre = means[(means['Group'] == 'Pennsylvania') & (means['Wave'] == 'Pre')]['FTE'].values[0]
pa_post = means[(means['Group'] == 'Pennsylvania') & (means['Wave'] == 'Post')]['FTE'].values[0]

did_estimate = (nj_post - nj_pre) - (pa_post - pa_pre)

ax.set_xlabel('Survey Wave', fontsize=12)
ax.set_ylabel('Average Full-Time Equivalent Employment', fontsize=12)
ax.set_title('Figure 1: Employment in NJ vs PA Fast-Food Restaurants\n'
             f'DID Estimate = {did_estimate:.2f}', fontsize=13)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "figure1.png"), dpi=300)
plt.show()

print(f"\nFigure 1 saved to {OUTPUT_DIR}/figure1.png")
print(f"DID estimate: {did_estimate:.3f}")