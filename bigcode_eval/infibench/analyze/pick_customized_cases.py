import argparse
import os
import os.path as osp
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('--suite_path', type=str, default='suite_v2.0.0.yaml')
if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.suite_path, 'r') as f:
        cases = yaml.load(f, yaml.Loader)['cases']
    for case_path in cases:
        with open(case_path, 'r') as f:
            case_data = yaml.load(f, yaml.Loader)
        if 'customized' in case_data['grading']:
            print(case_path)
