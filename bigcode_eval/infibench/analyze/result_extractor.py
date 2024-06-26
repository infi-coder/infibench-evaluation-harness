import yaml
import json
import numpy as np
import argparse
from tqdm import tqdm

result_paths = {
    'GPT-4': 'results/suite_v2.0.0_gpt-4_0.2_0.9_30_suite_v2.0.0.yaml',
    'GPT-3.5': 'results/suite_v2.0.0_gpt-3.5-turbo_0.2_0.9_30_suite_v2.0.0.yaml',
    'davinci-002': 'results/suite_v2.0.0_davinci-002_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-34B-Instruct': 'results/suite_v2.0.0_codellama-34b-instruct-new_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-34B': 'results/suite_v2.0.0_codellama-34b-base-new_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-34B-Python': 'results/suite_v2.0.0_codellama-34b-python-new_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-13B-Instruct': 'results/suite_v2.0.0_codellama-13b-instruct_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-13B': 'results/suite_v2.0.0_codellama-13b-base_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-13B-Python': 'results/suite_v2.0.0_codellama-13b-python_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-7B-Instruct': 'results/suite_v2.0.0_codellama-7b-instruct_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-7B': 'results/suite_v2.0.0_codellama-7b_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeLlama-7B-Python': 'results/suite_v2.0.0_codellama-7b-python_0.2_0.9_30_suite_v2.0.0.yaml',
    'WizardCoder-Python-34B-V1.0': 'results/suite_v2.0.0_wizardcoder-python-34b-new-new_0.2_0.9_10_suite_v2.0.0.yaml',
    'WizardCoder-Python-13B-V1.0': 'results/suite_v2.0.0_wizardcoder-python-13b-new_0.2_0.9_30_suite_v2.0.0.yaml',
    'WizardCoder-Python-7B-V1.0': 'results/suite_v2.0.0_wizardcoder-python-7b-new_0.2_0.9_30_suite_v2.0.0.yaml',
    'WizardCoder-15B-V1.0': 'results/suite_v2.0.0_WizardCoder-15B-V1.0_0.2_0.9_30_suite_v2.0.0.yaml',
    'WizardCoder-3B-V1.0': 'results/suite_v2.0.0_WizardCoder-3B-V1.0_0.2_0.9_30_suite_v2.0.0.yaml',
    'WizardCoder-1B-V1.0': 'results/suite_v2.0.0_WizardCoder-1B-V1.0_0.2_0.9_30_suite_v2.0.0.yaml',
    'phi-1.5': 'results/suite_v2.0.0_phi-1_5_new_0.2_0.9_30_suite_v2.0.0.yaml',
    'phi-1': 'results/suite_v2.0.0_phi-1_0.2_0.9_30_suite_v2.0.0.yaml',
    'StarCoderPlus': 'results/suite_v2.0.0_starcoderplus_0.2_0.9_30_suite_v2.0.0.yaml',
    'StarCoder': 'results/suite_v2.0.0_starcoder_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeGeeX2': 'results/suite_v2.0.0_codegeex2-6b-endn_0.2_0.9_30_suite_v2.0.0.yaml',
    'deepseek-coder-33b-instruct': 'results/suite_v2.0.0_deepseek-coder-33b-new-instruct_0.2_0.9_10_suite_v2.0.0.yaml',
    'deepseek-coder-6.7b-instruct': 'results/suite_v2.0.0_deepseek-coder-6.7b-instruct_0.2_0.9_30_suite_v2.0.0.yaml',
    'Qwen-14B-Chat': 'results/suite_v2.0.0_Qwen-14B-Chat_0.2_0.9_30_suite_v2.0.0.yaml',
    'Qwen-7B-Chat': 'results/suite_v2.0.0_Qwen-7B-Chat_0.2_0.9_30_suite_v2.0.0.yaml',
    'Baichuan2-13B-Chat': 'results/suite_v2.0.0_Baichuan2-13B-Chat_0.2_0.9_30_suite_v2.0.0.yaml',
    'Baichuan2-7B-Chat': 'results/suite_v2.0.0_Baichuan2-7B-Chat_0.2_0.9_30_suite_v2.0.0.yaml',
    'Zypher-7b-beta': 'results/suite_v2.0.0_zephyr-7b-beta_0.2_0.9_30_suite_v2.0.0.yaml',
    'OctoCoder': 'results/suite_v2.0.0_octocoder_0.2_0.9_30_suite_v2.0.0.yaml',
    'OctoGeeX': 'results/suite_v2.0.0_octogeex_0.2_0.9_30_suite_v2.0.0.yaml',
    'CodeGen2.5-7B-instruct': 'results/suite_v2.0.0_codegen25-7b-instruct_0.2_0.9_30_suite_v2.0.0.yaml'
}

