"""
  A Script to draw distinguishing cases to conduct human study
"""

import numpy as np
import pandas as pd
import yaml
import random
import os
import os.path as osp
import tqdm
from openai import OpenAI

suite_path = 'suite_v2.1.yaml'
case_urls_path = 'case_urls.csv'
model_results = [
    ['human_study/source/gpt-4-0613_output.csv', 'human_study/source/gpt-4-0613_result.yaml'],
    ['human_study/source/mistralai_Codestral-22B-v0.1_output.csv', 'human_study/source/mistralai_Codestral-22B-v0.1_result.yaml'],
    ['human_study/source/gpt-3.5-turbo-0.2-0.9-30_output.csv', 'human_study/source/gpt-3.5-turbo-0.2-0.9-30_result.yaml']
]

# TOT=150

# MODE = 'INFIRATER_DRAW'

# MODE = 'GPTRATER_GENCASE'

# MODE = 'GPTRATER_RATING'

# MODE = 'GPTRATER_DRAW'

MODE = 'PARSE_HUMAN_RATING'


OUTPUT_DIR = 'human_study/rater_cases'
if not osp.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

if __name__ == '__main__':
    if MODE == 'INFIRATER_DRAW':
        # First, we generate the scores by grading
        #    python3 bigcode_eval/infibench/grader_main.py bigcode_eval/infibench/suite_v2.1.yaml bigcode_eval/infibench/human_study/source/gpt-4-0613_output.csv --batched --batched_cases_path bigcode_eval/infibench/batched_cases/suite_v2.1_data.csv --result_detail_path bigcode_eval/infibench/human_study/source/gpt-4-0613_result.yaml --result_summary_path bigcode_eval/infibench/human_study/source/gpt-4-0613_summary.txt
        #    python3 bigcode_eval/infibench/grader_main.py bigcode_eval/infibench/suite_v2.1.yaml bigcode_eval/infibench/human_study/source/mistralai_Codestral-22B-v0.1_output.csv --batched --batched_cases_path bigcode_eval/infibench/batched_cases/suite_v2.1_data.csv --result_detail_path bigcode_eval/infibench/human_study/source/mistralai_Codestral-22B-v0.1_result.yaml --result_summary_path bigcode_eval/infibench/human_study/source/mistralai_Codestral-22B-v0.1_summary.txt
        #    python3 bigcode_eval/infibench/grader_main.py bigcode_eval/infibench/suite_v2.1.yaml bigcode_eval/infibench/human_study/source/gpt-3.5-turbo-0.2-0.9-30_output.csv --batched --batched_cases_path bigcode_eval/infibench/batched_cases/suite_v2.1_data.csv --result_detail_path bigcode_eval/infibench/human_study/source/gpt-3.5-turbo-0.2-0.9-30_result.yaml --result_summary_path bigcode_eval/infibench/human_study/source/gpt-3.5-turbo-0.2-0.9-30_summary.txt

        # Load suite names
        with open(suite_path, 'r') as f:
            suite_data = yaml.load(f, yaml.Loader)
        suite_cases = suite_data['cases']
        print(len(suite_cases))

        # Then we do a draw by checking the differentiable cases among the models
        case_response_with_scores = []
        for output_path, analyze_path in model_results:
            resp_set = pd.read_csv(output_path)
            with open(analyze_path, 'r') as f:
                analyze_res = yaml.load(f, yaml.Loader)
            now_response_with_scores = {}
            for suite_case in suite_cases:
                now_resps = resp_set[resp_set['filename'] == suite_case]['completion']
                now_total_scores = analyze_res[suite_case]['all_scores']
                now_response_with_scores[suite_case] = list(zip(now_resps, now_total_scores))
            case_response_with_scores.append(now_response_with_scores)

        # Then we do the random draw
        sf_suite_cases = suite_cases.copy()
        random.shuffle(sf_suite_cases)
        
        # Link to original question posts
        case_urls = pd.read_csv(case_urls_path)

        study_cases = []

        now_tt = 0
        for j, sc in enumerate(sf_suite_cases):
            # if now_tt >= TOT: break
            gathered_resps = [m[sc] for m in case_response_with_scores]


            case_url = case_urls[case_urls['case'] == sc]['url'].iloc[0]
            with open(sc.replace('eval_', 'prompt_').replace('.yaml', '.txt'), 'r') as f:
                question = f.read()

            found_distinguish = False
            for tries in range(10):
                selected = [list(random.choice(item)) for item in gathered_resps]
                for i, item in enumerate(selected):
                    item.append(i) # add model idx
                random.shuffle(selected)
                pair_a, pair_b = selected[0], selected[1]
                score_max = max(pair_a[1], pair_b[1])
                score_min = min(pair_a[1], pair_b[1])
                if score_max - score_min > 0.2:
                    study_cases.append([sc, case_url, question, pair_a, pair_b])
                    now_tt += 1
                    found_distinguish = True
                    # print(j, now_tt, score_max, score_min)
                    break
            
            if not found_distinguish:
                # anyway add the case for completeness
                now_tt += 1
                study_cases.append([sc, case_url, question, pair_a, pair_b])

        # print(study_cases[0])
        

        gts = []
        for i, item in enumerate(study_cases):
            case_url = item[1]
            with open(osp.join(OUTPUT_DIR, f'{i:04d}.md'), 'w') as f:
                f.write(f"""Case URL: {case_url}

------
Response A:

{item[3][0]}

Response A is better [ ] (label [x] to select)

-------
Response B:

{item[4][0]}

Response B is better [ ] (label [x]) to select)

-------

Response A and B are equally good [ ] (label [x]) to select
Response A and B are equally bad [ ] (label [x]) to select
""")
            gts.append({'ID': f'{i:04d}', 'Case': item[0], 'CaseURL': item[1], 'question': item[2], 
            'Amodel': item[3][1], 'Ascore': item[3][2], 'Bmodel': item[4][1], 'Bscore': item[4][2],
            'Aanswer': item[3][0], 'Banswer': item[4][0]})
        
        gt_frame = pd.DataFrame(gts)
        gt_frame.to_csv(osp.join(OUTPUT_DIR, 'infibench_ground_truth.csv'))

        print(now_tt, 'cases generated')


