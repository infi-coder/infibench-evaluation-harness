import argparse
import os
import os.path as osp
import yaml
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('in_path', type=str)
parser.add_argument('out', type=str)
parser.add_argument('--bsz', type=int, default=10)
parser.add_argument('--devset', type=str, default=None)
if __name__ == '__main__':
    args = parser.parse_args()
    assert args.out.endswith('.txt')

    with open(args.in_path, 'r') as f:
        full_results = yaml.load(f, yaml.Loader)
    
    fields = ['keywords', 'blank_filling', 'unit_test', 'similarity', 'custom']
    tot_scores = []
    full_score = 0.
    full_dev_score = 0.
    full_test_score = 0.
    skip_cnt = 0

    bsz = args.bsz

    if args.devset:
        with open(args.devset, 'r') as f:
            dev_cases = yaml.load(f, yaml.Loader)['cases']
            dev_cases = [c.split('/')[-1] for c in dev_cases]
        print_items = []
        for k in full_results:
            if k.split('/')[-1] in dev_cases:
                print_items.append(k)
    else:
        print_items = list(full_results.keys())

    fout = open(args.out, 'w')
    
    for case_name, case_report in full_results.items():
        case_full_score = case_report['full_score']
        print(case_name)
        
        best_scores = []
        for s in range(0, len(case_report['detail']), bsz):
            # locate the instance with highest score
            best_score = 0.
            for response_report in case_report['detail'][s: s+bsz]:
                now_score = 0.
                for field in fields:
                    if field + '_score' in response_report:
                        now_score += response_report[field + '_score']
                if now_score >= best_score:
                    best_score = now_score
            best_scores.append(best_score)
        
        tot_case_score = 0.
        for field in fields:
            if field + '_score' in case_report['detail'][0]:
                tot_case_score += case_report['detail'][0][field + '_totscore']

        # overwrite max_score
        if 'max_score' in case_report['detail'][0]:
            tot_case_score = case_report['detail'][0]['max_score']
        best_scores = [min(score, tot_case_score) / tot_case_score for score in best_scores]
        # print(case_name)
        assert np.mean(best_scores) == case_report['now_score'], f"diff found, buggy stat script: {np.mean(best_scores)} vs. {case_report['now_score']}"

        to_print = f'{case_name}, {np.mean(best_scores):.3f}, [' + ', '.join([f'{s:.3f}' for s in best_scores]) + ']\n'
        if case_name in print_items:
            fout.write(to_print)
        
        full_score += case_report['full_score']

        for i, best_score in enumerate(best_scores):
            if len(tot_scores) <= i:
                tot_scores.append(0.)
            tot_scores[i] += best_score
    
    tot_str = f'Tot: {np.mean(tot_scores)/full_score * 100.:.3f}% from [' + ', '.join([f'{s/full_score * 100.:.3f}%' for s in tot_scores]) + ']'
    print(tot_str)
    fout.write(tot_str)

    fout.close()

