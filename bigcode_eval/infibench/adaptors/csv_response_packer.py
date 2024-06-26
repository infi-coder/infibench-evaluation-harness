"""
    Pack the responses into a csv file for ease of storage and processing.
    Example usage: 
    - python3 adaptors/csv_response_packer.py responses/gpt-4_0.2_0.9_30_suite_v2.0.0/ ../gpt-4-0613_output.csv
    - python3 adaptors/csv_response_packer.py responses/gpt-4-1106-preview_0.2_0.9_30_suite_v2.0.0/ ../gpt-4-1106_output.csv
"""
import argparse
import csv
import pandas as pd
import yaml
import os
import os.path as osp

parser = argparse.ArgumentParser()
parser.add_argument('in_folder', type=str)
parser.add_argument('out_csv', type=str)
if __name__ == '__main__':
    args = parser.parse_args()
    print('in_folder', args.in_folder)
    print('out_csv', args.out_csv)
    # Read the params.yaml file
    with open(osp.join(args.in_folder, 'params.yaml'), 'r') as f:
        directories = yaml.safe_load(f)['answer_paths']
    filenames = []
    completions = []
    for directory in directories:
        print('directory', directory)
        for response_path in directories[directory]:
            with open(osp.join(args.in_folder, response_path), 'r') as f:
                now_response = f.read()
            filenames.append(directory)
            completions.append(now_response)
    df = pd.DataFrame({'filename': filenames, 'completion': completions})
    print(f'data len = {len(df)}')
    df.to_csv(args.out_csv, index=True)
    print('done, output to', args.out_csv)