#     elif MODE == 'GPTRATER_GENCASE':

#         # Load suite names
#         with open(suite_path, 'r') as f:
#             suite_data = yaml.load(f, yaml.Loader)
#         suite_cases = suite_data['cases']
#         print(len(suite_cases))

#         # Then we do the random draw of cases
#         sf_suite_cases = suite_cases.copy()
#         random.shuffle(sf_suite_cases)

#         # Then we load model responses
#         case_responses = []
#         for output_path, _ in model_results:
#             resp_set = pd.read_csv(output_path)
#             now_response = {}
#             for suite_case in suite_cases:
#                 now_resps = resp_set[resp_set['filename'] == suite_case]['completion']
#                 now_response[suite_case] = list(now_resps)
#             case_responses.append(now_response)

#         # Link to original question posts
#         case_urls = pd.read_csv(case_urls_path)

#         # Ask GPT with a prompt
#         TOT_CASE = 0
#         cases = []
#         for j, sc in enumerate(sf_suite_cases):
#             case_url = case_urls[case_urls['case'] == sc]['url'].iloc[0]
#             for ii in range(len(case_responses)):
#                 for jj in range(ii + 1, len(case_responses)):
#                     if random.random() <= 0.5:
#                         resp_a, resp_b = random.choice(case_responses[ii][sc]), random.choice(case_responses[jj][sc])
#                         model_a, model_b = ii, jj
#                     else:
#                         resp_a, resp_b = random.choice(case_responses[jj][sc]), random.choice(case_responses[ii][sc])
#                         model_a, model_b = jj, ii
#                     with open(sc.replace('eval_', 'prompt_').replace('.yaml', '.txt'), 'r') as f:
#                         question = f.read()
#                     gpt_prompt = f"""Question:
# {question}

# Candidate A:
# {resp_a}

# Candidate B:
# {resp_b}

# Given the instruction and input above, please compare the two candidates.
# You only have 4 choices to output:
# If you think A is better, please output: 1. A is better
# If you think B is better, please output: 2. B is better
# If you think both are good enough correctly give the answer, please output: 3. Same good
# If you think both are bad and do not follow the instruction, please output: 4. Same bad
# Do not output anything else except the 4 choices above.
# Output your choice below:
# """
#                     cases.append([len(cases), model_a, model_b, sc, case_url, question, resp_a, resp_b, gpt_prompt])

#         print(len(cases))
        
#         # Output
#         OUTPUT_DIR = 'human_study/gpt_rater_rawcases'
#         if not osp.exists(OUTPUT_DIR):
#             os.makedirs(OUTPUT_DIR)
#         case_df = pd.DataFrame(cases, columns=['no', 'Amodelno', 'Bmodelno', 'case', 'caseurl', 'casequestion', 'Aresp', 'Bresp', 'gptprompt'])
#         case_df.to_csv(osp.join(OUTPUT_DIR, 'case_alldata.csv'))

