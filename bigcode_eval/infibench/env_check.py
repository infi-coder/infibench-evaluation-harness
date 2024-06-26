import os
import subprocess
from tqdm import tqdm

command_to_check = [
    ['node --help', 'Need to install node.js properly -- please run apt-get install -y nodejs.'],
    ['node bigcode_eval/infibench/env_check_programs/test_jsdom.js', 'Need to install jsdom package for node.js -- please run npm install -g jsdom; export NODE_PATH=$(npm root --quiet -g)'],
    ['npx tsc bigcode_eval/infibench/env_check_programs/test_ts.ts --outfile env_check_programs/test_ts.js; rm env_check_programs/test_ts.js', 'Need to install TypeScript support for npm: npm install -g typescript.'],
    ['java -version', 'Need to install java SDK'],
    ['javac -version', 'Need to install java SDK'],
    ['g++ -v', 'Need to install C++ compiler (g++)'],
    ['g++ bigcode_eval/infibench/env_check_programs/test_cpp.cpp -o env_check_programs/test_cpp; ./env_check_programs/test_cpp; rm env_check_programs/test_cpp', 'Need to install some C++ libraries '],
    ['mcs --version', 'Need to install mono-complete for C# support in Ubuntu'],
    ['mono --version', 'Need to install mono-complete for C# support in Ubuntu'],
    ['go version', 'Need to install Go support in Ubuntu'],
    ["Rscript -e 'library(\"assert\")'", 'Need to install assert package or R engine'],
    ["Rscript -e 'library(\"stringr\")'", 'Need to install stringr package or R engine'],
    ["Rscript -e 'library(\"tidyverse\")'", 'Need to install tidyverse package or R engine'],
    ["Rscript -e 'library(\"dplyr\")'", 'Need to install dplyr package or R engine'],
    ["Rscript -e 'library(\"data.table\")'", 'Need to install data.table package or R engine'],
]

if __name__ == '__main__':
    failed = False
    for command, fail_msg in tqdm(command_to_check):
        exec_result = subprocess.run(command, shell=True, capture_output=True)
        if exec_result.returncode != 0:
            print(f'Fail in command {command} --- {fail_msg}')
            failed = True
    if failed:
        print('Please install the corresponding dependencies and try again.')
        exit(1)
    else:
        print("Env setup successfully!! You're good to go.")
        exit(0)

