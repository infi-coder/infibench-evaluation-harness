import argparse
import os
import os.path as osp
import yaml
import pandas as pd
from tqdm import tqdm

# Usage:
#. python3 analyze/parallel_results_analyze/dump_question_responses_in_one_txt.py /opt/tiger/inficoder-eval-responses /opt/tiger/inficoder-eval-responses-in-txt

parser = argparse.ArgumentParser()
parser.add_argument('result_dir', type=str, help='Directory with all csv response files')
parser.add_argument('output_dir', type=str, help='Path to output all in one txt')
parser.add_argument('--suite', type=str, help='suite yaml file', default='suite_v2.1.yaml')
parser.add_argument('--case_urls', type=str, help='path to case - url mapping csv file', default='case_urls.csv')
parser.add_argument('--batched_prompt', type=str, help='path to batched prompt csv file', default='batched_prompts/suite_v2.0.0.csv')
if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.suite, 'r') as f:
        suite_data = yaml.load(f, yaml.Loader)
    case_yamls = suite_data['cases']
    case_url_df = pd.read_csv(args.case_urls)
    case_urls = {}
    batch_prompt_df = pd.read_csv(args.batched_prompt)
    case_infos = {}

    for i, row in case_url_df.iterrows():
        case_urls[row['case']] = row['url']
    
    for i, row in batch_prompt_df.iterrows():
        case_infos[row['filename']] = [row['system_prompt'], row['content_prompt'], row['n_token']]

    for case_yaml in case_yamls:
        with open(case_yaml, 'r') as f:
            case_conf = f.read()
        case_infos[case_yaml].append(case_conf)
    
    if not osp.exists(args.output_dir):
        os.makedirs(args.output_dir)

    for f in tqdm(os.listdir(args.result_dir)):
        if f.endswith('.csv'):
            outf_name = f.replace('.csv', '.txt')
            response = pd.read_csv(osp.join(args.result_dir, f))
            output_txt = ''

            for case_yaml in case_yamls:
                filtered_resp = response[response['filename'] == case_yaml]
                for i, rows in filtered_resp.iterrows():
                    output_txt += f'********** {case_yaml} token_len={case_infos[case_yaml][2]} **********\n'
                    output_txt += f'========== {case_yaml} SYSTEM PROMPT ==========\n' + case_infos[case_yaml][0] + '\n\n'
                    output_txt += f'========== {case_yaml} CONTENT PROMPT ==========\n' + case_infos[case_yaml][1] + '\n\n'
                    output_txt += f'========== {case_yaml} EVAL CONFIG ==========\n' + case_infos[case_yaml][3] + '\n\n'
                    output_txt += f'++++++++++ {case_yaml} COMPLETION idx {i} ++++++++++\n' + str(rows['completion']) + '\n\n'
                with open(osp.join(args.output_dir, outf_name), 'w') as f:
                    f.write(output_txt)