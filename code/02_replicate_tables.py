"""
02_replicate_tables.py
Replicate Tables 2-4 from Card & Krueger (1994).
Input:  output/cleaned_data.csv
Output: output/tables/table2.csv, table3.csv, table4.csv
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import os

# ---------- Paths ----------
INPUT_PATH = "output/cleaned_data.csv"
OUTPUT_DIR = "output/tables"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

# ============================================================
# Build long-format data for DID regression
# ============================================================
wave1 = df[['SHEET', 'NJ', 'CHAIN', 'FTE', 'WAGE_ST', 'HRSOPEN']].copy()
wave1.columns = ['id', 'NJ', 'CHAIN', 'FTE', 'WAGE', 'HRSOPEN']
wave1['POST'] = 0

wave2 = df[['SHEET', 'NJ', 'CHAIN', 'FTE2', 'WAGE_ST2', 'HRSOPEN2']].copy()
wave2.columns = ['id', 'NJ', 'CHAIN', 'FTE', 'WAGE', 'HRSOPEN']
wave2['POST'] = 1

long_df = pd.concat([wave1, wave2], ignore_index=True)
long_df = long_df.dropna(subset=['FTE'])

print("Long-format shape:", long_df.shape)
print("Group distribution:")
print(long_df.groupby(['NJ', 'POST'])['FTE'].count())

# ============================================================
# Table 2: Average employment (FTE) by NJ/PA and wave
# ============================================================
table2 = long_df.groupby(['NJ', 'POST'])['FTE'].agg(['mean', 'std', 'count']).reset_index()
table2.columns = ['NJ', 'POST', 'Mean_FTE', 'Std_FTE', 'N']
table2['Group'] = table2['NJ'].map({1: 'New Jersey', 0: 'Pennsylvania'})
table2['Wave'] = table2['POST'].map({0: 'Wave 1 (Pre)', 1: 'Wave 2 (Post)'})

print("\n===== Table 2: Average FTE Employment =====")
print(table2[['Group', 'Wave', 'Mean_FTE', 'Std_FTE', 'N']])

table2.to_csv(os.path.join(OUTPUT_DIR, "table2.csv"), index=False)

# ============================================================
# Table 3: DID regression on employment
# ============================================================
long_df['NJ_POST'] = long_df['NJ'] * long_df['POST']

model = smf.ols('FTE ~ NJ + POST + NJ_POST', data=long_df).fit()

print("\n===== Table 3: DID Regression (Employment) =====")
print(model.summary())

did_coef = model.params['NJ_POST']
did_se = model.bse['NJ_POST']
did_pval = model.pvalues['NJ_POST']

table3 = pd.DataFrame({
    'Variable': ['Intercept', 'NJ', 'POST', 'NJ x POST (DID)'],
    'Coefficient': [model.params['Intercept'], model.params['NJ'],
                    model.params['POST'], did_coef],
    'Std_Error': [model.bse['Intercept'], model.bse['NJ'],
                  model.bse['POST'], did_se],
    'P_value': [model.pvalues['Intercept'], model.pvalues['NJ'],
                model.pvalues['POST'], did_pval]
})

print("\nDID estimate:", round(did_coef, 3), " (Std. Error:", round(did_se, 3), ")")
table3.to_csv(os.path.join(OUTPUT_DIR, "table3.csv"), index=False)

# ============================================================
# Table 4: Robustness checks under alternative specifications
# ============================================================
# Specification 1: full-time employees only (EMPFT)
wave1_ft = df[['SHEET', 'NJ', 'EMPFT']].copy()
wave1_ft.columns = ['id', 'NJ', 'EMP']
wave1_ft['POST'] = 0

wave2_ft = df[['SHEET', 'NJ', 'EMPFT2']].copy()
wave2_ft.columns = ['id', 'NJ', 'EMP']
wave2_ft['POST'] = 1

long_ft = pd.concat([wave1_ft, wave2_ft], ignore_index=True).dropna(subset=['EMP'])
long_ft['NJ_POST'] = long_ft['NJ'] * long_ft['POST']

model_ft = smf.ols('EMP ~ NJ + POST + NJ_POST', data=long_ft).fit()

# Specification 2: with chain fixed effects
model_chain = smf.ols('FTE ~ NJ + POST + NJ_POST + C(CHAIN)', data=long_df).fit()

# Specification 3: with starting wage control
long_df_wage = long_df.dropna(subset=['WAGE'])
model_wage = smf.ols('FTE ~ NJ + POST + NJ_POST + WAGE', data=long_df_wage).fit()

table4 = pd.DataFrame({
    'Specification': ['Full-time only', 'With chain FE', 'With wage control'],
    'DID_Coefficient': [
        model_ft.params['NJ_POST'],
        model_chain.params['NJ_POST'],
        model_wage.params['NJ_POST']
    ],
    'Std_Error': [
        model_ft.bse['NJ_POST'],
        model_chain.bse['NJ_POST'],
        model_wage.bse['NJ_POST']
    ],
    'P_value': [
        model_ft.pvalues['NJ_POST'],
        model_chain.pvalues['NJ_POST'],
        model_wage.pvalues['NJ_POST']
    ]
})

print("\n===== Table 4: Robustness Checks =====")
print(table4)
table4.to_csv(os.path.join(OUTPUT_DIR, "table4.csv"), index=False)

print(f"\nAll tables saved to {OUTPUT_DIR}/")