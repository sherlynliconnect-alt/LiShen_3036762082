# Minimum Wages and Employment: A Replication and Extension of Card & Krueger (1994)

Course: ECON6067 — Empirical Project
Author: Li Shen
Date:  2026/10/12

---

## 1. Research Question and Motivation

### 1.1 The Original Paper

Card and Krueger (1994) study the employment effect of New Jersey's minimum
wage increase on April 1, 1992, which raised the state minimum wage from
$4.25 to $5.05 per hour. Using eastern Pennsylvania as a comparison group —
where the minimum wage remained at $4.25 — they exploit a natural experiment
and apply a difference-in-differences (DID) design to a sample of 410
fast-food restaurants (Burger King, KFC, Roy Rogers, and Wendy's) surveyed
before (February–March 1992) and after (November–December 1992) the policy
change.

The central research question is:

> Did the minimum-wage increase reduce employment in New Jersey's fast-food
> industry relative to Pennsylvania?

Standard economic theory predicts that a binding minimum-wage increase
should reduce employment. Card and Krueger, however, find no evidence of an
employment decline: employment in New Jersey actually rose slightly relative
to Pennsylvania. This result challenged the conventional view and became a
foundational contribution to the empirical minimum-wage literature.

### 1.2 Motivation for Replication

Replicating this paper is valuable for three reasons. First, the data are
publicly available and well documented, making full replication feasible.
Second, the DID design is simple, transparent, and widely used in policy
evaluation. Third, the paper's conclusions are economically important and
have been the subject of extensive debate, so independent verification is
worthwhile.

### 1.3 Contribution of This Project

This project has two components:

1. **Core replication.** I reconstruct the analysis sample and reproduce
   Tables 2–4 and Figure 1 of the original paper.
2. **Independent extension.** I estimate chain-specific DID regressions to
   test whether the employment effect is homogeneous across the four
   fast-food chains in the sample.

---

## 2. Data Sources, Sample Construction, and Variable Definitions

### 2.1 Data Source

The data come from the publicly available replication package associated
with Card and Krueger (1994), distributed by Princeton University. The file
`public.csv` contains 410 restaurant-level observations, with separate
columns for the pre-increase survey (Wave 1) and the post-increase survey
(Wave 2).

### 2.2 Sample

The sample consists of 410 fast-food restaurants in two regions:

- **Treatment group:** New Jersey (331 restaurants).
- **Comparison group:** Eastern Pennsylvania (79 restaurants).

The restaurant chains represented are Burger King, KFC, Roy Rogers, and
Wendy's.

### 2.3 Variable Definitions

The key variables used in the analysis are:

| Variable | Definition |
|----------|------------|
| `STATE` | 1 if the restaurant is in New Jersey, 0 if in Pennsylvania |
| `NJ` | Treatment dummy, equal to 1 if the restaurant is in New Jersey |
| `CHAIN` | Chain identifier (1 = Burger King, 2 = KFC, 3 = Roy Rogers, 4 = Wendy's) |
| `EMPFT` | Number of full-time employees (Wave 1) |
| `EMPPT` | Number of part-time employees (Wave 1) |
| `NMGRS` | Number of managers (Wave 1) |
| `FTE` | Full-Time Equivalent employment in Wave 1: `EMPFT + 0.5 * EMPPT + 0.5 * NMGRS` |
| `FTE2` | Full-Time Equivalent employment in Wave 2, constructed analogously |
| `WAGE_ST` | Starting wage (Wave 1) |
| `WAGE_ST2` | Starting wage (Wave 2) |
| `POST` | Time dummy, equal to 1 for Wave 2 observations |

### 2.4 Data Cleaning

The following cleaning steps were applied:

1. Blank strings and whitespace-only entries were converted to missing
   values (`NaN`) to avoid treating non-responses as zeros.
2. All numeric variables were converted to numeric types.
3. The FTE measure was constructed as in Card and Krueger (1994):
   full-time employees count fully, part-time employees and managers count
   as half a full-time worker.
4. A long-format panel was constructed by stacking Wave 1 and Wave 2
   observations, with a `POST` indicator distinguishing the two periods.
5. Observations with missing FTE were dropped from the regression sample.

After cleaning, the analysis sample contains 398 restaurants in Wave 1 and
396 in Wave 2, for a total of 794 restaurant-wave observations.

---

## 3. Empirical Design

### 3.1 Difference-in-Differences Specification

The core empirical design is a standard 2×2 difference-in-differences
regression:

    FTE_i = β0 + β1 * NJ_i + β2 * POST_i + β3 * (NJ_i × POST_i) + ε_i

where:

- `FTE_i` is full-time equivalent employment for restaurant i in a given wave.
- `NJ_i` is a treatment-group dummy (1 = New Jersey, 0 = Pennsylvania).
- `POST_i` is a time dummy (1 = Wave 2, 0 = Wave 1).
- `NJ_i × POST_i` is the interaction term whose coefficient β3 is the DID
  estimate.

The coefficient β3 captures the average change in employment in New Jersey
relative to the change in Pennsylvania, which is the causal parameter of
interest.

### 3.2 Identifying Assumption

The DID design assumes that, absent the minimum-wage increase, employment
in New Jersey and Pennsylvania would have followed parallel trends. Card
and Krueger justify this assumption by the geographic proximity of the two
regions, their shared labor-market conditions, and their similar industrial
composition.

---

## 4. Core Replication Results

### 4.1 Average Employment (Table 2)

Table 2 reports average FTE employment by group and wave:

| Group         | Wave          | Mean FTE | Std. Dev. | N   |
|---------------|---------------|----------|-----------|-----|
| Pennsylvania  | Wave 1 (Pre)  | 21.56    | 11.75     | 77  |
| Pennsylvania  | Wave 2 (Post) | 19.35    | 8.07      | 77  |
| New Jersey    | Wave 1 (Pre)  | 18.74    | 8.90      | 321 |
| New Jersey    | Wave 2 (Post) | 19.30    | 9.03      | 319 |

Two observations stand out. First, average employment in Pennsylvania fell
by about 2.2 workers, while in New Jersey it rose slightly by about 0.6
workers. Second, the raw DID — computed as the change in New Jersey minus
the change in Pennsylvania — is approximately +2.77, implying that New
Jersey's employment did not decline relative to Pennsylvania.

### 4.2 DID Regression (Table 3)

The DID regression produces the following estimates:

| Variable         | Coefficient | Std. Error | t-stat | P-value |
|------------------|-------------|------------|--------|---------|
| Intercept        | 21.558      | 1.047      | 20.58  | 0.000   |
| NJ               | -2.817      | 1.166      | -2.42  | 0.016   |
| POST             | -2.205      | 1.481      | -1.49  | 0.137   |
| NJ × POST (DID)  | **+2.767**  | **1.650**  | **1.68** | **0.094** |

The DID estimate is +2.77 (standard error 1.65), statistically significant
at the 10% level (p = 0.094). This result is consistent with Card and
Krueger's main finding: there is no evidence that New Jersey's minimum-wage
increase reduced employment relative to Pennsylvania.

### 4.3 Robustness Checks (Table 4)

I re-estimate the DID specification under three alternative specifications:

| Specification        | DID Coefficient | Std. Error | P-value |
|----------------------|-----------------|------------|---------|
| Full-time only       | +3.36           | 1.48       | 0.023   |
| With chain FE        | +2.82           | 1.49       | 0.059   |
| With wage control    | +1.83           | 1.77       | 0.303   |

The first two specifications confirm the baseline result: the DID estimate
remains positive and statistically significant. In the third specification,
adding the starting wage as a control reduces the DID coefficient to +1.83
and renders it insignificant. This is expected: starting wage is strongly
correlated with treatment status, so controlling for it absorbs part of the
treatment effect. The result should therefore be interpreted as a
diagnostic rather than as evidence against the baseline finding.

### 4.4 Employment Paths (Figure 1)

Figure 1 plots the average FTE employment for New Jersey and Pennsylvania
across the two waves. The Pennsylvania line declines, while the New Jersey
line is roughly flat to slightly increasing. The visual pattern reinforces
the DID estimate: New Jersey employment did not fall relative to
Pennsylvania.

### 4.5 Comparison with the Original Paper

The replication results are qualitatively consistent with Card and Krueger
(1994):

- The sign of the DID estimate is positive in both the original paper and
  this replication.
- The magnitude is economically small, consistent with the original claim
  that the minimum-wage increase did not cause a measurable employment
  decline.
- Minor numerical differences reflect differences in sample construction
  and in the treatment of missing values. For example, my final sample
  contains 794 restaurant-wave observations, whereas the original paper
  reports somewhat different counts depending on the table.

Overall, the core replication supports the original paper's central
conclusion.

---

## 5. Independent Extension

### 5.1 Research Question

Did the employment effect of New Jersey's minimum-wage increase differ
across fast-food chains?

### 5.2 Motivation

The original paper reports a single pooled DID estimate. However, chains
differ in pricing power, profit margins, and workforce composition. A
pooled estimate may hide important heterogeneity across chains. If the
minimum wage mainly affects low-margin firms, negative employment effects
should be concentrated in specific chains.

### 5.3 Empirical Design

For each chain c, I estimate a separate DID regression:

    FTE_i = β0 + β1 * NJ_i + β2 * POST_i + β3 * (NJ_i × POST_i) + ε_i

The coefficient β3 is the chain-specific DID estimate. I compare it with
the pooled baseline DID estimate.

### 5.4 Results

| Chain         | N (obs) | DID coefficient | Std. Error | P-value |
|---------------|---------|-----------------|------------|---------|
| Burger King   | 330     | +4.66           | 2.34       | 0.047   |
| KFC           | 159     | -1.29           | 2.23       | 0.562   |
| Roy Rogers    | 193     | +2.54           | 3.48       | 0.467   |
| Wendy's       | 112     | +3.34           | 3.84       | 0.385   |
| **Pooled**    | **794** | **+2.77**       | **1.65**   | **0.094** |

### 5.5 Interpretation

The pooled DID estimate is +2.77 (p = 0.094), consistent with the original
paper. The chain-level analysis reveals meaningful heterogeneity:

- **Burger King** shows a statistically significant positive DID (+4.66,
  p = 0.047). The state's largest chain expanded employment relative to its
  Pennsylvania counterparts.
- **KFC** is the only chain with a negative point estimate (-1.29), but the
  estimate is far from statistically significant (p = 0.562). There is no
  statistical evidence of a KFC-specific employment decline.
- **Roy Rogers and Wendy's** show positive but imprecise estimates,
  consistent with their smaller sample sizes.

No chain shows a statistically significant employment decline. The
strongest evidence is a positive employment response at Burger King.

### 5.6 Limitations

- Chain-level sample sizes are small for some chains (Wendy's: 60
  restaurants; Roy Rogers: 99), so standard errors are wide.
- The analysis uses the same DID specification as the original paper;
  chain-level heterogeneity could also reflect regional differences within
  New Jersey and Pennsylvania.
- The data cover a single minimum-wage episode; external validity to other
  states or time periods is limited.

### 5.7 Conclusion of the Extension

The minimum-wage effect is heterogeneous across chains, but no chain shows
a statistically significant employment decline. The strongest evidence is
a positive employment response at Burger King. This reinforces the original
Card and Krueger conclusion while adding a chain-level perspective that the
original paper does not explore.

---

## 6. Validation, Limitations, and Conclusion

### 6.1 Validation

Three validation checks support the replication:

1. The DID estimate from the regression matches the raw difference in means
   computed from Table 2.
2. The chain-specific DID estimates, when weighted by sample size, are
   consistent with the pooled DID estimate.
3. The visual pattern in Figure 1 matches the numerical results.

### 6.2 Limitations

- **Sample size.** Some chains have small samples, which reduces precision.
- **Short panel.** The data cover only two waves, so dynamic effects cannot
  be studied.
- **External validity.** The results apply to a specific state and period;
  they do not necessarily generalize to other minimum-wage episodes.
- **Omitted variables.** The DID design does not control for local demand
  shocks that may differ between New Jersey and Pennsylvania.

### 6.3 Conclusion

This project replicates Card and Krueger (1994) using publicly available
data. The core DID estimate is +2.77 (p = 0.094), consistent with the
original finding that New Jersey's minimum-wage increase did not reduce
fast-food employment relative to Pennsylvania. The independent extension
shows that the employment effect varies across chains, with Burger King
exhibiting a statistically significant positive response, while no chain
shows a statistically significant decline.

The replication supports the original paper's central conclusion and adds
a new dimension — chain-level heterogeneity — that enriches the policy
interpretation without overturning the main result.

---

## References

Card, D., & Krueger, A. B. (1994). Minimum Wages and Employment: A Case
Study of the Fast-Food Industry in New Jersey and Pennsylvania. *American
Economic Review*, 84(4), 772–793.