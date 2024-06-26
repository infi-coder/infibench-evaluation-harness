"""
    Dump case data to recover the original test suite and all its cases
    Example usage:
        python3 bigcode_eval/infibench/adaptors/whole_suite_unpacker.py bigcode_eval/infibench/suite_v2.1.yaml bigcode_eval/infibench/batched_cases/suite_v2.1_data.csv bigcode_eval/infibench/cases
"""


import os
import os.path as osp
import argparse
import yaml
import json
import pandas as pd

def create_file(dir_path, file_path, text):
    if not osp.exists(osp.dirname(osp.join(dir_path, file_path))):
        os.makedirs(osp.dirname(osp.join(dir_path, file_path)))
    with open(osp.join(dir_path, file_path), 'w') as f:
        f.write(text)
    print(f'Write to', osp.join(dir_path, file_path))

parser = argparse.ArgumentParser()
parser.add_argument('suite_path', type=str, help='Suite yaml file path')
parser.add_argument('suite_data_path', type=str, help='Suite data csv file')
parser.add_argument('output_dir', type=str, help='The root dir to dump')
if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.suite_path, 'r') as f:
        suite_data = yaml.load(f, yaml.Loader)
    case_paths = suite_data['cases']
    suite_data_df = pd.read_csv(args.suite_data_path)
    suite_data = {}
    for i, row in suite_data_df.iterrows():
        suite_data[row['case_path']] = {
            'prompt': row['prompt'],
            'eval_spec': yaml.safe_load(row['eval_spec']),
            'eval_spec_raw': row['eval_spec'],
            'dependencies': json.loads(row['dependencies'])
        }

    for i, case_path in enumerate(case_paths):
        print(f'Dump No. #{i}')
        case_data = suite_data[case_path]
        case_rootdir = osp.join(args.output_dir, osp.dirname(case_path))
        # for prompt
        create_file(case_rootdir, case_data['eval_spec']['prompt_path'], case_data['prompt'])
        # for eval spec
        create_file(case_rootdir, osp.basename(case_path), case_data['eval_spec_raw'])
        # for dependendies
        for k, v in case_data['dependencies'].items():
            create_file(case_rootdir, k, v)
    
    print('Done')