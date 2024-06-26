"""
    Dump problem-level breakdown results to csv.
    Including the problem type, lang, caseURLs, model avg, best@10, best@all score.
    Also, include full score rate and empty score rate among all responses
    For free-form qa questions, will also include min, max, mean of
        rouge1
        rouge2
        rougeL
        rougeLsum
"""
import os
import os.path as osp
import pandas as pd
import numpy as np
import yaml
import argparse
from collections import OrderedDict
from tqdm import tqdm

# usage example:
# v2.0.0
# python3 analyze/parallel_results_analyze/dump_problem_level_csv.py ../result_parallel_freeform_qa_ver200_eval_gpt /opt/tiger/problem_level_v200_gpt.csv -r $(ls -p1 /opt/tiger/result_parallel_freeform_qa_ver200_eval_gpt/*.yaml | sed 's#.*/##' | tr '\n' ' ')
#
# v2.1
# python3 analyze/parallel_results_analyze/dump_problem_level_csv.py ../result_parallel_freeform_qa_ver21_eval_gpt /opt/tiger/problem_level_v21_gpt.csv -r $(ls -p1 /opt/tiger/result_parallel_freeform_qa_ver21_eval_gpt/*.yaml | sed 's#.*/##' | tr '\n' ' ')
# python3 analyze/parallel_results_analyze/dump_problem_level_csv.py ../result_parallel_freeform_qa_ver21_eval /opt/tiger/problem_level_v21_gpt.csv -r $(ls -p1 /opt/tiger/result_parallel_freeform_qa_ver21_eval/*gpt*.yaml | sed 's#.*/##' | tr '\n' ' ')


POSSIBLE_FIELD_LIST = ['keywords', 'blank_filling', 'unit_test', 'similarity', 'custom']

