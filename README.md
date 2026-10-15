# Card & Krueger (1994) Minimum Wage and Employment — Replication Project

## Project Overview
This project replicates Card & Krueger (1994), which studies the employment
effects of New Jersey's minimum wage increase on the fast-food industry.

## Data Source
- Raw data: `data/raw/public.csv` (publicly available from Princeton University)
- Data dictionary: see `01_DID/DATA_DICTIONARY.md`

## Project Structure
ECO6067_Project/
├── data/
│   └── raw/ #raw data
│   └── processed/ #cleaned analysis data
├── code/ # Analysis code
│   ├── run_all.py
│   ├── 01_clean_data.py
│   ├── 02_replicate_tables.py
│   └── 03_replicate_figure.py
│   └── 04_extension_chain.py
├── outputs/ # Output results
│   ├── tables/
│   └── figures/
├── requirements.txt # Dependencies
└── README.md
├── report.pdf
└── AI_USE_DISCLOSURE.md

## How to Reproduce
1. Install dependencies: `pip install -r requirements.txt`
2. Place `public.csv` in `data/raw/`.
3. Run: `python code/run_all.py`
4. All tables and figures will be saved to `outputs/`.

## Main Results
- Table 2: Average FTE employment by group and wave
- Table 3: DID regression results
- Table 4: Robustness checks
- Figure 1: Employment changes in NJ vs PA

## Independent Extension

### Research Question
Did the employment effect of New Jersey's minimum wage increase differ
across fast-food chains?

### Motivation
Card & Krueger (1994) report a single, pooled difference-in-differences
(DID) estimate. However, fast-food chains differ substantially in pricing
power, profit margins, and labor-management practices. A pooled estimate
may therefore hide important heterogeneity across chains. This extension
asks whether the minimum-wage effect is homogeneous or chain-specific.

### Empirical Design
I estimate a separate DID regression for each of the four chains in the
data (Burger King, KFC, Roy Rogers, Wendy's):

    FTE = β0 + β1 * NJ + β2 * POST + β3 * (NJ × POST) + ε

where β3 is the chain-specific DID estimate. I compare each chain-specific
estimate with the pooled baseline DID estimate.

### Results

| Chain        | N (obs) | DID coefficient | Std. Error | P-value |
|--------------|---------|-----------------|------------|---------|
| Burger King  | 330     | +4.66           | 2.34       | 0.047   |
| KFC          | 159     | -1.29           | 2.23       | 0.562   |
| Roy Rogers   | 193     | +2.54           | 3.48       | 0.467   |
| Wendy's      | 112     | +3.34           | 3.84       | 0.385   |
| **Pooled**   | **794** | **+2.77**       | **1.65**   | **0.094** |

### Interpretation
- The pooled DID estimate is +2.77 (p = 0.094), consistent with the
  original paper: no evidence of an employment decline in New Jersey.
- Burger King shows a statistically significant positive DID (+4.66,
  p = 0.047), suggesting that the state's largest chain expanded employment
  relative to its Pennsylvania counterparts.
- KFC is the only chain with a negative DID (-1.29), but the estimate is
  far from statistically significant (p = 0.562), so there is no evidence
  of a KFC-specific employment decline.
- Roy Rogers and Wendy's show positive but imprecise estimates, consistent
  with small sample sizes (99 and 60 restaurants respectively).

### Conclusion
The employment effect of the minimum-wage increase is heterogeneous across
chains, but no chain shows a statistically significant employment decline.
The strongest evidence is a positive employment response at Burger King.
This reinforces Card & Krueger's main conclusion while adding a chain-level
dimension that the original paper does not explore.

### Output Files
- `outputs/tables/extension_chain.csv`
- `outputs/figures/extension_chain.png`

## AI-Use Disclosure

### Where and how AI was used
- AI was used to help design the data-cleaning pipeline, including the
  construction of the Full-Time Equivalent (FTE) employment measure.
- AI was used to draft the DID regression code and the chain-level
  heterogeneity extension.
- AI was used to help write and structure this README.

### How AI outputs were checked
- All variable definitions were verified against the public data dictionary
  and the original Card & Krueger (1994) paper.
- The DID regression results were checked for internal consistency: the
  chain-level DID estimates, when weighted by sample size, are consistent
  with the pooled DID estimate.
- The Figure 1 output was visually inspected to confirm that the New Jersey
  and Pennsylvania employment paths match the pattern in the original paper.

### AI errors or suggestions that were corrected or rejected
- The initial AI-generated cleaning script treated blank cells as zeros
  rather than missing values. This was corrected before running the
  regressions, because zero employment is not economically meaningful in
  this context.
- An early AI suggestion to include starting wage as a control in the
  baseline specification was rejected: starting wage is highly correlated
  with treatment status (NJ vs PA), so including it absorbs part of the
  treatment effect. It is instead reported only in the robustness checks.