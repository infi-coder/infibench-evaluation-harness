# Infernece and evaluation: take code-gemma-7b-it as an example
# If it runs smoothly, the outcome score should be 52.43% ±1.19%

export MODEL_NAME="google/codegemma-7b-it"
export SAVE_NAME=$(echo "$MODEL_NAME" | tr '/' '_') # avoid hierarchical folder creation
export DATASET_CSV_PATH=/opt/tiger/open-freeform-code-qa-suite/batched_prompts/suite_v2.0.0.csv

# for monitoring gpu usage
pip install gpustat
# for qwen models
pip install transformers==4.40.0 accelerate tiktoken einops scipy transformers_stream_generator==0.0.4 peft

cd /opt/tiger/bigcode-evaluation-harness

set -e # Optional, set to interrupt the script execution when error occurs, to ensure result reliability
mv -f /usr/bin/node /usr/bin/node_old # these mv's and ln's make backups for the system's default nodejs environment. If they run with errors, just comment out
mv -f /usr/bin/npm /usr/bin/npm_old
mv -f /usr/bin/npx /usr/bin/npx_old
ln -s /usr/local/nvm/versions/node/v16.15.1/bin/node /usr/bin/node
ln -s /usr/local/nvm/versions/node/v16.15.1/bin/npm /usr/bin/npm
ln -s /usr/local/nvm/versions/node/v16.15.1/bin/npx /usr/bin/npx
bash bigcode_eval/infibench/setup.sh # main script for environment installation
export NODE_PATH=$(npm root --quiet -g)
pip install -r requirements.txt
python3 bigcode_eval/infibench/env_check.py

n=0
until [ "$n" -ge 5 ] # try 5 times
do
    accelerate launch --main_process_port 25768 /opt/tiger/bigcode-evaluation-harness/main.py --model ${MODEL_NAME} --tasks code-ffqa-v2-codegemma --batch_size 2 --n_samples 30 --do_sample True --temperature 0.2 --top_p 0.9 --save_generations --save_references --trust_remote_code --generation_only --max_new_tokens 1024 --save_generations_path generations_${SAVE_NAME}.json --eos '<eos>' --use_auth_token
    exit_status=$?
    echo $exit_status
    if [ $exit_status -eq 0 ]; then
        break
    fi
    n=$((n+1)) 
    sleep 120
done
python3 infibench_infer_post_processor.py generations_${SAVE_NAME}.json references.json /mnt/bn/codegeniusgen1/inficoder-eval/open-source/responses/${SAVE_NAME}_output.csv --eos '<eos>'

python3 bigcode_eval/infibench/grader_main.py bigcode_eval/infibench/suite_v2.1.yaml /mnt/bn/codegeniusgen1/inficoder-eval/open-source/responses/${SAVE_NAME}_output.csv --batched --batched_cases_path bigcode_eval/infibench/batched_cases/suite_v2.1_data.csv --result_detail_path results/suite_v2.1_model_to_test.yaml --result_summary_path results/suite_v2.1_model_to_test_table.txt
python3 bigcode_eval/infibench/print_result_stat.py results/suite_v2.1_model_to_test.yaml results/suite_v2.1_model_to_test_table.txt --model_name $MODEL_NAME --case_path_prefix bigcode_eval/infibench
cp results/suite_v2.1_model_to_test.yaml /mnt/bn/codegeniusgen1/inficoder-eval/open-source/results/v210_${SAVE_NAME}.yaml # Output 1: Score details at the case-level
cp results/suite_v2.1_model_to_test_table.txt /mnt/bn/codegeniusgen1/inficoder-eval/open-source/results/v210_${SAVE_NAME}_table.txt # Output 2：Overall score report table
echo "Output paths:"
echo "/mnt/bn/codegeniusgen1/inficoder-eval/open-source/results/v210_${SAVE_NAME}.yaml"
echo "/mnt/bn/codegeniusgen1/inficoder-eval/open-source/results/v210_${SAVE_NAME}_table.txt"