#         for item in cases:
#             id = item[0]
#             txt = item[-1]
#             with open(osp.join(OUTPUT_DIR, f'gpt_prompt_{id:04d}.txt'), 'w') as f:
#                 f.write(txt)

    elif MODE == 'GPTRATER_RATING':

        with open('../../openai_token.key', 'r') as f:
            org_id, project_id, api_key = f.read().split()
            org_id, project_id, api_key = org_id.strip(), project_id.strip(), api_key.strip()

        client = OpenAI(
            organization=org_id,
            project=project_id,
            api_key=api_key
        )

        instruction_template = "You are a professional critic for a developer QA platform. You should reliability help us to distinguish answers to given question based on answer correctness."

        prompt_template = """Question:
{}

Candidate A:
{}

Candidate B:
{}

Given the instruction and input above, please compare the two candidates.
You only have 4 choices to output:
If you think A is better, please output: 1. A is better
If you think B is better, please output: 2. B is better
If you think both are good enough correctly give the answer, please output: 3. Same good
If you think both are bad and do not follow the instruction, please output: 4. Same bad
Do not output anything else except the 4 choices above.
Output your choice below:
"""

        infibench_rated_df = pd.read_csv(osp.join(OUTPUT_DIR, 'infibench_ground_truth.csv'))

        prompt1s = []
        prompt2s = []
        message1s = []
        message2s = []
        Avotes = []
        Bvotes = []

        for i in tqdm.tqdm(range(len(infibench_rated_df))):
            id = infibench_rated_df.iloc[i]['ID']
            question = infibench_rated_df.iloc[i]['question']
            aanswer = infibench_rated_df.iloc[i]['Aanswer']
            banswer = infibench_rated_df.iloc[i]['Banswer']

            prompt1 = prompt_template.format(question, aanswer, banswer)
            prompt2 = prompt_template.format(question, banswer, aanswer)

            completion1 = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": instruction_template},
                    {"role": "user", "content": prompt1}
                ]
            )
            message1 = completion1.choices[0].message.content

            completion2 = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": instruction_template},
                    {"role": "user", "content": prompt2}
                ]
            )
            message2 = completion2.choices[0].message.content

            prompt1s.append(prompt1)
            prompt2s.append(prompt2)
            message1s.append(message1)
            message2s.append(message2)

            print(message1, message2)

            score_add_mat = [['A is better', 1, 0],
                             ['B is better', 0, 1],
                             ['Same good', 1, 1],
                             ['Same bad', -1, -1]]
            gptascore, gptbscore = 0, 0
            for kw, s_da, s_db in score_add_mat:
                if kw in message1:
                    gptascore += s_da
                    gptbscore += s_db
                elif kw in message2:
                    gptascore += s_db
                    gptbscore += s_da
            
            print(gptascore, gptbscore)
            
            Avotes.append(gptascore)
            Bvotes.append(gptbscore)

        both_rated_df = infibench_rated_df.assign(prompt1=prompt1s, prompt2=prompt2s,
                                                  message1=message1s, message2=message2s,
                                                  gptAvote=Avotes, gptBvote=Bvotes)

        both_rated_df.to_csv(osp.join(OUTPUT_DIR, 'both_rated.csv'))

    # elif MODE == 'GPTRATER_DRAW':
    #     pass
    
    elif MODE == 'PARSE_HUMAN_RATING':
        
        both_rated_df = pd.read_csv(osp.join(OUTPUT_DIR, 'both_rated.csv'))

        human_rates = []
        for i in range(1000):
            now_rate = -1
            if osp.exists(osp.join(OUTPUT_DIR, f'{i:04d}.md')):
                with open(osp.join(OUTPUT_DIR, f'{i:04d}.md'), 'r') as f:
                    txt = f.read()
                hits = [kw in txt for kw in ['Response A is better [x] (label [x] to select)',
                                             'Response B is better [x] (label [x]) to select)',
                                             'Response A and B are equally good [x] (label [x]) to select',
                                             'Response A and B are equally bad [x] (label [x]) to select']]
                if sum(hits) == 1:
                    now_rate = hits.index(True)
                human_rates.append(now_rate)
            else:
                break
        
        print(human_rates)

        id_order = list(both_rated_df['ID'])
        human_rated_ordered = [human_rates[id] for id in id_order]

        final_rate_df = both_rated_df.assign(human_score=human_rated_ordered)
        final_rate_df.to_csv(osp.join(OUTPUT_DIR, 'final_rated.csv'))


