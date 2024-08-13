
<h1 align="center">InfiBench: Evaluating the Question-Answering Capabilities of Code LLMs</h1>


<h4 align="center">The InfiCoder Team</h4>

<h4 align="center">
    <p><a href="https://infi-coder.github.io/infibench/">Website</a> |
    <a href="https://arxiv.org/abs/2404.07940">Report</a></p>
</h4>


<h4 align="center">
    <p>
        <a href="#features-and-tutorials">Features</a> |
        <a href="#setup">Setup</a> |
        <a href="#example">Example</a> |
        <a href="#extension">Extension</a>
    <p>
</h4>

## Features and Tutorials
This repo contains the full InfiBench benchmark including both benchmark data and evaluation code. The benchmark is designed to evaluate the question-answering capabilities of code language models. 

The benchmark is inspired by and forked from the [BigCode Evaluation Harness](https://github.com/bigcode-project/bigcode-evaluation-harness) framework, adding the following two main features:

1. **LLM Inference on All InfiBench Questions**

The InfiBench questions are stored [here](https://github.com/infi-coder/infibench-evaluation-harness/blob/main/bigcode_eval/infibench/batched_prompts/suite_v2.1.csv). We extend the framework with a series of new tasks [here](https://github.com/infi-coder/infibench-evaluation-harness/blob/main/bigcode_eval/tasks/code_ffqa_v200.py) to support the LLM inference on these questions, supporting varies prompting templates.

To conduct the model inference, one only needs to execute the following two commands in sequence:

````bash
# STEP 1: codegemma-7b-it inference as an example to conduct inference, output to the specified json file
accelerate launch --main_process_port 25768 \
 /opt/tiger/bigcode-evaluation-harness/main.py \
 --model google/codegemma-7b-it --tasks code-ffqa-v2-codegemma \
 --batch_size 2 --n_samples 30 \
 --do_sample True --temperature 0.2 \
 --top_p 0.9 --save_generations --save_references \
 --trust_remote_code --generation_only --max_new_tokens 1024 \
 --save_generations_path generations_codegemma.json --eos '<eos>' \
 --use_auth_token 
# STEP 2: join raw inference output with the case IDs, and output to the specified csv file, for better readabiltiy and subsequence evaluation
python3 infibench_infer_post_processor.py generations_codegemma.json references.json codegemma_output.csv --eos '<eos>' 
````

To support more prompt templates for your model, you only need to modify [bigcode_eval/tasks/code_ffqa_v200.py](https://github.com/infi-coder/infibench-evaluation-harness/blob/main/bigcode_eval/tasks/code_ffqa_v200.py) (and sometimes [infibench_infer_post_processor.py](https://github.com/infi-coder/infibench-evaluation-harness/blob/main/infibench_infer_post_processor.py) for customized post-processing like trimming).

*Note: The above Step 1 deploys data parallel on multiple GPUs for inference. For large LLMs (e.g., over 40B with A100-80GB GPU), a single GPU cannot run the inference and tensor partitioning is needed. In this case, we need to replace the step 1 command by `python3 /opt/tiger/bigcode-evaluation-harness/main.py ... --max_memory_per_gpu auto --reduce_batch_thres 2048`. Noticng that we discard `accelerate launch` to disable data parallel and use `max_memory_per_gpu` to activate the fsdp tensor partitioning. The `reduce_batch_thres 2048` will dynamically reduce the batch size when the input prompt length exceeds 2048 to avoid OOM.*

2. **Response Evaluation**

Given the responses, we provide the automatic evaluation tool, featuring the execution runtime for 8 languages (Python, Javascript, Java, C, C++, Go, R, C#). Given model responses, the tool directly evaluates and outputs the scores along with subscores in a nice table. Detail scores and runtime log are dumped to a yaml file for customized analysis.

To run the evaluation, we first need to setup the runtime environment correctly. We provide an example bash script [infibench_eval_example.sh](https://github.com/infi-coder/infibench-evaluation-harness/blob/main/infibench_eval_example.sh) where lines 1-24 setup the environment. Then we provide [bigcode_eval/infibench/env_check.py](https://github.com/infi-coder/infibench-evaluation-harness/blob/main/bigcode_eval/infibench/env_check.py) to check whether the environment is ready.

When it is ready, the evaluation is in one command:
````bash
# take the codegemma_output.csv response file as an example
python3 bigcode_eval/infibench/grader_main.py bigcode_eval/infibench/suite_v2.1.yaml codegemma_output.csv --batched --batched_cases_path bigcode_eval/infibench/batched_cases/suite_v2.1_data.csv --result_detail_path results_detail.yaml --result_summary_path result_summary.txt
````

The evaluation specification is in `bigcode_eval/infibench/batched_cases/suite_v2.1_data.csv`. The above command outputs to `results_detail.yaml` and `result_summary.txt`.

Then, we can print the result summary table in a nice table to stdout and `results_table.txt` by:
````bash
python3 bigcode_eval/infibench/print_result_stat.py results_detail.yaml results_table.txt --case_path_prefix bigcode_eval/infibench
````
Note that `--case_path_prefix bigcode_eval/infibench` is necessary since all cases are stored under the `bigcode_eval/infibench/cases` directory.

3. **Raw Evaluation Data**

The raw model responses of our evaluation presented in the website and the report can be found in [here](https://figshare.com/articles/dataset/InfiBench_Detail_Evaluation_Data/26104864).

## Setup

At this point, we only support Linux environment.

```bash
bash bigcode_eval/infibench/setup.sh # main script for environment installation
export NODE_PATH=$(npm root --quiet -g)
pip install -r requirements.txt
```

Then, you can run
```bash
python3 bigcode_eval/infibench/env_check.py
```
to check and fix the environment incompatibility according to the console output. If the console output is "`You're good to go.`", then we can proceed.

## Example

We provide an example bash script [infibench_eval_example.sh](https://github.com/infi-coder/infibench-evaluation-harness/blob/main/infibench_eval_example.sh) that integrates the [code-gemma-7b-it](https://huggingface.co/google/codegemma-7b-it) model inference and evaluation on InfiBench.

After the execution, in both stdout and `v210_${SAVE_NAME}_table.txt` table, you will find the evaluation result showing like the following table.

````
-----------------------------------------------------------------------------------------------------------------
                                    | google/codegemma-7b-it         |                 | Full Score | Allocation 
------------------------------------|------------------------|-------|--------|--------|------------|------------
 Overall Score                      | 122.36                   ±2.65 | 52.29%   ±1.13% | 234.00     |            
 Lang: python                       | 24.02                    ±1.18 | 51.11%   ±2.52% | 47.00      | 20.09%     
 Lang: javascript                   | 24.66                    ±0.84 | 56.04%   ±1.91% | 44.00      | 18.80%     
 Lang: dart                         | 5.18                     ±0.76 | 27.28%   ±4.02% | 19.00      | 8.12%      
 Lang: bash                         | 11.71                    ±1.22 | 61.63%   ±6.41% | 19.00      | 8.12%      
 Lang: java                         | 11.46                    ±0.58 | 67.43%   ±3.39% | 17.00      | 7.26%      
 Lang: c#                           | 5.06                     ±0.63 | 42.13%   ±5.26% | 12.00      | 5.13%      
 Lang: css                          | 4.76                     ±0.19 | 47.56%   ±1.92% | 10.00      | 4.27%      
 Lang: rust                         | 4.28                     ±0.42 | 42.78%   ±4.19% | 10.00      | 4.27%      
 Lang: c++/c                        | 5.17                     ±0.58 | 51.67%   ±5.77% | 10.00      | 4.27%      
 Lang: ruby                         | 6.00                     ±0.00 | 60.00%   ±0.00% | 10.00      | 4.27%      
 Lang: html                         | 5.29                     ±0.34 | 58.77%   ±3.80% | 9.00       | 3.85%      
 Lang: r                            | 4.17                     ±0.58 | 46.30%   ±6.42% | 9.00       | 3.85%      
 Lang: php                          | 5.17                     ±0.44 | 57.41%   ±4.90% | 9.00       | 3.85%      
 Lang: go                           | 5.44                     ±0.19 | 60.49%   ±2.14% | 9.00       | 3.85%      
 Type: code completion              | 42.76                    ±0.40 | 57.78%   ±0.54% | 74.00      | 31.62%     
 Type: code debugging               | 30.33                    ±2.11 | 48.14%   ±3.35% | 63.00      | 26.92%     
 Type: knowledge question-answering | 28.98                    ±0.67 | 52.69%   ±1.22% | 55.00      | 23.50%     
 Type: non-code debugging           | 20.29                    ±1.02 | 48.31%   ±2.42% | 42.00      | 17.95%     
 Metric: keywords                   | 82.40                    ±2.93 | 48.78%   ±1.73% | 168.93     | 72.19%     
 Metric: unit_test                  | 28.37                    ±0.12 | 56.73%   ±0.23% | 50.00      | 21.37%     
 Metric: blank_filling              | 10.88                    ±0.00 | 41.86%   ±0.00% | 26.00      | 11.11%     
 Metric: similarity                 | 2.87                     ±0.40 | 47.88%   ±6.74% | 6.00       | 2.56%      
-----------------------------------------------------------------------------------------------------------------
````

The final score we reported is `52.29%±1.13%`.

## Extension

The framework can be easily expanded and we welcome any extension!

- Expand the code framework:

Besides the inference extension code, which lies in `bigcode_eval/tasks/code_ffqa_v200.py`. All code is located in `bigcode_eval/infibench`. We have core code in `bigcode_eval/infibench/*.py`, and some optional components in sub-folders, e.g., result analysis code in `bigcode_eval/infibench/analyze`.

- Expand the question set:

The question prompts are batched in `bigcode_eval/infibench/batched_prompts`. The whole question, including prompts, evaluation standards, and dependency files are batched in `bigcode_eval/infibench/batched_cases` and unfolded in `bigcode_eval/infibench/cases`.

The batched cases can also be found at https://huggingface.co/datasets/llylly001/InfiBench/blob/main/suite_v2.1_data.csv.


## Acknowledgements

Some components of this framework is built upon:

- https://huggingface.co/spaces/Muennighoff/code_eval_octopack

- https://huggingface.co/spaces/evaluate-metric/rouge

(The required components have been copied into this repo --- no need to download them separately any more.)

The execution environment is partly adapted from Humanevalpack: https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/lm_eval/tasks/humanevalpack.py.

The repo is forked the `main` branch of Jun 25 2024 version of `bigcode-evaluation-harness`.
Below is the original README.md content from the repo.

---

<h1 align="center">Code Generation LM Evaluation Harness</h1>


<h4 align="center">
    <p>
        <a href="https://huggingface.co/bigcode">BigCode</a>
    <p>
</h4>

<h3 align="center">
    <img style="float: middle; padding: 10px 10px 10px 10px;" width="50" height="50" src="https://user-images.githubusercontent.com/44069155/191557209-6219acb8-a766-448c-9bd6-284d22b1e398.png" /></a>
</h3>

## Features

This is a framework for the evaluation of code generation models. This work is inspired from [EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) for evaluating language models in general. We welcome contributions to fix issues, enhance features and add new benchmarks. You can find contribution guides in [`docs/guide.md`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/docs/guide.md) and [`CONTRIBUTING.md`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/CONTRIBUTING.md) and more documentation in [`docs/README.md`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/docs/README.md). 

Below are the features and tasks of this framework:

- Features:
    - Any autoregressive model available on [Hugging Face hub](https://huggingface.co/) can be used, but we recommend using code generation models trained specifically on Code such as [SantaCoder](https://huggingface.co/bigcode/santacoder), [InCoder](https://huggingface.co/facebook/incoder-6B) and [CodeGen](https://huggingface.co/Salesforce/codegen-16B-mono).
    - We provide Multi-GPU text generation with `accelerate` and Dockerfiles for evaluating on Docker containers for security and reproducibility.

- Tasks:
    - 7 code generation **Python** tasks (with unit tests): [HumanEval](https://huggingface.co/datasets/openai_humaneval), [HumanEval+](https://huggingface.co/datasets/evalplus/humanevalplus), [InstructHumanEval](https://huggingface.co/datasets/codeparrot/instructhumaneval), [APPS](https://huggingface.co/datasets/codeparrot/apps), [MBPP](https://huggingface.co/datasets/mbpp), [MBPP+](https://huggingface.co/datasets/evalplus/mbppplus), and [DS-1000](https://github.com/HKUNLP/DS-1000/) for both completion (left-to-right) and insertion (FIM) mode.
    - [HumanEvalPack](https://huggingface.co/datasets/bigcode/humanevalpack) extends HumanEval to **3** scenarios across **6** languages via human translations and was released with [OctoPack](https://arxiv.org/abs/2308.07124).
    - [MultiPL-E](https://github.com/nuprl/MultiPL-E) evaluation suite (HumanEval translated into **18** programming languages).
    - [Recode](https://github.com/amazon-science/recode/tree/main) applied to the HumanEval benchmark. It evaluates the robustness of code-generation models.
    - [Pal](https://github.com/reasoning-machines/pal) Program-aided Language Models evaluation for grade school math problems : [GSM8K](https://huggingface.co/datasets/gsm8k) and [GSM-HARD](https://huggingface.co/datasets/reasoning-machines/gsm-hard). These problems are solved by generating reasoning chains of text and code.
    - Code to text task from [CodeXGLUE](https://huggingface.co/datasets/code_x_glue_ct_code_to_text) (zero-shot & fine-tuning) for 6 languages: **Python, Go, Ruby, Java, JavaScript and PHP.**  Documentation translation task from [CodeXGLUE](https://huggingface.co/datasets/code_x_glue_tt_text_to_text).
    - [CoNaLa](https://huggingface.co/datasets/neulab/conala) for **Python** code generation (2-shot setting and evaluation with BLEU score).
    - [Concode](https://huggingface.co/datasets/code_x_glue_tc_text_to_code) for **Java** code generation (2-shot setting and evaluation with BLEU score).
    - 3 multilingual downstream classification tasks: [Java Complexity prediction](https://huggingface.co/datasets/codeparrot/codecomplex), [Java code equivalence prediction](https://huggingface.co/datasets/code_x_glue_cc_clone_detection_big_clone_bench), [C code defect prediction](https://huggingface.co/datasets/code_x_glue_cc_defect_detection).
    - [SantaCoder-FIM](https://huggingface.co/datasets/bigcode/santacoder-fim-task) for evaluating FIM on **Python** code using Exact Match. Further details are described in [SantaCoder](https://arxiv.org/abs/2301.03988). Includes two tasks:
        - `StarCoderFIM`: which uses the default FIM tokens `"<fim_prefix>", "<fim_middle>", "<fim_suffix>"`, and
        - `SantaCoderFIM`: which uses SantaCoder FIM tokens `"<fim-prefix>", "<fim-middle>", "<fim-suffix>"`
    - [Mercury](https://huggingface.co/datasets/Elfsong/Mercury) for evaluating computational efficiency of **Python** code generation.

More details about each task can be found in  the documentation in [`docs/README.md`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/docs/README.md).
## Setup

```bash
git clone https://github.com/bigcode-project/bigcode-evaluation-harness.git
cd bigcode-evaluation-harness
```
Install [`torch`](https://pytorch.org/get-started/locally/) based on your device type, and install the other packages using:
```
pip install -e .
```
To run the `DS-1000` benchmark, additional constraints must be resolved.
```
# python version must be 3.7.10
pip install -e ".[ds1000]" # installs all additional dependencies except PyTorch
# torch==1.12.1 required. Download version with relevant GPU support etc., e.g.,
pip install torch==1.12.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116

# to suppress any tensorflow optimization warnings, 
# precede call to "accelerate launch" with "TF_CPP_MIN_LOG_LEVEL=3"

# on some systems, tensorflow will attempt to allocate all GPU memory
# to its process at import which will raise a CUDA out-of-memory error
# setting "export TF_FORCE_GPU_ALLOW_GROWTH=true" resolves this
```
Also make sure you have `git-lfs` installed and are logged in the Hub
```
huggingface-cli login
````

We use [`accelerate`](https://huggingface.co/docs/accelerate/index) to generate code/text in parallel when multiple GPUs are present (multi-GPU mode). You can configure it using:

accelerate config



This evaluation harness can also be used in an evaluation only mode, you can use a Multi-CPU setting. For large models, we recommend specifying the precision of the model using the `--precision` flag instead of accelerate config to have only one copy of the model in memory. You can also load models in 8bit with the flag `--load_in_8bit` or 4bit with `--load_in_4bit` if you have `bitsandbytes` installed with the required transformers and accelerate versions.

The evaluation part (solutions execution) for [MultiPL-E](https://github.com/nuprl/MultiPL-E) requires extra dependencies for some programming languages, we provide a Dockerfile with all dependencies, see section [Docker](#docker-containers) for more details.

## Usage
You can use this evaluation harness to generate text solutions to code benchmarks with your model, to evaluate (and execute) the solutions or to do both. While it is better to use GPUs for the generation, the evaluation only requires CPUs. So it might be beneficial to separate these two steps. By default both generation and evaluation are performed.

For more details on how to evaluate on the tasks, please refer to the documentation in [`docs/README.md`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/docs/README.md). 

### Generation and evaluation
Below is an example to generate and evaluate on a task.

accelerate launch  main.py \
  --model <MODEL_NAME> \
  --tasks <TASK_NAME> \
  --limit <NUMBER_PROBLEMS> \
  --max_length_generation <MAX_LENGTH> \
  --temperature <TEMPERATURE> \
  --do_sample True \
  --n_samples 100 \
  --batch_size 10 \
  --precision <PRECISION> \
  --allow_code_execution \
  --save_generations


* `limit` represents the number of problems to solve, if it's not provided all problems in the benchmark are selected. 
* `allow_code_execution` is for executing the generated code: it is off by default, read the displayed warning before calling it to enable execution. 
* Some models with custom code on the HF hub like [SantaCoder](https://huggingface.co/bigcode/santacoder) require calling `--trust_remote_code`, for private models add `--use_auth_token`.
* `save_generations` saves the post-processed generations in a json file at `save_generations_path` (by default `generations.json`). You can also save references by calling `--save_references`
* `max_length_generation` is the maximum token length of generation including the input token length. The default is 512, but for some tasks like GSM8K and GSM-Hard, the complete prompt with 8 shot examples (as used in [PAL](https://github.com/reasoning-machines/pal)) take up `~1500` tokens, hence the value should be greater than that and the recommended value of `max_length_generation` is `2048` for these tasks.

Some tasks don't require code execution such as
`codexglue_code_to_text-<LANGUAGE>`/`codexglue_code_to_text-python-left`/`conala`/`concode` that use BLEU evaluation. In addition, we generate one candidate solution for each problem in these tasks, so use `n_samples=1` and `batch_size=1`. (Note that `batch_size` should always be equal or less than `n_samples`).
* For APPS tasks, you can use `n_samples=1` for strict and average accuracies (from the original APPS paper) and `n_samples>1` for pass@k.

### Generation only

If you want to generate solutions without executing and evaluating the code, call `--generation_only`, in addition to the instructions above. This will save the solutions in a json file provided in `save_generation_path` in the working directory. 

This can be useful if you don't want to execute code in the machine you're using for generations for security or efficiency reasons. For instance, you can do the generations on multiple GPUs, but switch to a multiple workers CPU machine or docker container for the execution.

### Evaluation only

If you already have the generations in a json file from this evaluation harness and want to evaluate them, specify the path of the generations via the `load_generations_path` argument. You may need to reconfigure `accelerate` to use multiple CPUs.

Below is an example, be mind of specifying arguments proper to the task you are evaluating on, and note that `model` value here only serves for documenting the experiment. Also add `--n_samples` to specify the number of samples to evaluate per problem (usually the same value used in generation).


accelerate launch  main.py   --tasks mbpp  --allow_code_execution  --load_generations_path generations.json  --model incoder-temperature-08


## Docker containers
For safety, we provide a Dockerfiles to do the execution inside a docker container. To do that, first, do the generation on your machine and save them in `generations.json` for example by adding the flag `--generation_only` to the command. Then use the Docker image that we provide:

````
$ docker pull ghcr.io/bigcode-project/evaluation-harness
$ docker tag ghcr.io/bigcode-project/evaluation-harness evaluation-harness
````

If you want to evaluate on MultiPL-E, we have a different Dockerfile since it requires more dependencies, use:
````bash
$ docker pull ghcr.io/bigcode-project/evaluation-harness-multiple
$ docker tag ghcr.io/bigcode-project/evaluation-harness-multiple evaluation-harness-multiple
````


### Building  Docker images

If you modify the evaluation harness, you may want to rebuild the docker images.

Here's how to build a docker image for the evaluation harness:
````bash
$ sudo make DOCKERFILE=Dockerfile  all
````
This creates an image called `evaluation-harness`, and runs a test on it. To skip the test remove `all` form the command.

For MultiPL-E:
````bash
$ sudo make DOCKERFILE=Dockerfile-multiple all
````
This creates an image called `evaluation-harness-multiple`.

### Evaluating inside a container
Suppose you generated text with the `bigcode/santacoder` model and saved it in `generations_py.json` with:
````bash
accelerate launch  main.py \
    --model bigcode/santacoder  \
    --tasks multiple-py  \
    --max_length_generation 650 \
    --temperature 0.8   \
    --do_sample True  \
    --n_samples 200  \
    --batch_size 200  \
    --trust_remote_code \
    --generation_only \
    --save_generations \
    --save_generations_path generations_py.json
````

To run the container (here from image `evaluation-harness-multiple`) to evaluate on `generations_py.json`, or another file mount it with `-v`, specify `n_samples` and allow code execution with `--allow_code_execution` (and add the number of problems `--limit`  if it was used during generation):
````bash
$ sudo docker run -v $(pwd)/generations_py.json:/app/generations_py.json:ro -it evaluation-harness-multiple python3 main.py \
    --model bigcode/santacoder \
    --tasks multiple-py \
    --load_generations_path /app/generations_py.json \
    --allow_code_execution  \
    --temperature 0.8 \
    --n_samples 200
````

## Implementing new tasks
To implement a new task in this evaluation harness, see the guide in [`docs/guide`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/docs/guide.md). The are also contribution guidelines in this [`CONTRIBUTING.md`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/CONTRIBUTING.md)

## Documentation
We provide documentation for the existing benchmarks and how to run the evaluation in [`docs/README.md`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/docs/README.md).

## Remarks
* Currenltly, we use data parallel evaluation across multiple GPUs using `accelerate`, this assumes that you can fit the model in one GPU. 

## Acknowledgements
We thank EleutherAI for their work on the [lm-evaluation harness](https://github.com/EleutherAI/lm-evaluation-harness) from which this repository is inspired.

## Cite as

````
@misc{bigcode-evaluation-harness,
  author       = {Ben Allal, Loubna and
                  Muennighoff, Niklas and
                  Kumar Umapathi, Logesh and
                  Lipkin, Ben and
                  von Werra, Leandro},
  title = {A framework for the evaluation of code generation models},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/bigcode-project/bigcode-evaluation-harness}},
  year = 2022,
}
````
