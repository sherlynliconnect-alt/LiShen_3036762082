# Reusable Skill: Replicating Card & Krueger (1994)

## Purpose
This skill documents the reusable workflow for replicating the minimum-wage
employment analysis in Card & Krueger (1994), including the DID regression
and the chain-level heterogeneity extension.

## Inputs
- `data/raw/public.csv` — raw restaurant-level survey data (not committed
  to the repository; see `data/raw/README.md` for access instructions).

## Outputs
- `data/processed/cleaned_data.csv` — cleaned analysis sample.
- `outputs/tables/table2.csv` — average FTE by group and wave.
- `outputs/tables/table3.csv` — DID regression results.
- `outputs/tables/table4.csv` — robustness checks.
- `outputs/tables/extension_chain.csv` — chain-level DID results.
- `outputs/figures/figure1.png` — NJ vs PA employment paths.
- `outputs/figures/extension_chain.png` — chain-level DID bar chart.

## How to Run
From the project root:

    python code/run_all.py

## Key Steps
1. **Data cleaning** (`code/01_clean_data.py`):
   - Replace blanks with NaN.
   - Convert numeric columns.
   - Construct FTE = EMPFT + 0.5 * EMPPT + 0.5 * NMGRS.
   - Construct NJ and POST dummies.

2. **Core replication** (`code/02_replicate_tables.py`):
   - Build a long-format panel.
   - Estimate DID: FTE ~ NJ + POST + NJ*POST.
   - Save Tables 2, 3, and 4.

3. **Core figure** (`code/03_replicate_figure.py`):
   - Plot average FTE by group and wave.
   - Annotate with the DID estimate.

4. **Extension** (`code/04_extension_chain.py`):
   - Estimate chain-specific DID regressions.
   - Plot chain-level DID estimates with 95% confidence intervals.

## Notes
- The DID identifying assumption is parallel trends between New Jersey
  and eastern Pennsylvania.
- The extension is descriptive; chain-level sample sizes are small for
  some chains.