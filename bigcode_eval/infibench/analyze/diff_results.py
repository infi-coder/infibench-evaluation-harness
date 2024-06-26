import os
import os.path as osp
import argparse
import yaml
import json

parser = argparse.ArgumentParser()
parser.add_argument('res_a', type=str)
parser.add_argument('res_b', type=str)
parser.add_argument('--suite_path', type=str, default='suite_v2.0.0.yaml')
if __name__ == '__main__':
    args = parser.parse_args()
    res_a = args.res_a
    res_b = args.res_b
    assert res_a.endswith('.yaml') and res_b.endswith('.yaml')
    with open(res_a, 'r') as f:
        result_a = yaml.load(f, yaml.Loader)
    with open(res_b, 'r') as f:
        result_b = yaml.load(f, yaml.Loader)
    with open(args.suite_path, 'r') as f:
        suites = yaml.load(f, yaml.Loader)
    # loading prompt path
    prompts_paths = {}
    langs = {}
    for case in suites['cases']:
        with open(case, 'r') as f:
            now_case_file = yaml.load(f, yaml.Loader)
        prompts_paths[case] = now_case_file['prompt_path']
        langs[case] = now_case_file['lang']
    # loading a b scores
    a_scores = {}
    b_scores = {}
    for case, item in result_a.items():
        a_scores[case] = item['now_score']
    for case, item in result_b.items():
        b_scores[case] = item['now_score']
    # count a and b
    a_better_b = {}
    b_better_a = {}
    for case in prompts_paths:
        if a_scores[case] >= 1.0 and b_scores[case] <= 0.1:
            a_better_b[case] = f"{('cases/' + prompts_paths[case], langs[case], a_scores[case], b_scores[case])}"
        if b_scores[case] >= 1.0 and a_scores[case] <= 0.1:
            b_better_a[case] = f"{('cases/' + prompts_paths[case], langs[case], a_scores[case], b_scores[case])}"
    print(f'a > b (# {len(a_better_b)}):', json.dumps(a_better_b, indent=2))
    print('')
    print(f'b > a (# {len(b_better_a)}):', json.dumps(b_better_a, indent=2))