result_sizes = {
    'GPT-4': None,
    'GPT-3.5': None,
    'davinci-002': 175,
    'CodeLlama-34B-Instruct': 34,
    'CodeLlama-34B': 34,
    'CodeLlama-34B-Python': 34,
    'CodeLlama-13B-Instruct': 13,
    'CodeLlama-13B': 13,
    'CodeLlama-13B-Python': 13,
    'CodeLlama-7B-Instruct': 7,
    'CodeLlama-7B': 7,
    'CodeLlama-7B-Python': 7,
    'WizardCoder-Python-34B-V1.0': 34,
    'WizardCoder-Python-13B-V1.0': 13,
    'WizardCoder-Python-7B-V1.0': 7,
    'WizardCoder-15B-V1.0': 15,
    'WizardCoder-3B-V1.0': 3,
    'WizardCoder-1B-V1.0': 1,
    'phi-1.5': 1.5,
    'phi-1': 1.3,
    'StarCoderPlus': 15.5,
    'StarCoder': 15.5,
    'CodeGeeX2': 6,
    'deepseek-coder-33b-instruct': 33,
    'deepseek-coder-6.7b-instruct': 6.7,
    'Qwen-14B-Chat': 14,
    'Qwen-7B-Chat': 7,
    'Baichuan2-13B-Chat': 13,
    'Baichuan2-7B-Chat': 7,
    'Zypher-7b-beta': 7,
    'OctoCoder': 15.5,
    'OctoGeeX': 6,
    'CodeGen2.5-7B-instruct': 7
}


def extractor(result_path, bsz=10, dev_cases=[], test_cases=[]):
    with open(result_path, 'r') as f:
        full_results = yaml.load(f, yaml.Loader)
    
    fields = ['keywords', 'blank_filling', 'unit_test', 'similarity', 'custom']
    tot_scores = []
    tot_dev_scores = []
    tot_test_scores = []
    full_score = 0.
    full_dev_score = 0.
    full_test_score = 0.
    
    for case_name, case_report in full_results.items():
        case_full_score = case_report['full_score']
        
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

        for i, best_score in enumerate(best_scores):
            if len(tot_scores) <= i:
                tot_scores.append(0.)
            tot_scores[i] += best_score
            if len(tot_dev_scores) <= i:
                tot_dev_scores.append(0.)
            if len(tot_test_scores) <= i:
                tot_test_scores.append(0.)
            if case_name in dev_cases:
                tot_dev_scores[i] += best_score
            if case_name in test_cases:
                tot_test_scores[i] += best_score
        
        full_score += case_report['full_score']
        full_dev_score += case_report['full_score'] if case_name in dev_cases else 0.
        full_test_score += case_report['full_score'] if case_name in test_cases else 0.
    
    print(full_score, full_dev_score, full_test_score)
    return full_score, [tot_score / full_score for tot_score in tot_scores], float(np.mean(tot_scores)) / full_score, \
                       [tot_score / full_dev_score for tot_score in tot_dev_scores], float(np.mean(tot_dev_scores)) / full_dev_score, \
                       [tot_score / full_test_score for tot_score in tot_test_scores], float(np.mean(tot_test_scores)) / full_test_score

parser = argparse.ArgumentParser()
parser.add_argument('--dev_path', type=str, default='suite_v2.0.0_dev.yaml')
parser.add_argument('--test_path', type=str, default='suite_v2.0.0_test.yaml')
parser.add_argument('--output_path', type=str, default='results/main_results.json')
if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.dev_path, 'r') as f:
        dev_cases = yaml.load(f, yaml.Loader)['cases']
        dev_cases = [c.replace('cases_dev', 'cases') for c in dev_cases]
    with open(args.test_path, 'r') as f:
        test_cases = yaml.load(f, yaml.Loader)['cases']
        test_cases = [c.replace('cases_test', 'cases') for c in test_cases]

    ans = []
    for k, v in tqdm(result_paths.items()):
        ret = extractor(v, dev_cases=dev_cases, test_cases=test_cases)
        item = ['', k, result_sizes[k]] + list(ret)
        ans.append(item)
    
    with open(args.output_path, 'w') as f:
        json.dump(ans, f, indent=2)
    

    with open(args.output_path, 'r') as f:
        ans = json.load(f)
    
    for item in ans:
        print(item[0], item[1], item[3], 
              [f'{v * 100.:.2f}%' for v in item[4]], f'{item[5] * 100.:.2f}%', f'std = {np.std(item[4]) * 100.:.2f}%', # full
              [f'{v * 100.:.2f}%' for v in item[6]], f'{item[7] * 100.:.2f}%', f'std = {np.std(item[6]) * 100.:.2f}%', # dev
              [f'{v * 100.:.2f}%' for v in item[8]], f'{item[9] * 100.:.2f}%', f'std = {np.std(item[8]) * 100.:.2f}%') # test
    print("Output to", args.output_path)
    