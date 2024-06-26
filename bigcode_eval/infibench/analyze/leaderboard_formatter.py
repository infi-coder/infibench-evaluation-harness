import os
import os.path as osp
import json
import yaml
import numpy as np

in_json = 'results/main_results.json'
out_yaml = 'results/leaderboard.yaml'

if __name__ == '__main__':
    with open(in_json, 'r') as f:
        in_data = json.load(f)
    in_data = sorted(in_data, key=lambda x: x[5], reverse=True)
    records = []
    for i, item in enumerate(in_data):
        now_entry = {
            'title': item[1],
            'size': item[2],
            'score': item[5],
            'score_std': float(np.std(item[4])) if len(item[4]) > 1 else None,
            'devscore': item[7],
            'devscore_std': float(np.std(item[6])) if len(item[6]) > 1 else None,
            'testscore': item[9],
            'testscore_std': float(np.std(item[8])) if len(item[8]) > 1 else None,
            'link': None,
            'comment': None,
            'rank': i+1
        }
        for field in ['score', 'score_std', 'devscore', 'devscore_std', 'testscore', 'testscore_std']:
            if now_entry[field]:
                # format to percentage
                now_entry[field] = f'{now_entry[field] * 100.:.2f}%'
        records.append(now_entry)
    ans = {'settings': 'main', 'records': records}
    with open(out_yaml, 'w') as f:
        yaml.dump(ans, f)
    print('Dumped to', out_yaml)