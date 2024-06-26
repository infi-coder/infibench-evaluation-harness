from transformers import AutoTokenizer
import os
import os.path as osp
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--suite_path', type=str, default='suite_v2.0.0.yaml')
parser.add_argument('--result_folder', type=str, default='responses/gpt-4_0.2_0.9_30_suite_v2.0.0')
parser.add_argument('--tokenizer', default=None, help='path to the tokenizer, if provided, I will count the number of tokens in the prompt and output it as a field')
if __name__ == '__main__':
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    print(args.tokenizer)
    with open(args.suite_path, 'r') as f:
        suite_cases = yaml.load(f, yaml.Loader)['cases']
    tot = 0
    exceed_lim_tot = 0
    for case in suite_cases:
        with open(case, 'r') as f:
            case_data = yaml.load(f, yaml.Loader)
        prompt_path = 'cases/' + case_data['prompt_path']
        with open(prompt_path, 'r') as f:
            prompts = f.read()
        case_base_name = case.split('/')[1].split('.')[0]
        for resp in range(30):
            with open(args.result_folder + '/' + case_base_name + f'_{resp}.txt', 'r') as f:
                now_resp = f.read()
            tok_len = len(tokenizer.tokenize(prompts + now_resp))
            tot += 1
            if tok_len >= 2048: exceed_lim_tot += 1
        print(tot, '>= 2048', exceed_lim_tot)

# among 8100 prompt + answers, 140 has token len >= 2K
# 30 has token len >= 8K