"""
    Packing all cases within a suite into a CSV file
    Example usage:
        python3 adaptors/whole_suite_packer.py suite_v2.1.yaml ../suite_v2.1_data.csv
"""
import os
import os.path as osp
import argparse
import yaml
import json
import pandas as pd

def search_for_dependency(spec):
    if isinstance(spec, dict):
        if 'module' in spec and 'func' in spec:
            # something like post_handler
            # trim the "cases." prefix
            module_name = spec['module']
            if module_name.startswith('cases.'):
                module_name = module_name[len('cases.'):]
            module_name = module_name.replace('.', '/')
            return [module_name + '.py']
        if 'tests' in spec:
            # unit test
            ret = []
            for test in spec['tests']:
                if 'path' in test:
                    ret.append(test['path'])
                if 'prefix_path' in test:
                    ret.append(test['prefix_path'])
                if 'cleanup_path' in test:
                    ret.append(test['cleanup_path'])
            return ret
        if 'references' in spec:
            ret = []
            for item in spec['references']:
                if isinstance(item, dict) and item['path']:
                    ret.append(item['path'])
            return ret
        return [item for lst in spec.values() for item in search_for_dependency(lst)]
    elif isinstance(spec, list):
        return [item for lst in spec for item in search_for_dependency(lst)]
    else:
        return []

parser = argparse.ArgumentParser()
parser.add_argument('suite_path', type=str, help='Suite yaml file path')
parser.add_argument('output_path', type=str, help='The output CSV file containing all cases with their dependencies')
if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.suite_path, 'r') as f:
        suite_data = yaml.load(f, yaml.Loader)
    case_paths = suite_data['cases']

    tot_deps = 0

    data = []
    for i, case_path in enumerate(case_paths):
        now_data = {
            'no': i,
            'case_path': case_path,
            'prompt': None,
            'eval_spec': None,
            'dependencies': None
        }
        dependencies = {}
        with open(osp.join(osp.dirname(args.suite_path), case_path), 'r') as f:
            eval_spec_str = f.read()
        eval_spec = yaml.safe_load(eval_spec_str)
        prompt_path = eval_spec['prompt_path']
        case_rootdir = osp.dirname(osp.join(osp.dirname(args.suite_path), case_path))
        with open(osp.join(case_rootdir, prompt_path), 'r') as f:
            prompt = f.read()
        now_data['prompt'] = prompt
        now_data['eval_spec'] = eval_spec_str

        dependent_files = search_for_dependency(eval_spec)
        dependencies = {}
        for k in dependent_files:
            with open(osp.join(case_rootdir, k), 'r') as f:
                dependencies[k] = f.read()
        now_data['dependencies'] = json.dumps(dependencies)
        print(f'.  [{i:04d}] {len(dependencies)} dependent files')
        tot_deps += len(dependencies)
        if len(dependent_files):
            print(dependent_files)

        data.append(now_data)
    
    data = pd.DataFrame(data, index=None)
    data.to_csv(args.output_path)
    print(f'{len(data)} data items with {tot_deps} dependent files dumped to {args.output_path}')
        

    pass

