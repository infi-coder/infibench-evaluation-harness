import argparse
import os
import os.path as osp
import yaml
import random

parser = argparse.ArgumentParser()
parser.add_argument('metric_type', type=str, choices=['keywords', 'unit_test', 'blank_filling', 'similarity'])
parser.add_argument('--suite_path', type=str, default='suite_v2.0.0.yaml')
if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.suite_path, 'r') as f:
        cases = yaml.load(f, yaml.Loader)['cases']
    case_list = dict(zip(['keywords', 'unit_test', 'blank_filling', 'similarity'], [[],[],[],[]]))
    for case_path in cases:
        with open(case_path, 'r') as f:
            case_data = yaml.load(f, yaml.Loader)
            for field in case_data['grading']:
                if field in case_list:
                    case_list[field].append(case_path)
                if field == 'customized':
                    case_list[case_data['grading'][field]['real_metric_type']].append(case_path)
    for key in case_list:
        print(key, len(case_list[key]))
    selected = random.sample(case_list[args.metric_type], k=1)
    print(selected)
    print('=' * 10)
    with open(selected[0], 'r') as f:
        case_data = f.read()
        print(case_data)
    print('=' * 10)
    with open(selected[0], 'r') as f:
        prompt_path = yaml.load(f, yaml.Loader)['prompt_path']
        with open('cases/' + prompt_path, 'r') as ff:
            print(ff.read())
    print('=' * 10)