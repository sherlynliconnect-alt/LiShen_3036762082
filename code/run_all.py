"""
run_all.py
Run the entire replication pipeline end-to-end.

Usage:
    python code/run_all.py

This script runs, in order:
    1. Data cleaning and variable construction
    2. Core replication tables (Tables 2-4)
    3. Core replication figure (Figure 1)
    4. Independent extension (chain-level heterogeneity)

After running, all outputs will be saved to:
    - outputs/tables/
    - outputs/figures/
    - data/processed/
"""

import subprocess
import sys
import os

# Ensure we run from the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)

scripts = [
    "code/01_clean_data.py",
    "code/02_replicate_tables.py",
    "code/03_replicate_figure.py",
    "code/04_extension_chain.py",
]

for script in scripts:
    print(f"\n{'=' * 60}")
    print(f"Running: {script}")
    print("=" * 60)
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"\nERROR: {script} failed.")
        sys.exit(1)

print("\nAll scripts completed successfully.")
print("Outputs saved to outputs/tables/ and outputs/figures/.")