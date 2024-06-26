
def f(df):
    return df.loc[df.groupby('A').B.idxmin()]

import pandas as pd
import numpy as np
df = pd.DataFrame({'A': [1, 2, 2, 1, 3, 3],
                   'B': [1, 2, 3, 4, 5, 6],
                   'C': [2, 4, 6, 8, 10, 12]})
from copy import deepcopy

assert all(getMin(deepcopy(df)) == f(deepcopy(df)))