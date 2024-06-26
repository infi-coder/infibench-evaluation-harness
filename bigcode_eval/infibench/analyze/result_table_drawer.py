import json
from matplotlib import pyplot as plt
import numpy as np

fname = 'results/main_results.json'

if __name__ == '__main__':
    with open(fname, 'r') as f:
        results = json.load(f)
    
    anses = {}
    seq_ans = ''

    for row in results:
        model_name = row[1]
        model_size = row[2] if row[2] else '/'
        model_mean = f'{np.mean(row[4]) * 100.:.2f}\%'
        model_var = f'{np.std(row[4]) * 100.:.2f}\%' if len(row[4]) > 1 else ''
        if model_var:
            ans = f'{model_name} & {model_size} & \witherr{{${model_mean}$}}{{${model_var}$}} &  \\\\ \n'
        else:
            ans = f'{model_name} & {model_size} & ${model_mean}$ & \\\\ \n'
        seq_ans += ans
        anses[model_mean] = ans
    
    means = sorted(list(anses.keys()), reverse=True)
    ans = ''
    for mean in means:
        ans += anses[mean]

    # print(ans)
    print(seq_ans)
    
