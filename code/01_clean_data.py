"""
01_clean_data.py
Card & Krueger (1994) Minimum Wage and Employment
Data cleaning and variable construction.
Input:  data/raw/public.csv
Output: data/processed/cleaned_data.csv
"""

import pandas as pd
import numpy as np
import os

# ---------- Path settings ----------
INPUT_PATH = "data/raw/public.csv"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Load data ----------
df = pd.read_csv(INPUT_PATH)

# ---------- Basic cleaning ----------
# Convert empty strings or whitespace to NaN
df = df.replace(r'^\s*$', np.nan, regex=True)

# Convert numeric variables
numeric_cols = [
    'EMPFT', 'EMPPT', 'NMGRS', 'WAGE_ST', 'INCTIME', 'FIRSTINC',
    'BONUS', 'PCTAFF', 'MEALS', 'HRSOPEN', 'PSODA', 'PFRY', 'PENTREE',
    'NREGS', 'NREGS11',
    'EMPFT2', 'EMPPT2', 'NMGRS2', 'WAGE_ST2', 'INCTIME2', 'FIRSTIN2',
    'SPECIAL2', 'MEALS2', 'HRSOPEN2', 'PSODA2', 'PFRY2', 'PENTREE2',
    'NREGS2', 'NREGS112'
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# ---------- Construct key variables ----------
# 1. Full-Time Equivalent employment
#    FTE = full-time employees + 0.5 * part-time employees + 0.5 * managers
df['FTE'] = df['EMPFT'] + 0.5 * df['EMPPT'] + 0.5 * df['NMGRS']
df['FTE2'] = df['EMPFT2'] + 0.5 * df['EMPPT2'] + 0.5 * df['NMGRS2']

# 2. Treatment group dummy (NJ = 1, PA = 0)
df['NJ'] = (df['STATE'] == 1).astype(int)

# 3. Starting wage (wave 1)
df['WAGE_START'] = df['WAGE_ST']

# 4. Chain identifier
df['CHAIN'] = df['CHAIN'].astype(int)

# ---------- Inspect key variables ----------
print("Data shape:", df.shape)
print("\nTreatment group distribution (NJ=1):")
print(df['NJ'].value_counts())
print("\nFTE summary statistics (Wave 1):")
print(df['FTE'].describe())
print("\nFTE2 summary statistics (Wave 2):")
print(df['FTE2'].describe())

# ---------- Save cleaned data ----------
df.to_csv(os.path.join(OUTPUT_DIR, "cleaned_data.csv"), index=False)
print(f"\nCleaned data saved to {OUTPUT_DIR}/cleaned_data.csv")