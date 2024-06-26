
import os
import os.path as osp
import argparse
import json
import pandas as pd

# python3 ffqa_processor.py generations_ffqav2_codellama_13b_python.json references.json codellama_13b_python_output.csv

dataset_csv_path = os.environ['DATASET_CSV_PATH']

parser = argparse.ArgumentParser()
parser.add_argument('generation_path', type=str, help='generations .json')
parser.add_argument('references_path', type=str, help='reference .json')
parser.add_argument('out_csv_path', type=str, help='output csv path')
parser.add_argument('--eos', type=str, default='</s>', help='eos token')
if __name__ == '__main__':
    args = parser.parse_args()
    ds = pd.read_csv(dataset_csv_path)
    ds_prompts = {}
    out_completions = []
    out_filenames = []
    for i, row in ds.iterrows():
        ds_prompts[row['filename']] = row['content_prompt']
    with open(args.generation_path, 'r') as f:
        generations = json.load(f)
    with open(args.references_path, 'r') as f:
        references = json.load(f)
    for gens, ref in zip(generations, references):
        print(ref)
        for gen in gens:
            if len(ds_prompts[ref]) > len(gen) - 100:
                # print(ref, 'Long:', len(ds_prompts[ref]))
                try:
                    completion = gen[gen.index(ds_prompts[ref][-len(gen) + 100:]) + len(ds_prompts[ref][-len(gen) + 100:]): ]
                except:
                    # pass the tokenizer
                    from transformers import AutoTokenizer
                    tokenizer = AutoTokenizer.from_pretrained("internlm/internlm-7b", trust_remote_code=True)
                    ds_prompts[ref] = tokenizer.decode(tokenizer(ds_prompts[ref])['input_ids'])[4:].strip()
                    # print('!!!!!!!\n', ds_prompts[ref], '!!!!!!!\n')
                    try:
                        completion = gen[gen.index(ds_prompts[ref].strip()) + len(ds_prompts[ref].strip()): ]
                    except:
                        print(gen, '\n=========\n', ds_prompts[ref])
                        exit(1)
            else:
                try:
                    completion = gen[gen.index(ds_prompts[ref]) + len(ds_prompts[ref]): ]
                except:
                    # pass the tokenizer
                    from transformers import AutoTokenizer
                    tokenizer = AutoTokenizer.from_pretrained("internlm/internlm-7b", trust_remote_code=True)
                    ds_prompts[ref] = tokenizer.decode(tokenizer(ds_prompts[ref])['input_ids'])[4:].strip()
                    # print('!!!!!!!\n', ds_prompts[ref], '!!!!!!!\n')
                    try:
                        completion = gen[gen.index(ds_prompts[ref].strip()) + len(ds_prompts[ref].strip()): ]
                    except:
                        print(gen, '\n=========\n', ds_prompts[ref])
                        print('!!! bad internlm repeating bug found at', ref)
                        if '<eoh>' in gen:
                            completion = gen[gen.index('<eoh>'): ]
                        elif '<start_of_turn>model\n' in gen:
                            completion = gen[gen.index('<start_of_turn>model\n'): ]
            
            # print('orig:', completion)
            qwen_start_key = '<|im_start|>assistant\n'
            baichuan_start_key = '<reserved_107>'
            zypher_start_key = '<|assistant|>\n'
            octo_start_key = '\n\nAnswer:'
            qwen_end_key = '<|im_end|>'
            wizard_start_key = '### Response:'
            internlm_start_key = '\n<|Bot|>:'
            lingyi_start_key = '\n<|im_start|> assistant'
            magi_start_key = '@@ Response\n'
            mixtral_moe_start_key = '[/INST] '
            yuan_end_key = '<eod>'
            llama2_start_key = ' [/INST]'
            deepseek_chat_start_key = '\n\n' + 'Assistant:'
            gemma_start_key = '<start_of_turn>model\n'
            gemma_end_key = '<end_of_turn>'
            llama3_start_key = '<|start_header_id|>assistant<|end_header_id|>\n\n'
            llama3_end_key1 = '<|end_of_text|>'
            llama3_end_key2 = '<|eot_id|>'
            if qwen_start_key in completion:
                completion = completion[completion.index(qwen_start_key) + len(qwen_start_key): ]
            if baichuan_start_key in completion:
                completion = completion[completion.index(baichuan_start_key) + len(baichuan_start_key): ]
            if zypher_start_key in completion:
                completion = completion[completion.index(zypher_start_key) + len(zypher_start_key): ]
            if octo_start_key in completion:
                completion = completion[completion.index(octo_start_key) + len(octo_start_key): ]
            if wizard_start_key in completion:
                completion = completion[completion.index(wizard_start_key) + len(wizard_start_key): ]
            if internlm_start_key in completion:
                completion = completion[completion.index(internlm_start_key) + len(internlm_start_key): ]
            if lingyi_start_key in completion:
                completion = completion[completion.index(lingyi_start_key) + len(lingyi_start_key): ]
            if magi_start_key in completion:
                completion = completion[completion.index(magi_start_key) + len(magi_start_key): ]
            if mixtral_moe_start_key in completion:
                completion = completion[completion.index(mixtral_moe_start_key) + len(mixtral_moe_start_key): ]
            if llama2_start_key in completion:
                completion = completion[completion.index(llama2_start_key) + len(llama2_start_key): ]
            if deepseek_chat_start_key in completion:
                completion = completion[completion.index(deepseek_chat_start_key) + len(deepseek_chat_start_key): ]
            if gemma_start_key in completion:
                completion = completion[completion.index(gemma_start_key) + len(gemma_start_key): ]
            if qwen_end_key in completion:
                completion = completion[: completion.index(qwen_end_key)]
            if yuan_end_key in completion:
                completion = completion[: completion.index(yuan_end_key)]
            if gemma_end_key in completion:
                completion = completion[: completion.index(gemma_end_key)]
            if llama3_start_key in completion:
                completion = completion[completion.index(llama3_start_key) + len(llama3_start_key): ]
            if llama3_end_key1 in completion:
                completion = completion[: completion.index(llama3_end_key1)]
            if llama3_end_key2 in completion:
                completion = completion[: completion.index(llama3_end_key2)]
            # print('new:', completion)
            
            if completion.count(args.eos) > 0:
                completion = completion[:completion.index(args.eos)]
            out_completions.append(completion)
            out_filenames.append(ref)
    out_df = pd.DataFrame({'filename': out_filenames, 'completion': out_completions})
    out_df.to_csv(args.out_csv_path)
    print(f'Output to {args.out_csv_path}, len={len(out_df)}')
