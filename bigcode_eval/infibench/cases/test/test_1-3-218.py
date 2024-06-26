
import re
def f(df):
    df['LGA'] = [re.sub("[\(\[].*?[\)\]]", "", x).strip() for x in df['LGA']]
    # delete anything between brackets
    return df

import pandas as pd
df = pd.DataFrame({'LGA': ['Alpine (S)',
                           'Ararat (RC)',
                           'Ballarat (C)',
                           'Banyule (C)',
                           'Bass Coast (S)',
                           'Baw Baw (S)',
                           'Bayside (C)',
                           'Benalla (RC)',
                           'Boroondara (C)',
                           'Brimbank (C)',
                           'AXX (RC)',
                           'BYY (C)',
                           'CIUHGWU (S)']})
from copy import deepcopy

assert remove(deepcopy(df)).equals(f(df))