<h1 align="center">Full Evaluation Framework for InfiCoder-Eval</h1>

<h4 align="center">The InfiCoder Team</h4>

<h4 align="center">Project Page: https://infi-coder.github.io/inficoder-eval/</h4>

<h4 align="center">
    <p>
        <a href="#features">Features</a> |
        <a href="#usage">Usage</a> |
        <a href="#future">Contribution</a>
    <p>
</h4>

## Features
This is the evaluation framework for the InfiCoder-Eval benchmark along with dev set questions.

Featuring the execution runtime for 8 languages (Python, Javascript, Java, C, C++, Go, R, C#), given model responses, the framework can directly evaluate and output the scores along with subscores in a nice table.

## Usage


#### Setup

At this point, we only support Linux environment.

Run `pip3 install -r requirements.txt`, then `./setup.sh` (time costly, usually 1-2 hours) which installs necessary compilers and packages for multi-lingual execution environment.

Check the evaluation environment.
`Run python3 env_check.py` to check and fix the environment incompatibility according to the console output. If the console output is "`You're good to go.`", then we can proceed.

#### Evaluate

Usually, the evaluation involves three stages.

(1) Call API to generate responses (for evaluating OpenAPI models) or use our [Inference Framework](https://github.com/infi-coder/ffqa-evaluation-harness) to generate responses and unpack with `python3 adaptors/csv_response_unpacker.py your_response.csv responses/your_model_response_folder`.

- If you want to evaluate on the whole set of 270 questions:

(2) Grading: call `python3 grader_main.py suite_v2.0.0.yaml [your_model_response_folder]` to grade.

(3) Print Report: call `python3 print_result_stat.py results/suite_v2.0.0_[your_model_response_folder_basename].yaml [table_output_path_to_specify].txt --model_name [model_name_in_the_table_to_specify]`.

- If you want to evaluate on the dev set of 135 questions:

(2) Grading: call `python3 grader_main.py suite_v2.0.0_dev.yaml [your_model_response_folder]` to grade.

(3) Print Report: call `python3 print_result_stat.py results/suite_v2.0.0_dev_[your_model_response_folder_basename].yaml [table_output_path_to_specify].txt --model_name [model_name_in_the_table_to_specify]`.


#### Result Examples

We have attached GPT-4 and GPT-3.5-turbo responses --- you can play with them and test the usage of the framework. See a self-contained instruction in `run_dev.sh`. 

- Whole set:

Command:
```bash
python3 print_result_stat.py results/suite_v2.0.0_gpt-4_0.2_0.9_30_suite_v2.0.0.yaml example_table_gpt-4.txt --model_name gpt-4
```

Output: (full score 59.75% ± 0.51%)
```bash
[159.94376961356517, 162.71023409193634, 161.31650626492984]
Write to example_table_gpt-4.txt
Final Result:
--------------------------------------------------------------------------------------------------
                                    | gpt-4          |                  | Full Score | Allocation 
------------------------------------|--------|-------|--------|---------|------------|------------
 Overall Score                      | 161.32   ±1.38 | 59.75%   ±0.51%  | 270.00     |            
 Lang: python                       | 32.22    ±1.25 | 68.56%   ±2.66%  | 47.00      | 17.41%     
 Lang: javascript                   | 31.07    ±0.46 | 70.61%   ±1.05%  | 44.00      | 16.30%     
 Lang: bash                         | 11.76    ±0.35 | 55.99%   ±1.66%  | 21.00      | 7.78%      
 Lang: dart                         | 9.41     ±1.02 | 49.50%   ±5.36%  | 19.00      | 7.04%      
 Lang: java                         | 13.79    ±0.04 | 76.63%   ±0.23%  | 18.00      | 6.67%      
 Lang: c#                           | 4.67     ±0.88 | 38.89%   ±7.35%  | 12.00      | 4.44%      
 Lang: css                          | 7.98     ±0.19 | 79.78%   ±1.92%  | 10.00      | 3.70%      
 Lang: html                         | 7.00     ±0.00 | 70.00%   ±0.00%  | 10.00      | 3.70%      
 Lang: r                            | 5.50     ±1.00 | 55.00%   ±10.00% | 10.00      | 3.70%      
 Lang: rust                         | 6.00     ±0.73 | 60.00%   ±7.26%  | 10.00      | 3.70%      
 Lang: c++/c                        | 7.33     ±0.76 | 73.33%   ±7.64%  | 10.00      | 3.70%      
 Lang: php                          | 3.67     ±0.29 | 36.67%   ±2.89%  | 10.00      | 3.70%      
 Lang: go                           | 7.33     ±0.00 | 73.33%   ±0.00%  | 10.00      | 3.70%      
 Lang: ruby                         | 6.42     ±0.29 | 64.17%   ±2.89%  | 10.00      | 3.70%      
 Lang: kotlin                       | 2.83     ±0.00 | 28.33%   ±0.00%  | 10.00      | 3.70%      
 Lang: swift                        | 2.84     ±0.12 | 28.41%   ±1.19%  | 10.00      | 3.70%      
 Lang: vba                          | 1.51     ±0.04 | 16.78%   ±0.42%  | 9.00       | 3.33%      
 Type: code completion              | 52.08    ±0.61 | 63.51%   ±0.75%  | 82.00      | 30.37%     
 Type: knowledge question-answering | 38.06    ±1.45 | 52.14%   ±1.99%  | 73.00      | 27.04%     
 Type: code debugging               | 44.67    ±0.72 | 62.04%   ±1.01%  | 72.00      | 26.67%     
 Type: non-code debugging           | 26.51    ±1.07 | 61.65%   ±2.49%  | 43.00      | 15.93%     
 Metric: keywords                   | 109.41   ±2.96 | 64.32%   ±1.74%  | 170.10     | 63.00%     
 Metric: unit_test                  | 34.17    ±0.58 | 66.99%   ±1.13%  | 51.00      | 18.89%     
 Metric: blank_filling              | 14.93    ±0.12 | 45.25%   ±0.35%  | 33.00      | 12.22%     
 Metric: similarity                 | 8.26     ±0.14 | 25.82%   ±0.45%  | 32.00      | 11.85%     
--------------------------------------------------------------------------------------------------
```

- Dev set:

Command:
```bash
python3 print_result_stat.py results/suite_v2.0.0_dev_gpt-4_0.2_0.9_30_suite_v2.0.0_dev.yaml example_table_gpt-4.txt --model_name gpt-4
```

Output: (dev score 61.03% ± 1.39%)
```bash
[80.49660549928024, 84.25483084597717, 82.42070024848911]
Write to example_table_gpt-4.txt
Final Result:
-------------------------------------------------------------------------------------------------
                                    | gpt-4         |                  | Full Score | Allocation 
------------------------------------|-------|-------|--------|---------|------------|------------
 Overall Score                      | 82.39   ±1.88 | 61.03%   ±1.39%  | 135.00     |            
 Lang: python                       | 14.50   ±0.87 | 60.42%   ±3.61%  | 24.00      | 17.78%     
 Lang: javascript                   | 17.17   ±0.64 | 78.03%   ±2.92%  | 22.00      | 16.30%     
 Lang: bash                         | 5.72    ±0.42 | 57.22%   ±4.19%  | 10.00      | 7.41%      
 Lang: java                         | 6.22    ±0.06 | 69.12%   ±0.64%  | 9.00       | 6.67%      
 Lang: dart                         | 3.43    ±0.58 | 38.15%   ±6.42%  | 9.00       | 6.67%      
 Lang: c#                           | 2.33    ±0.58 | 38.89%   ±9.62%  | 6.00       | 4.44%      
 Lang: css                          | 3.42    ±0.38 | 68.44%   ±7.70%  | 5.00       | 3.70%      
 Lang: html                         | 4.00    ±0.00 | 80.00%   ±0.00%  | 5.00       | 3.70%      
 Lang: r                            | 3.17    ±0.58 | 63.33%   ±11.55% | 5.00       | 3.70%      
 Lang: rust                         | 3.50    ±0.33 | 70.00%   ±6.67%  | 5.00       | 3.70%      
 Lang: c++/c                        | 3.33    ±0.76 | 66.67%   ±15.28% | 5.00       | 3.70%      
 Lang: php                          | 3.00    ±0.00 | 60.00%   ±0.00%  | 5.00       | 3.70%      
 Lang: go                           | 4.33    ±0.00 | 86.67%   ±0.00%  | 5.00       | 3.70%      
 Lang: ruby                         | 3.92    ±0.00 | 78.33%   ±0.00%  | 5.00       | 3.70%      
 Lang: kotlin                       | 1.50    ±0.00 | 30.00%   ±0.00%  | 5.00       | 3.70%      
 Lang: swift                        | 1.68    ±0.09 | 33.62%   ±1.89%  | 5.00       | 3.70%      
 Lang: vba                          | 1.16    ±0.04 | 23.23%   ±0.71%  | 5.00       | 3.70%      
 Type: code completion              | 30.17   ±1.00 | 70.16%   ±2.33%  | 43.00      | 31.85%     
 Type: knowledge question-answering | 21.46   ±0.81 | 53.64%   ±2.03%  | 40.00      | 29.63%     
 Type: code debugging               | 18.95   ±1.71 | 57.43%   ±5.17%  | 33.00      | 24.44%     
 Type: non-code debugging           | 11.82   ±0.76 | 62.19%   ±4.02%  | 19.00      | 14.07%     
 Metric: keywords                   | 48.48   ±2.64 | 63.79%   ±3.47%  | 76.00      | 56.30%     
 Metric: unit_test                  | 17.50   ±1.00 | 64.81%   ±3.70%  | 27.00      | 20.00%     
 Metric: blank_filling              | 11.35   ±0.12 | 63.06%   ±0.64%  | 18.00      | 13.33%     
 Metric: similarity                 | 5.90    ±0.07 | 32.76%   ±0.38%  | 18.00      | 13.33%     
-------------------------------------------------------------------------------------------------
```

Command:
```bash
python3 print_result_stat.py results/suite_v2.0.0_dev_gpt-3.5-turbo_0.2_0.9_30_suite_v2.0.0_dev.yaml example_table_gpt-3.5-turbo.txt --model_name gpt-3.5-turbo
```

Output: (dev score 46.45% ± 0.88%)

```bash
[62.23807707366633, 61.832625454308975, 64.06869518783614]
Write to example_table_gpt-3.5-turbo.txt
Final Result:
--------------------------------------------------------------------------------------------------------
                                    | gpt-3.5-turbo         |                 | Full Score | Allocation 
------------------------------------|---------------|-------|--------|--------|------------|------------
 Overall Score                      | 62.71           ±1.19 | 46.45%   ±0.88% | 135.00     |            
 Lang: python                       | 10.47           ±1.15 | 43.61%   ±4.81% | 24.00      | 17.78%     
 Lang: javascript                   | 12.73           ±0.60 | 57.88%   ±2.73% | 22.00      | 16.30%     
 Lang: bash                         | 3.96            ±0.56 | 39.64%   ±5.58% | 10.00      | 7.41%      
 Lang: java                         | 4.33            ±0.29 | 48.15%   ±3.21% | 9.00       | 6.67%      
 Lang: dart                         | 1.90            ±0.00 | 21.11%   ±0.00% | 9.00       | 6.67%      
 Lang: c#                           | 2.06            ±0.29 | 34.35%   ±4.81% | 6.00       | 4.44%      
 Lang: css                          | 1.33            ±0.35 | 26.67%   ±7.06% | 5.00       | 3.70%      
 Lang: html                         | 3.40            ±0.00 | 68.00%   ±0.00% | 5.00       | 3.70%      
 Lang: r                            | 2.50            ±0.00 | 50.00%   ±0.00% | 5.00       | 3.70%      
 Lang: rust                         | 3.17            ±0.00 | 63.33%   ±0.00% | 5.00       | 3.70%      
 Lang: c++/c                        | 3.17            ±0.29 | 63.33%   ±5.77% | 5.00       | 3.70%      
 Lang: php                          | 2.89            ±0.19 | 57.78%   ±3.85% | 5.00       | 3.70%      
 Lang: go                           | 4.22            ±0.38 | 84.44%   ±7.70% | 5.00       | 3.70%      
 Lang: ruby                         | 2.19            ±0.42 | 43.89%   ±8.39% | 5.00       | 3.70%      
 Lang: kotlin                       | 1.25            ±0.04 | 24.90%   ±0.81% | 5.00       | 3.70%      
 Lang: swift                        | 1.83            ±0.17 | 36.69%   ±3.42% | 5.00       | 3.70%      
 Lang: vba                          | 1.30            ±0.15 | 26.05%   ±2.94% | 5.00       | 3.70%      
 Type: code completion              | 22.20           ±1.53 | 51.63%   ±3.55% | 43.00      | 31.85%     
 Type: knowledge question-answering | 18.75           ±0.68 | 46.87%   ±1.70% | 40.00      | 29.63%     
 Type: code debugging               | 13.98           ±0.51 | 42.37%   ±1.54% | 33.00      | 24.44%     
 Type: non-code debugging           | 7.78            ±0.50 | 40.96%   ±2.63% | 19.00      | 14.07%     
 Metric: keywords                   | 37.67           ±0.71 | 49.56%   ±0.93% | 76.00      | 56.30%     
 Metric: unit_test                  | 13.87           ±1.15 | 51.36%   ±4.28% | 27.00      | 20.00%     
 Metric: blank_filling              | 7.38            ±0.87 | 41.02%   ±4.81% | 18.00      | 13.33%     
 Metric: similarity                 | 4.63            ±0.15 | 25.72%   ±0.82% | 18.00      | 13.33%     
--------------------------------------------------------------------------------------------------------
```

#### Where are prompts and evaluation criteria?

If you are curious about the questions and evaluation criteria in the benchmark,
all the benchmark dev set prompts are available at `batched_prompts/suite_v2.0.0_dev.csv` (csv format) or `batched_prompts/suite_v2.0.0_dev.parquet` (parquet format) or `cases_dev/prompt*.txt` (pure text format).

The evaluation criteria are decoded in `cases_dev/eval*.yaml` files, some may have link to reference answers or checkers in the same directory.

## Future

We plan to integrate this evaluation framework into [The BigCode Evaluation Farness Framework](https://github.com/bigcode-project/bigcode-evaluation-harness) --- feel free to contact [us](mailto:linyi2@illinois.edu) if you are happy to contribute!

## Acknowledgements

Some components of this framework is built upon:

- https://huggingface.co/spaces/Muennighoff/code_eval_octopack

- https://huggingface.co/spaces/evaluate-metric/rouge

(The required components have been copied into this repo --- no need to download them separately any more.)

The execution environment is partly adapted from Humanevalpack: https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/lm_eval/tasks/humanevalpack.py.

## Cite as

```
@misc{li2023inficodereval,
  author = {InfiCoderTeam},
  title = {InfiCoder-Eval: Systematically Evaluating Question-Answering for Code Large Language Models},
  year = {2023},
  publisher = {Github Pages},
  howpublished = "\url{https://infi-coder.github.io/inficoder-eval/}"
}
```