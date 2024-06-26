
import pandas as pd
def f():
    new_list = [["first", "second"], ["third", "four"], ["five", "six"]]
    df = pd.DataFrame(new_list)
    writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()

writeExcel()

import os
assert os.path.exists("data.xlsx")
assert pd.read_excel("data.xlsx", header=None).values.tolist() == [["first", "second"], ["third", "fourth"]]