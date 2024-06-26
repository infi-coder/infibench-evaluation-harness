
import pandas as pd
def f(df, s):
    df = df.set_index('instrument_token')
    a = df.loc[s, 'tradingsymbol']
    return a


df1 = pd.DataFrame({'instrument_token': ['12295682', '12295683', 'asd'],
                   'tradingsymbol': ['ABC', 'DEF', 'GHI'],
                   'lot_size': [100, 200, 300]})
s11 = 'asd'
s12 = '12295682'

df2 = pd.DataFrame({'instrument_token': ['234', 'sdf', 'asd', '2341', 'sdf1', 'a1sd'],
                    'tradingsymbol': ['ABC', 'DEF', 'GHI', 'aa', '31', '311'],
                    'lot_size': [100, 200, 300, 1, 2, 3]})
s21 = '2341'
s22 = 'a1sd'

assert f(df1, s11) == extractCellValue(df1, s11)
assert f(df1, s12) == extractCellValue(df1, s12)
assert f(df2, s21) == extractCellValue(df2, s21)
assert f(df2, s22) == extractCellValue(df2, s22)
