# Code freeform QA dataset v2.0.0
"""
TODO: Add the Paper Title on this line.
TODO: Add the paper's PDF URL (preferably from arXiv) on this line.

TODO: Write a Short Description of the task.

Homepage: https://infi-coder.github.io/inficoder-eval
"""
from bigcode_eval.base import Task
from bigcode_eval.tasks.custom_metrics.code_eval import compute_code_eval


# TODO: Add the BibTeX citation for the task.
_CITATION = """
"""

def create_all_tasks():
    """Creates a dictionary of tasks from a list of levels
    :return: {task_name: task}
        e.g. {multiple-py: Task, multiple-java: Task}
    """
    return {"code-ffqa-v2":                    create_task('\n'), 
            "code-ffqa-v2-no-n":               create_task(''), 
            "code-ffqa-v2-endn":               create_task('\n', True), 
            "code-ffqa-v2-qwen-chat":          create_task('\n', False, True),
            "code-ffqa-v2-deepseek-chat":      create_task('\n', False, False, True), # this is indeed for deepseek-coder-instruct
            "code-ffqa-v2-baichuan2":          create_task('\n', False, False, False, True),
            "code-ffqa-v2-zypher":             create_task('\n', False, False, False, False, True),
            "code-ffqa-v2-octo":               create_task('\n', False, False, False, False, False, True),
            "code-ffqa-v2-wizard":             create_task('\n', False, False, False, False, False, False, True),
            "code-ffqa-v2-phi":                create_task('\n', False, False, False, False, False, False, False, True),
            "code-ffqa-v2-inficoder":          create_task('\n', False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-internlm":           create_task('\n', False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-magicoder":          create_task('\n', False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-mixtral_moe":        create_task('\n', False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-phi2":               create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-chatglm3":           create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-llama2":             create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-deepseek-chat-real": create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True), # this is the real deepseek-chat
            "code-ffqa-v2-gemma-it":           create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-starcoder2-instruct":create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-llama3"             :create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False),
            "code-ffqa-v2-llama3-instruct"    :create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-qwen2-chat":         create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-deepseek-coder-v2"  :create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True),
            "code-ffqa-v2-codegemma":          create_task('\n', False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True),
            }

def create_task(concate_sys_prompt, end_with_n=False, qwen_chat=False, deepseek_instruct=False, baichuan2=False, zypher=False, 
                octo=False, wizard=False, phi=False, inficoder=False, internlm=False, magicoder=False, mixtral_moe=False, phi2=False,
                chatglm3=False, llama2=False, deepseek_chat=False, gemma_it=False, starcoder2_instruct=False, llama3=False, llama3_instruct=False,
                qwen2_chat=False, deepseek_coder_v2=False, codegemma=False):
    class LocalCodeFFQAV2(CodeFFQAV2):
        def __init__(self, **kwargs):
            super().__init__(concate_sys_prompt, end_with_n, qwen_chat, deepseek_instruct, baichuan2, zypher, 
                octo, wizard, phi, inficoder, internlm, magicoder, mixtral_moe, phi2, 
                chatglm3, llama2, deepseek_chat, gemma_it, starcoder2_instruct, llama3, llama3_instruct, 
                qwen2_chat, deepseek_coder_v2, codegemma, **kwargs)

    return LocalCodeFFQAV2


