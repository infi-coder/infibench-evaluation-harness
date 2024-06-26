import os
import os.path as osp
import argparse
from typing import OrderedDict
import yaml
import numpy as np
from tqdm import tqdm
import pandas as pd

# usage example:
# python3 analyze/parallel_results_analyze/dump_overall_scores.py /opt/tiger/result_parallel_freeform_qa_ver21_eval /opt/tiger/overall_scores.csv
# python3 analyze/parallel_results_analyze/dump_overall_scores.py /opt/tiger/result_ver21_append_1 /opt/tiger/overall_scores_append1.csv
# python3 analyze/parallel_results_analyze/dump_overall_scores.py /opt/tiger/result_files /opt/tiger/overall_scores.csv

def stem_to_model_name(fname: str) -> str:
    name_pieces = fname.rsplit('.', 1)[0].split('_')
    if len(name_pieces) >= 2 and name_pieces[0] in ['eval', 'evaltable'] and name_pieces[1].isdigit():
        name_pieces = name_pieces[2:]
    if len(name_pieces) >= 1 and name_pieces[0] in ['v210']:
        name_pieces = name_pieces[1:]
    if name_pieces[-1] == 'table':
        name_pieces = name_pieces[:-1]
    model_name = '_'.join(name_pieces)
    if model_name.endswith('_parallel'):
        model_name = model_name[: -len('_parallel')]
    if model_name.endswith('_output'):
        model_name = model_name[: -len('_output')]
    return model_name

