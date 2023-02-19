# %%[markdown]
"""
Writes bodyweights for each subject to csv
"""
# %%
import pandas as pd
from pathlib import Path
# %%
BW = [
    95.3,
    62,
    77.24,
    70.5,
    91.03,
    87.8,
    81.47,
    75.9,
    81.4,
    87.9,
    82.6,
    82.6,
    74.5,
    63.09,
    65,
    63.7,
    96.02,
    60.7,
    73.3,
    66.2,
    93.9,
    93.6,
    67.99,
]
dfBW = pd.DataFrame([range(1, len(BW)+1), BW]).transpose()
dfBW.to_csv(Path('../../data/external/bodyweight.csv'))