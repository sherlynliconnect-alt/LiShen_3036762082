# AI-Use Disclosure

## Overview
This document describes how AI tools were used at each stage of the project,
how AI outputs were verified, and which AI suggestions were rejected or
corrected.

## 1. Project Planning and Literature Understanding
- **How AI was used:** AI was used to summarize Card & Krueger (1994),
  clarify the difference-in-differences identification strategy, and
  outline the replication workflow.
- **How it was checked:** Key claims were verified against the original
  paper and the public data dictionary.
- **Errors corrected:** Initial AI summaries overstated the precision of
  the original results. The final report reflects the correct statistical
  language (10% significance level, not 5%).

## 2. Data Cleaning and Variable Construction
- **How AI was used:** AI helped draft the cleaning script and the
  construction of the Full-Time Equivalent (FTE) measure.
- **How it was checked:** All variable definitions were verified against
  the original paper and the data dictionary.
- **Errors corrected:** The initial AI draft treated blank cells as zeros.
  This was corrected to missing values (`NaN`) before running any regressions.

## 3. Empirical Analysis
- **How AI was used:** AI helped write the DID regression code and the
  chain-level extension.
- **How it was checked:** Regression outputs were compared with the raw
  differences in means from Table 2, and chain-level estimates were
  checked for consistency with the pooled estimate.
- **Suggestions rejected:** An early AI suggestion to include starting
  wage as a control in the baseline specification was rejected because
  starting wage is highly correlated with treatment status.

## 4. Writing and Reporting
- **How AI was used:** AI helped structure the report, improve clarity,
  and format tables.
- **How it was checked:** All numerical claims were verified against the
  actual regression outputs.
- **Errors corrected:** AI occasionally generated placeholder numbers
  that did not match the results; these were replaced with the actual
  estimates.

## 5. Reproducibility
- **How AI was used:** AI helped design the repository structure and the
  `run_all.py` entry point.
- **How it was checked:** The full pipeline was run from a clean state to
  confirm that `python code/run_all.py` reproduces all tables and figures.

## Summary
AI was used as a productivity tool throughout the project, but every
substantive decision — data cleaning, variable construction, regression
specification, robustness checks, and interpretation — was reviewed and
verified by the author.