# TODO: Replace `NewTask` with the name of your Task.
class CodeFFQAV2(Task):
    VERSION = 2
    # TODO: Add the `DATASET_PATH` string. This will be the name of the `Task`
    # dataset as denoted in HuggingFace `datasets`.
    DATASET_PATH = None
    # TODO: Add the `DATASET_NAME` string. This is the name of a subset within
    # `DATASET_PATH`. If there aren't specific subsets you need, leave this as `None`.
    DATASET_NAME = None

    def __init__(self, concate_sys_prompt, end_with_n=False, qwen_chat=False, deepseek_instruct=False, baichuan2=False, zypher=False, 
        octo=False, wizard=False, phi=False, inficoder=False, internlm=False, magicoder=False, mixtral_moe=False, phi2=False,
        chatglm3=False, llama2=False, deepseek_chat=False, gemma_it=False, starcoder2_instruct=False, llama3=False, llama3_instruct=False,
        qwen2_chat=False, deepseek_coder_v2=False, codegemma=False):
        super().__init__(stop_words=["<s>", "</s>", "<|endoftext|>", "<|EOT|>"], requires_execution=False)
        self.concate_sys_prompt = concate_sys_prompt
        self.end_with_n = end_with_n
        self.qwen_chat = qwen_chat
        self.deepseek_instruct = deepseek_instruct
        self.baichuan2 = baichuan2
        self.zypher = zypher
        self.octo = octo
        self.wizard = wizard
        self.phi = phi
        self.inficoder = inficoder
        self.internlm = internlm
        self.magicoder = magicoder
        self.mixtral_moe = mixtral_moe
        self.phi2 = phi2
        self.chatglm3 = chatglm3
        self.llama2 = llama2
        self.deepseek_chat = deepseek_chat
        self.gemma_it = gemma_it
        self.starcoder2_instruct = starcoder2_instruct
        self.llama3 = llama3
        self.llama3_instruct = llama3_instruct
        self.qwen2_chat = qwen2_chat
        self.deepseek_coder_v2 = deepseek_coder_v2
        self.codegemma = codegemma
    
    def get_dataset(self):
        """Returns dataset for the task or an iterable of any object, that get_prompt can handle"""
        url = "https://code.byted.org/linyi.li/open-freeform-code-qa-suite/blob/main/batched_prompts/suite_v2.0.0.csv"

        # import tempfile
        # import requests
        import datasets
        import os

        # with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
        #     print("Downloading source prompts...")
        #     r = requests.get(url, stream=True)
        #     f.write(r.content)
        #     f.flush()
            
        #     dataset = datasets.load_dataset("larryleeworking/code-ffqa-dataset-v2", data_files={"test": f.name})

        dataset = datasets.load_dataset("csv", data_files={"test": os.environ['DATASET_CSV_PATH']})
        return dataset['test']

    # def get_dataset(self):
    #     """Returns dataset for the task or an iterable of any object, that get_prompt can handle"""
    #     return self.dataset["test"]

    def get_prompt(self, doc):
        """Builds the prompt for the LM to generate from."""
        if self.qwen_chat:
            return '<|im_start|>system\n' + doc['system_prompt'] + '<|im_end|>\n<|im_start|>user\n' + doc['content_prompt'] + '<|im_end|>\n<|im_start|>assistant\n'
        elif self.deepseek_instruct:
            return doc['system_prompt'] + '### Instruction:\n' + doc['content_prompt'] + '\n' + '### Response:\n'
        elif self.baichuan2:
            return doc['system_prompt'] + '<reserved_106>' + doc['content_prompt'] + '<reserved_107>'
        elif self.zypher:
            return '<|system|>\n' + doc['system_prompt'] + '</s>' + '<|user|>\n' + doc['content_prompt'] + '</s>'
        elif self.octo:
            return doc['system_prompt'] + '\n' + 'Question: ' + doc['content_prompt'] + '\n\nAnswer:'
        elif self.wizard:
            return doc['system_prompt'] + '\n\n' + '### Instruction:\n' +  doc['content_prompt'] + '\n\n### Response:'
        elif self.phi:
            return doc['system_prompt'] + '\n' + doc['content_prompt'] + '\n\nAnswer:'
        elif self.inficoder:
            return f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{doc['content_prompt']}\n\n### Response:"
        elif self.internlm:
            return '<|User|>:{}<eoh>\n<|Bot|>:'.format(doc['system_prompt'] + '\n' + doc['content_prompt'])
        elif self.mixtral_moe:
            return '<s> [INST] {} [/INST] '.format(doc['system_prompt'] + '\n' + doc['content_prompt'])
        elif self.magicoder:
            return f"""You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.

@@ Instruction
{doc['content_prompt']}

@@ Response
"""
        elif self.phi2:
            return 'Instruct: {}\nOutput:'.format(doc['system_prompt'] + '\n' + doc['content_prompt'])
        elif self.chatglm3:
            # return '<|system|>{}<|user|>{}<|assistant|>'.format(doc['system_prompt'], doc['content_prompt'])
            return '<|system|>\n {}<|user|>\n {}<|assistant|>'.format(doc['system_prompt'], doc['content_prompt'])
        elif self.llama2:
            return """<s>[INST] <<SYS>>
{}
<</SYS>>

{} [/INST]""".format(doc['system_prompt'], doc['content_prompt'].strip())
        elif self.deepseek_chat:
            return 'User: ' + doc['system_prompt'] + '\n' + doc['content_prompt'] + '\n\n' + 'Assistant:'
        elif self.gemma_it:
            return "<start_of_turn>user\n" + doc['system_prompt'] + '\n' + doc['content_prompt'] + "\n<start_of_turn>model\n"
        elif self.starcoder2_instruct:
            return "<|endoftext|>You are an exceptionally intelligent coding assistant that consistently delivers accurate and reliable responses to user instructions.\n\n### Instruction\n" + doc['content_prompt'] + '\n\n### Response\n'
        elif self.llama3_instruct:
            return '<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n' + doc['system_prompt'] + '<|eot_id|>' + \
                '<|start_header_id|>user<|end_header_id|>\n\n' + doc['content_prompt'] + '<|eot_id|>' + \
                '<|start_header_id|>assistant<|end_header_id|>\n\n'
        elif self.qwen2_chat:
            return '<|im_start|>system\n' + doc['system_prompt']  + '<|im_end|>\n' + \
                    '<|im_start|>user\n' + doc['content_prompt'] + '<|im_end|>\n' + \
                    '<|im_start|>assistant\n'
        elif self.deepseek_coder_v2:
            return '<｜begin▁of▁sentence｜>' + doc['system_prompt'] + '\n\n' + 'User: ' + doc['content_prompt'] + '\n\n' + 'Assistant:'
        elif self.codegemma:
            return '<bos><start_of_turn>user\n' + doc['system_prompt'] + '\n' + doc['content_prompt'].strip(' \n') + \
            '<end_of_turn>\n<start_of_turn>model\n' 
        else:
            return doc['system_prompt'] + self.concate_sys_prompt + doc['content_prompt'] + ('\n' if self.end_with_n else '')
            
    def get_reference(self, doc):
        """Builds the reference solution for the doc (sample from the test dataset)."""
        """Here it is just a filename printer for us to locate the evaluator script"""
        target = doc['filename'] 
        # use filename to locate the evaluator script
        return target

    def postprocess_generation(self, generation, idx):
        return generation
    
    def process_results(self, generations, references):
        """Takes the list of LM generations and evaluates them against ground truth references,
        returning the metric for the generations.
        :param generations: list(list(str))
            list of lists containing generations
        :param references: list(str)
            list of str containing references
        """
        results = []
        for gens, filename in zip(generations, references):
            for j, gen in enumerate(gens):
                results.append({'filename': filename, 'completion': gen, 'completion_no': j})
        return results

    def check_fn(self, generation):
        import os
        ret = "</s>" in generation or '\n' * 10 in generation or "<|endoftext|>" in generation or "<|EOT|>" in generation or "<eod>" in generation \
            or '<|eot_id|>' in generation or '<|im_end|>' in generation
        if len(generation) % 100 == 0:
            print('[', os.environ.get('LOCAL_RANK',-1), ']', len(generation), ret)
        if len(generation) >= 3500: # a heuristic, since gpt4 response has max len 2542
            ret = True
        return ret
