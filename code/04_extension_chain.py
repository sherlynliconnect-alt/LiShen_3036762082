"""
04_extension_chain.py
Independent Extension: Heterogeneous Effects of the Minimum Wage
by Fast-Food Chain (Card & Krueger 1994 replication data).

Research question:
    Did the employment effect of New Jersey's minimum wage increase
    differ across fast-food chains (Burger King, KFC, Roy Rogers, Wendy's)?

Input:  output/cleaned_data.csv
Output: output/tables/extension_chain.csv
        output/figures/extension_chain.png
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import os

# ---------- Paths ----------
INPUT_PATH = "output/cleaned_data.csv"
TABLE_DIR = "output/tables"
FIGURE_DIR = "output/figures"
os.makedirs(TABLE_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

# ---------- Chain labels ----------
# CHAIN codes in the data: 1 = Burger King, 2 = KFC, 3 = Roy Rogers, 4 = Wendy's
chain_labels = {1: "Burger King", 2: "KFC", 3: "Roy Rogers", 4: "Wendy's"}
df["CHAIN_NAME"] = df["CHAIN"].map(chain_labels)

# ============================================================
# Build long-format data
# ============================================================
wave1 = df[["SHEET", "NJ", "CHAIN", "CHAIN_NAME", "FTE"]].copy()
wave1.columns = ["id", "NJ", "CHAIN", "CHAIN_NAME", "FTE"]
wave1["POST"] = 0

wave2 = df[["SHEET", "NJ", "CHAIN", "CHAIN_NAME", "FTE2"]].copy()
wave2.columns = ["id", "NJ", "CHAIN", "CHAIN_NAME", "FTE"]
wave2["POST"] = 1

long_df = pd.concat([wave1, wave2], ignore_index=True).dropna(subset=["FTE"])
long_df["NJ_POST"] = long_df["NJ"] * long_df["POST"]

# ============================================================
# Full-sample DID (baseline)
# ============================================================
baseline = smf.ols("FTE ~ NJ + POST + NJ_POST", data=long_df).fit()
baseline_did = baseline.params["NJ_POST"]

print("=" * 60)
print("Baseline DID (full sample)")
print("=" * 60)
print(f"DID estimate: {baseline_did:.3f}")
print(f"Std. Error  : {baseline.bse['NJ_POST']:.3f}")
print(f"P-value     : {baseline.pvalues['NJ_POST']:.3f}")

# ============================================================
# Chain-by-chain DID
# ============================================================
results = []

for chain_code, chain_name in chain_labels.items():
    sub = long_df[long_df["CHAIN"] == chain_code].copy()
    n_obs = len(sub)
    n_restaurants = sub["id"].nunique()

    if n_obs < 10 or sub["NJ"].nunique() < 2:
        print(f"\nSkipping {chain_name}: insufficient variation.")
        continue

    model = smf.ols("FTE ~ NJ + POST + NJ_POST", data=sub).fit()
    did = model.params["NJ_POST"]
    se = model.bse["NJ_POST"]
    pval = model.pvalues["NJ_POST"]

    results.append({
        "Chain": chain_name,
        "N_obs": n_obs,
        "N_restaurants": n_restaurants,
        "DID_coefficient": did,
        "Std_Error": se,
        "P_value": pval,
        "Significant_5pct": pval < 0.05
    })

    print("\n" + "=" * 60)
    print(f"DID for {chain_name} (N = {n_obs})")
    print("=" * 60)
    print(f"DID estimate: {did:.3f}")
    print(f"Std. Error  : {se:.3f}")
    print(f"P-value     : {pval:.3f}")

results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(TABLE_DIR, "extension_chain.csv"), index=False)

print("\n" + "=" * 60)
print("Summary: DID by chain")
print("=" * 60)
print(results_df)

# ============================================================
# Plot: DID by chain vs. baseline
# ============================================================
fig, ax = plt.subplots(figsize=(9, 6))

x = np.arange(len(results_df))
ax.bar(x, results_df["DID_coefficient"], yerr=1.96 * results_df["Std_Error"],
       capsize=6, color="steelblue", alpha=0.8, label="Chain-specific DID (95% CI)")

ax.axhline(baseline_did, color="red", linestyle="--", linewidth=2,
           label=f"Full-sample DID = {baseline_did:.2f}")
ax.axhline(0, color="black", linewidth=1)

ax.set_xticks(x)
ax.set_xticklabels(results_df["Chain"], rotation=15)
ax.set_ylabel("DID Estimate (FTE Employment)", fontsize=12)
ax.set_title("Independent Extension: Heterogeneous Minimum-Wage Effects by Chain",
             fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURE_DIR, "extension_chain.png"), dpi=300)
plt.show()

print(f"\nExtension table saved to {TABLE_DIR}/extension_chain.csv")
print(f"Extension figure saved to {FIGURE_DIR}/extension_chain.png")