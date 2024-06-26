import os
import os.path as osp
import yaml
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('--suite_path', type=str, default='suite_v2.0.0.yaml')
parser.add_argument('--result_yaml_path', type=str, default='results/suite_v2.0.0_gpt-4_0.2_0.9_30_suite_v2.0.0.yaml')
if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.result_yaml_path, 'r') as f:
        result_data = yaml.load(f, yaml.Loader)
    bad_cases = {}
    for k in result_data:
        if result_data[k]['now_score'] <= 1e-6:
            with open(k, 'r') as f:
                case_script = (f.read())
            with open(k, 'r') as f:
                prompt_path = yaml.load(f, yaml.Loader)['prompt_path']
            with open('cases/' + prompt_path, 'r') as f:
                case_prompt = (f.read())
            bad_cases[k] = (case_script, case_prompt)
    print(len(bad_cases))

    bad_case_lst = list(bad_cases.keys())
    selected = random.sample(bad_case_lst, k=1)[0]
    print(selected)
    print('*' * 10)
    print(bad_cases[selected][0])
    print('+' * 10)
    print(bad_cases[selected][1])
