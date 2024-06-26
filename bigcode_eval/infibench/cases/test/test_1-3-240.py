def f(df1, df2):
    return df1[~df1.apply(tuple,1).isin(df2.apply(tuple,1))]

import pandas as pd
df1 = pd.DataFrame({'a':[1,2,3,4,5, 8, 8], 'b':[1,2,3,4,5, 6, 7]})
df2 = pd.DataFrame({'a':[1,2,3], 'b':[1,2,3]})

from copy import deepcopy

assert all(f(deepcopy(df1), deepcopy(df2)) == getDifference(deepcopy(df1), deepcopy(df2)))