import argparse
import os
import os.path as osp
import yaml

final_dict = {}

parser = argparse.ArgumentParser()
parser.add_argument('--suite_path', type=str, default='suite_v2.0.0.yaml')
if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.suite_path, 'r') as f:
        cases = yaml.load(f, yaml.Loader)['cases']
    for case_path in cases:
        with open(case_path, 'r') as f:
            case_data = yaml.load(f, yaml.Loader)
        metric_types = []
        for k in case_data['grading']:
            if k ==  'customized':
                metric_types.append(case_data['grading']['customized'].get('real_metric_type', 'customized'))
            else:
                metric_types.append(k)
        metric_types = list(set(metric_types))
        for m in metric_types:
            if m not in final_dict:
                final_dict[m] = 0
            final_dict[m] += 1
    for m in final_dict:
        print(m, final_dict[m], f'{final_dict[m] / 270. * 100.:.2f}%')

