import os
import os.path as osp
import pandas as pd
import json
import yaml
import numpy as np

in_csv = 'bigcode_eval/infibench/analyze/tables_and_plots/main.csv'
out_yaml = 'bigcode_eval/infibench/analyze/tables_and_plots/leaderboard.yaml'

if __name__ == '__main__':
    in_data = pd.read_csv(in_csv)

    data = []
    columns = list(in_data.columns)
    for i, item in in_data.iterrows():
        dict_item = {key: item[key] for key in columns if key != 'Unnamed: 0'}
        data.append(dict_item)
    data = [row for row in data if isinstance(row['no'], str) and row['no'].isdigit()]
    # Sort by the main score
    data = sorted(data, key=lambda x: float(x['Overall Score_score'].replace('%', '')), reverse=True)
    print(len(data))

    records = []
    s = 0
    for i, item in enumerate(data):
        if item['eval_type'] not in ['Ablation', 'Human']:
            now_entry = {
                'title': item['model_family'] + '/' + item['print_name'],
                'locked': (item['eval_type'] == 'Closed'),
                'size': item['model_params'],
                'score': item['Overall Score_score'],
                'score_std': item['Overall Score_std'] if item['Overall Score_std'] != '0.00%' else '',
                'ctx_length': item['ctx_length'],
                'modeltype': item['type'],
                'modeldomain': item['domain'],
                'link': None,
                'comment': None,
                'rank': s+1
            }
            # for field in ['score', 'score_std', 'devscore', 'devscore_std', 'testscore', 'testscore_std']:
            #     if now_entry[field]:
            #         # format to percentage
            #         now_entry[field] = f'{now_entry[field] * 100.:.2f}%'
            records.append(now_entry)
            s += 1
    ans = {'settings': 'main', 'records': records}
    with open(out_yaml, 'w') as f:
        yaml.dump(ans, f)
    print('Dumped to', out_yaml)