parser = argparse.ArgumentParser()
parser.add_argument('result_dir', type=str, help='Directory with all txt result files')
parser.add_argument('output_path', type=str, help='Path to output')
parser.add_argument('--grouping', type=str, help='Path to a yaml file with grouping information', default='analyze/difficulty_levels.yaml')
if __name__ == '__main__':
    args = parser.parse_args()
    results = OrderedDict()
    # filter out table files
    result_files = []
    for fname in os.listdir(args.result_dir):
        if fname.endswith('.txt'):
            with open(osp.join(args.result_dir, fname), 'r') as f:
                firstline = f.readline()
                if firstline.startswith('-' * 30):
                    result_files.append(fname)
    print(f'{len(result_files)} result table files found')

    # read in question groupings
    with open(args.grouping, 'r') as f:
        grouping = yaml.load(f, yaml.Loader)
        grouping_keys = sorted(list(grouping.keys()))
        for k in grouping_keys:
            grouping[k] = set(grouping[k]) # use set to improve efficiency

    # use the first table file as the canopy to parse needed fields
    with open(osp.join(args.result_dir, result_files[0]), 'r') as f:
        lines = f.readlines()
        for line in lines[3:]:
            if line.startswith('-' * 20):
                # reaches the end
                break
            field = line.strip(' ').split('|')[0].strip(' ')
            results[field] = []
    
    for g in grouping_keys:
        results['Group: ' + g] = []

    # plug in some additional fields
    results['num_responses'] = []
    results['mean_score'] = []
    results['overall_maxscore'] = []
    
    # now working on all tables
    # first sort result files by implicit model names
    file_model_names = []
    for fname in result_files:
        model_name = stem_to_model_name(fname)
        yaml_detail_file = None
        n_found = 0
        for yaml_fname in os.listdir(args.result_dir):
            if yaml_fname.endswith('.yaml') and stem_to_model_name(yaml_fname) == model_name:
                # found the corresponding yaml result file!
                yaml_detail_file = yaml_fname
                n_found += 1
        assert n_found == 1, f'Multiple yaml result detail file found for {fname}'
        assert yaml_detail_file is not None, f'Could not found the corresponding result detail file for {fname}'
        file_model_names.append((fname, model_name, yaml_detail_file))
    
    file_model_names = sorted(file_model_names, key=lambda x: x[1])

    # debug
    # file_model_names = file_model_names[:10]

    for fname, model_name, yaml_detail_file in tqdm(file_model_names):
        with open(osp.join(args.result_dir, fname), 'r') as f:
            lines = f.readlines()[3:]
            for line in lines:
                if line.startswith('-' * 20):
                    # mark the end
                    break
                lines = line.split('|')
                field = lines[0].strip(' ')
                score = lines[2][: lines[2].index('±')].strip(' ')
                score_std = lines[2][lines[2].index('±') + 1: ].strip(' ')
                full_score = lines[3].strip(' ')
                results[field].append([model_name, score, score_std, full_score])
        
        max_score = []
        mean_max_10_score = []
        mean_score = []
        num_responses = None

        by_group_info = {k: [[], [], []] for k in grouping_keys} # record max, mean_max_10, mean

        with open(osp.join(args.result_dir, yaml_detail_file), 'r') as f:
            detail_data = yaml.load(f, yaml.Loader)
            for key, value in detail_data.items():
                if len(value['all_scores']) == 0:
                    value['all_scores'] = [0.]
                if num_responses is None:
                    num_responses = len(value['all_scores'])
                max_score.append(np.max(value['all_scores']))
                mean_score.append(np.mean(value['all_scores']))
                group = []
                for i in range(0, len(value['all_scores']), 10):
                    group.append(np.max(value['all_scores'][i: i+10]))
                mean_max_10_score.append(np.mean(group))

                for g in grouping_keys:
                    if key in grouping[g]:
                        by_group_info[g][0].append(np.max(value['all_scores']))
                        by_group_info[g][1].append(np.mean(group))
                        by_group_info[g][2].append(np.mean(value['all_scores']))
        
        results['num_responses'].append([model_name, num_responses])
        results['mean_score'].append([model_name, f'{np.sum(mean_score) / len(mean_score) * 100.:.2f}%', '0.00%', len(mean_score)])
        results['overall_maxscore'].append([model_name, f'{np.sum(max_score) / len(max_score) * 100.:.2f}%', '0.00%', len(max_score)])
        model_score = np.sum(mean_max_10_score) / len(mean_max_10_score)
        
        for g in grouping_keys:
            cur_group_maxes, cur_group_10_maxes, cur_group_means = by_group_info[g]
            results['Group: ' + g].append([model_name, f'{np.sum(cur_group_10_maxes) / len(cur_group_10_maxes) * 100.:.2f}%', '0.00%', len(cur_group_10_maxes), f'{np.sum(cur_group_maxes) / len(cur_group_maxes) * 100.:.2f}%', f'{np.sum(cur_group_means) / len(cur_group_means) * 100.:.2f}%'])

        comp_score = f'{model_score * 100.:.2f}%'
        rec_score = results['Overall Score'][-1][1]
        assert comp_score == rec_score, f'{model_name} - computed score {comp_score}, recorded score {rec_score} mismatch'
        print(model_name, f'{num_responses} responses', f'{model_score * 100.:.2f}%', results['Overall Score'][-1][1])
    
    df_data = {}
    df_data['modelname'] = [f[1] for f in file_model_names]
    df_data['tablefile'] = [f[0] for f in file_model_names]
    df_data['yamlfile'] = [f[2] for f in file_model_names]
    df_data['num_responses'] = [f[1] for f in results['num_responses']]
    for field in results:
        if field != 'num_responses':
            df_data[field + '_score'] = [f[1] for f in results[field]]
            df_data[field + '_std'] = [f[2] for f in results[field]]
            df_data[field + '_num_pblms'] = [f[3] for f in results[field]]
            if field.startswith('Group: '): # we have additional stats for them
                df_data[field + '_maxscore'] = [f[4] for f in results[field]]
                df_data[field + '_mean_score'] = [f[5] for f in results[field]]

    df = pd.DataFrame(df_data, columns=['modelname', 'num_responses'] + 
    [k for k in df_data.keys() if k.startswith('Overall Score')] + 
    [k for k in df_data.keys() if k.startswith('mean_score') and (k.count('_std') == 0) and (k.count('_num_pblms') == 0)] + 
    [k for k in df_data.keys() if k.startswith('overall_maxscore') and (k.count('_std') == 0) and (k.count('_num_pblms') == 0)] + 
    [k for k in df_data.keys() if k.startswith('Group: ') and (k.count('_std') == 0)] + 
    [k for k in df_data.keys() if k.startswith('Type: ')] + [k for k in df_data.keys() if k.startswith('Metric: ')] + [k for k in df_data.keys() if k.startswith('Lang: ')] + ['tablefile', 'yamlfile'])
    df.to_csv(args.output_path)