parser = argparse.ArgumentParser()
parser.add_argument('root_dir', type=str, help='Root directory that stores those csv files')
parser.add_argument('output_path', type=str, help='Output csv file path')
parser.add_argument('-r', '--result_yaml', type=str, nargs='+', help='yaml file to parse')
parser.add_argument('--case_url_path', type=str, help='a csv file that records the correspondence between case number and original queston urls', default='case_urls.csv')
if __name__ == '__main__':
    args = parser.parse_args()
    assert len(args.result_yaml) > 0

    # use the first result file to grab attribute data of each case
    canopy_resfile = args.result_yaml[0]
    with open(osp.join(args.root_dir, canopy_resfile), 'r') as f:
        canopy_result = yaml.load(f, yaml.Loader)
    cases_list = sorted(list(canopy_result.keys()), key=lambda x: int(x.split('.')[0].split('-')[-1]))
    print('# tot number of cases:', len(cases_list))

    # grab case source urls
    case_url_df = pd.read_csv(args.case_url_path)
    case_url_dict = {} # str -> str
    for i, row in case_url_df.iterrows():
        case_url_dict[row['case']] = row['url']
    
    # determine each case's type
    case_types = {} # str -> [str]
    for case in cases_list:
        case_result = canopy_result[case]['detail'][0]

        cur_case_types = []
        for field in POSSIBLE_FIELD_LIST:
            if field + '_score' in case_result:
                nfield = field
                if field == 'custom':
                    # check what is the real metric type
                    with open(case, 'r') as f:
                        case_cfg = yaml.load(f, yaml.Loader)
                        nfield = case_cfg['grading']['customized'].get('real_metric_type', field)
                cur_case_types.append(nfield)
        case_types[case] = cur_case_types
    
    # determine each case's lang and area
    case_langs = {} # str -> str
    case_pblmtypes = {} # str -> str
    for case in cases_list:
        with open(case, 'r') as f:
            case_cfg = yaml.load(f, yaml.Loader)
        case_langs[case] = case_cfg['lang']
        case_pblmtypes[case] = case_cfg['type']

    # determine max local score for later normalization
    case_max_local_scores = {} # str -> float
    case_min_local_scores = {} # str -> float
    for case in cases_list:
        case_result = canopy_result[case]
        first_case_details = case_result['detail'][0]
        
        now_case_score_tot = 0.
        for field in POSSIBLE_FIELD_LIST:
            if field + '_score' in first_case_details:
                now_case_score_tot += first_case_details[field + '_totscore']
            
        # overwrite max_score
        if 'max_score' in first_case_details:
            now_case_score_tot = first_case_details['max_score']
        case_max_local_scores[case] = now_case_score_tot

        if 'min_score' in first_case_details:
            case_min_local_scores[case] = first_case_details['min_score']

    response_wise_result = {}

    # main processing for each response file
    for now_result_yaml_path in tqdm(args.result_yaml):
        with open(osp.join(args.root_dir, now_result_yaml_path), 'r') as f:
            now_result_data = yaml.load(f, yaml.Loader)
        
        num_responses = len(now_result_data[cases_list[0]]['detail'])
        casewise_stats = {}

        for now_case in cases_list:
            now_case_result_data = now_result_data[now_case]

            # compute all local score, and then normalized to get global score list
            local_scores = []
            for detail in now_result_data[now_case]['detail']:
                now_score = 0.
                for field in POSSIBLE_FIELD_LIST:
                    if field + '_score' in detail:
                        now_score += detail[field + '_score']
                now_score = min(now_score, case_max_local_scores[now_case])
                if now_case in case_min_local_scores:
                    now_score = max(now_score, case_min_local_scores[now_case])
                local_scores.append(now_score)
            assert len(local_scores) == num_responses, f"Len mismatch: {num_responses} expected, {len(local_scores)} found"
            global_scores = [s / case_max_local_scores[now_case] for s in local_scores]

            # compute mean, max by 10, max by all
            global_mean_score = np.mean(global_scores)
            global_max_by_ten = np.mean([np.max(global_scores[i: i+10]) for i in range(0, len(global_scores), 10)])
            global_max_score = np.max(global_scores)
            global_min_score = np.min(global_scores)

            # compute min, max, mean of rouge scores if needed
            # have_similarity = False
            # rouge1_min, rouge1_max, rouge1_mean, rouge2_min, rouge2_max, rouge2_mean, \
            #     rougeL_min, rougeL_max, rougeL_mean, rougeLsum_min, rougeLsum_max, rougeLsum_mean = \
            #         0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.
            # local_sim_score_min, local_sim_score_max, local_sim_score_mean = 0., 0., 0.
            # local_tot_sim_score = 0.
            # global_sim_score_min, global_sim_score_max, global_sim_score_mean = 0., 0., 0.
            # if 'similarity' in case_types[now_case]:
            #     have_similarity = True
            #     rouge1, rouge2, rougeL, rougeLsum = [], [], [], []
            #     local_sim_scores, global_sim_scores = [], []
            #     for detail in now_result_data[now_case]['detail']:
            #         local_sim_scores.append(detail['similarity_score'])
            #         local_tot_sim_score = detail['similarity_totscore']
            #         more = detail['similarity_detail'][0]
            #         rouge1.append(more['rouge1'])
            #         rouge2.append(more['rouge2'])
            #         rougeL.append(more['rougeL'])
            #         rougeLsum.append(more['rougeLsum'])
            #     rouge1_min, rouge1_max, rouge1_mean = np.min(rouge1), np.max(rouge1), np.mean(rouge1)
            #     rouge2_min, rouge2_max, rouge2_mean = np.min(rouge2), np.max(rouge2), np.mean(rouge2)
            #     rougeL_min, rougeL_max, rougeL_mean = np.min(rougeL), np.max(rougeL), np.mean(rougeL)
            #     rougeLsum_min, rougeLsum_max, rrougeLsum_mean = np.min(rougeLsum), np.max(rougeLsum), np.mean(rougeLsum)
            #     local_sim_score_min, local_sim_score_max, local_sim_score_mean = np.min(local_sim_scores), np.max(local_sim_scores), np.mean(local_sim_scores)
            #     global_sim_score_min, global_sim_score_max, global_sim_score_mean = local_sim_score_min / local_tot_sim_score, local_sim_score_max / local_tot_sim_score, local_sim_score_mean / local_tot_sim_score
            
            # gather result
            casewise_stats[now_case] = {
                'local_scores': local_scores,
                'global_scores': global_scores,
                'global_mean_score': global_mean_score,
                'global_max_by_ten': global_max_by_ten,
                'global_max_score': global_max_score,
                'global_min_score': global_min_score,
                # 'similarity': {
                #     'have_similarity': have_similarity,
                #     'rouge1_min': rouge1_min,
                #     'rouge1_max': rouge1_max,
                #     'rouge1_mean': rouge1_mean,
                #     'rouge2_min': rouge2_min,
                #     'rouge2_max': rouge2_max,
                #     'rouge2_mean': rouge2_mean,
                #     'rougeL_min': rougeL_min,
                #     'rougeL_max': rougeL_max,
                #     'rougeL_mean': rougeL_mean,
                #     'rougeLsum_min': rougeLsum_min,
                #     'rougeLsum_max': rougeLsum_max,
                #     'rougeLsum_mean': rougeLsum_mean,
                #     'local_sim_score_min': local_sim_score_min,
                #     'local_sim_score_max': local_sim_score_max,
                #     'local_sim_score_mean': local_sim_score_mean,
                #     'global_sim_score_min': global_sim_score_min,
                #     'global_sim_score_max': global_sim_score_max,
                #     'global_sim_score_mean': global_sim_score_mean,
                #     'local_tot_sim_score': local_tot_sim_score
                # }
            }
        response_wise_result[now_result_yaml_path] = {
            'num_responses': num_responses,
            'casewise_stats': casewise_stats
        }
    
    print('collect done, now output...')

    data = OrderedDict()
    data['cases'] = cases_list
    data['lang'] = [case_langs[c] for c in cases_list]
    data['metric'] = [case_types[c][0] if len(case_types[c]) == 1 else case_types[c] for c in cases_list]
    data['pblmtype'] = [case_pblmtypes[c] for c in cases_list]
    data['url'] = [case_url_dict[c] for c in cases_list]
    data['local_totscore'] = [case_max_local_scores[c] for c in cases_list]

    for now_result_yaml_path in tqdm(args.result_yaml):
        save_prefix = now_result_yaml_path.split('_')[2]
        data[save_prefix + '_num_responses'] = [response_wise_result[now_result_yaml_path]['num_responses'] for _ in cases_list]
        data[save_prefix + '_mean'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['global_mean_score'] for case in cases_list]
        data[save_prefix + '_max'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['global_max_score'] for case in cases_list]
        data[save_prefix + '_max_by_ten'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['global_max_by_ten'] for case in cases_list]
        data[save_prefix + '_min'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['global_min_score'] for case in cases_list]
        # data[save_prefix + '_max_Rouge1'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['similarity']['rouge1_max'] if 'similarity' in case_types[case] else '' for case in cases_list]
        # data[save_prefix + '_max_Rouge2'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['similarity']['rouge2_max'] if 'similarity' in case_types[case] else '' for case in cases_list]
        # data[save_prefix + '_max_RougeL'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['similarity']['rougeL_max'] if 'similarity' in case_types[case] else '' for case in cases_list]
        # data[save_prefix + '_max_RougeLsum'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['similarity']['rougeLsum_max'] if 'similarity' in case_types[case] else '' for case in cases_list]
        # data[save_prefix + '_max_simscore'] = [response_wise_result[now_result_yaml_path]['casewise_stats'][case]['similarity']['global_sim_score_max'] if 'similarity' in case_types[case] else '' for case in cases_list]

    pd.DataFrame(data).to_csv(args.output_path)