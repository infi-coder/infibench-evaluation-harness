<h1 align="center">Inference for InfiCoder-Eval</h1>

<h4 align="center">The InfiCoder Team</h4>

<h4 align="center">(Forked from <a href="https://github.com/bigcode-project/bigcode-evaluation-harness">Code Generation LM Evaluation Harness</a>)</h4>


<h4 align="center">
    <p>
        <a href="#features">Features</a> |
        <a href="#usage">Usage</a> |
        <a href="#implementing-new-tasks">Contribution</a>
    <p>
</h4>

## Features
This is a very lightweight fork of bigcode-evaluation-harness to support inference on InfiCoder-Eval benchmark prompts.

The setup process and prerequisite are the same as the original bigcode-evaluation-harness framework. There are only some minor changes to the original code (e.g., support `max_new_tokens` and always `use_cache` in generation) along with InfiCoder-Eval tasks added.

New tasks for InfiCoder-Eval:

- code-ffqa-v2 

    The default one, prompt with `system_prompt + '\n' + content_prompt`.
    
- code-ffqa-v2-endn

    Prompt with `system_prompt + '\n' + content_prompt + '\n'`.

- code-ffqa-v2-deepseek-chat 

    deepseek-coder-instruct format

- code-ffqa-v2-baichuan2
    
    baichuan2 models format 

- code-ffqa-v2-zypher

    zypher-7b-beta format

- code-ffqa-v2-octo 

    octopack model format

- code-ffqa-v2-wizard

    wizard-python model format

- code-ffqa-v2-phi 
    
    phi-1.5 model format

- code-ffqa-v2-inficoder

    Our InfiCoder model format

For detail information, please visit [InfiCoder-Eval](https://infi-coder.github.io/inficoder-eval/).

## Usage

For InfiCoder-Eval, **we only use this framework for response generation**. The actual evaluation is delegated to our [Evaluation Repo](https://github.com/infi-coder/inficoder-eval-framework), which can be deployed in the same instance or another one.

An example usage can be found in `run.sh`:

```bash
# This shell exemplifies how to run the inference for inficoder-eval with this repo
# see detailed instructions in https://infi-coder.github.io/inficoder-eval/

export DATASET_CSV_PATH=..../inficoder-eval-framework/batched_prompts/suite_v2.0.0_dev.csv

# for example, to evaluate Phi-1.5
# first, generate responses
accelerate launch ..../ffqa-evaluation-harness/main.py --model microsoft/phi-1_5 --tasks code-ffqa-v2-phi --batch_size 16 --precision bf16 --n_samples 30 --do_sample True --temperature 0.2 --top_p 0.9 --save_generations --save_references --trust_remote_code --generation_only --max_length_generation 2048 --save_generations_path generations_phi-1_5.json --eos='<|endoftext|>'

# then, join with case names and output a csv file, later the evaluation framework can process
python3 ffqa_processor.py generations_phi-1_5.json references.json ../phi-1_5_output.csv --eos '<|endoftext|>'
```

Detail illustration is in [Evaluation Repo](https://github.com/infi-coder/inficoder-eval-framework).


## Implementing new tasks
To implement a new task or prompting method for our InfiCoder-Eval, please read and modify here: `bigcode_eval/tasks/code_ffqa_v200.py`. For generic task extensions, see the guide in [`docs/guide`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/docs/guide.md). The are also contribution guidelines in this [`CONTRIBUTING.md`](https://github.com/bigcode-project/bigcode-evaluation-harness/blob/main/CONTRIBUTING.md)

In the long term, we plan to integrate InfiCoder-Eval [evaluation framework](https://github.com/infi-coder/inficoder-eval-framework) into this repo and merge this benchmark into the official bigcode-evaluation-harness. If you are interested in this effort, you are more than welcome to [contact us](mailto:linyi2@illinois.edu)!

## Acknowledgements
We thank the BigCode team for developing such a great framework and EleutherAI for their work on the [lm-evaluation harness](https://github.com/EleutherAI/lm-evaluation-harness) from which this repository is built upon.

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
