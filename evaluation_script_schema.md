## Overall Architecture

Suite -> Case -> References Answers/Keywords/Unit Tests
There are two types of YAML files, for suite and case spec respectively.

## Suite Spec:

"*" stands for optional fields

Example: suite_v1.yaml

Format:

```yaml
*attempt_reduce_mode: ['avg' | 'max' | 'min'] [default: 'avg']
# For multiple attempts, i.e., multiple model responses, how to aggregate score
*full_score_per_question: float [default: 1.0]
# per instance full score, will be overwritten 
# if case instance has "full_score" field
*null_score_per_question: float [default: 0.0]
# if there is no response, we get null score per case, will be overwritten 
# if case instance has "null_score" field
cases: list
  - [str or dict]
    {if str, equals to 
    - path: str (e.g., "xxxx.yaml")
      # relative path to case config file
    - weight: 1.0}
    - path: str
    - weight: float [default: 1.0]
    
  - ...
*version: str
# for suite self identification
```

## Case Spec and Scoring:
Example: `cases/eval_208.yaml`
Format:
- All paths are relative to the case file

Scoring:
- Case score is the sum score of each criterion, if presents, clipped by the max score (if present), then normalized by the full score:
$$caseScore(resp, spec) = \dfrac{\min\{maxScore, S_{keyWord} + S_{blankFilling} + S_{unitTest} + S_{similarity} + S_{custom}\}}{\min\{maxScore, FS_{keyWord} + FS_{blankFilling} + FS_{unitTest} + FS_{similarity} + FS_{custom}\}}$$

- Suite score is the sum score of each case score aggregated by avg/min/max among response attempts.

$$suiteScore = \sum_{case} \left\\{ \begin{aligned} 
& {avg/min/max}_{resp\in Responses} 
\{caseScore(resp, spec) * fullScore\} & Responses \neq \emptyset \\
& nullScore & Responses = \emptyset \\
\end{aligned} \\
 \right.$$

```yaml
id: str
# for case self identificaton
prompt_path: str
# relative path to the prompt text
type: str
# question type, for later statistics, e.g., 'knowledge question-answering'
lang: str
# question language or area, for later statistics, e.g., 'web', 'java', 'cpp', etc
*full_score: float
# the full score of this case in the final suite report, overwrites full_score_per_question in suite spec 
*null_score: float
# the score of no response, overwrites null_score_per_question in suite spec
grading:
    *max_score: float
    # the maximum score within the test case for clipping purpose, if not specified, no maximum clipping
    *min_score: float
    # the minimum score within the test case for clipping purpose, if not specified, no minimum clipping
    *keywords: list # keyword grading spec
        - [str or dict]
          {if str, equals to
            content: str
            weight: 1.0
            to_lower: false
          }
          content: [str or dict] # the keyword to match
            {if str, equals to
            content: str}
            # either "content" or "or" or "and" should appear
              *content: str # the keyword
              *or: # or clause for keyword matching
                - recursive with above spec
              *and: 
                - recursive with above spec
              *cond: str [default: "True"]
                  # Python statement to post-process the matched result
                  # Available variables: 
                  #    ans - current judged sat status in bool
                  #    context - history keyword judged results 
                  #              as a list of "unmatch"/"match"
               *regex: bool [default: False]
                  # whether to view the keyword as a regex expression
                  # and apply re.search to match
          *weight: float [default: 1.0] # default score if matched
          *to_lower: false [default: bool]
          *neg: bool [default: False] # if neg = True, will minus weight score to ban wrong answers
        - *post_handler: 
            module: str
            func: str
            # post handler func signature:
            # module.__call__(func)(key_word_get_score: float, key_word_tot_score: float, status: list[str])
            # -> (new_key_word_get_score: float,  new_key_word_tot_score: float, scoring_detail: Any)
            # Param: "key_word_get_score" is the get score in keyword matching subitem
            # "key_word_tot_score" is the total score in keyword matching subitem
            # both can be overwritten by post handler
            # "status" is the list of ["unmatch"/"match"] for each keyword
            # then, you can output "scoring_detail" to log something which will be appear in the final result yaml
    *blank_filling: dict
        template: str # the whole string of template we asked the model to complete
                      # by replacing the "blank_str" with entities
        *blank_str: str [default: "[blank]"]
        *escape: str [default: " '\"·"]
            # list of characters to be pre-filtered for model responses for blanks
        *prefix: str [default: ""]
            # prepend the model response with some prefix
        targets: list # gold answer for blanks in sequence
            - [str or dict]
              {if str, equals to
              content: str}
              content: [str or list of str or dict] 
                       # gold answer in OR-clause for the blank
                {if str, equals to single element list}
                - [str or dict]
                  {if str, equals to 
                  content: str}
                  content: str
                  *regex: bool [default: False]
                  *cond: str [default: "True"]
                    # Python statement to post-process the matched result
                    # Result will be concatenated by "and": (match_or_not and cond)
                    # Available variables:
                    #    grading_details: list of string starting with "(un)matched"
                    #    ans_str: str (gold answer)
                    #    ans_re: bool (whether to use regex matching)
                    #    response_str: str (model response for the blank)
              *weight: float [default: 1.0]
              *to_lower: bool [default: False]
              *substr_match: bool [default: False] # whether to match substring instead of exact whole seq match
        *post_handler: 
            module: str
            func: str
            # post handler func signature:
            # module.__call__(func)(key_word_get_score: float, key_word_tot_score: float, status: list[str])
            # -> (new_key_word_get_score: float,  new_key_word_tot_score: float, scoring_detail: Any)
            # Param: "key_word_get_score" is the get score in keyword matching subitem
            # "key_word_tot_score" is the total score in keyword matching subitem
            # both can be overwritten by post handler
            # "status" is the list of ["unmatched ..."/"matched ..."] for each keyword
            # ** "status" format is the only difference from the post_handler in "keywords" **
            # then, you can output "scoring_detail" to log something which will be appear in the final result yaml
    *unit_test: dict
        *lang: str # overwrite the root lang field and decide how to execute the code
        tests: list of str or dict
            - [str or dict]
              {if str, equals to
              content: str}
              # content or path field must appear
              *content: str # source code in literal string
              *path: str # source code path
              *prefix: str [default: ""]
              *prefix_path: str
                # prefix to add to model response 
                # before extracting code component & evaluate
              *cleanup_path: str
                # path to optional cleaning-up code
              *weight: float [default: 1.0]
              *timeout: float [default timeout is lang specific]
              *only_longest: bool [default: false]
                # whether to only keep the longest consecutive snippet rather than concatenating all code together
    *similarity: list of dict
      - metric: str [from "rouge1"/"rouge2"/"rougeL"/"rougeLsum" for now]
        references: list of str or dict
          - [str or dict]
            {if str, direct read in as the gold answer}
            path: str # gold answer path
        *max_score: float [default: 0.53 for rouge1, 0.51 for others]
          # map what score to full score
        *min_score: float [default: 0.3]
          # map what score to zero score
        *weight: float [default: 1.0]
    *customized: dict
        *real_metric_type: keywords / blank_filling / unit_test / similarity
        module: str
        func: str
        # func(response) -> (now_score: float, full_score: float, detail: *)
```
 
## Human Annotation:

Raw instruction for human annotators (in Chinese)

```
要求：改写的prompt请在大致忠实于问题原意的基础上，尽量保持简洁和明确，并保证完整（无外部URL或图片依赖）。如为代码修改和代码生成类问题，请尽量明确需求以致可以写出其单元测试，即需明确要补全的函数名称、签名等。
类型分类：知识问答（knowledge question-answering），代码补全（code completion），代码debug（code debugging）
语言和领域分类：如为单语言问题，使用语言标签：Javascript/Cpp/Python/Sql/Dart/C#/Java/Swift/...。如为多语言或无语言问题，使用领域标签：Web/Mobile/Cloud/OS/...。不确定的情况可同时设置语言和领域标签。
评估标准：五大类评估标准中选择一项（少数情况可结合多项标准）
1. 关键词匹配：请列出需要匹配的关键词，可带有相互依赖的匹配规则（例：如匹配到关键词1，则匹配关键词2）。每个关键词可以有不同的权重，关键词也支持基于正则表达式的模糊匹配。
2. 完形填空：需在prompt中给出模型需要补全的完形填空模板，并在答案中依次给出每个空的参考答案。由于完形填空相对较开放，推荐使用GPT4/3.5先让模型生成一版，再根据生成的结果启发来尽量考虑所有可能的正确答案。同样，每个空也可以设置不同的权重，并支持基于正则表达式的模糊匹配。
3. 单元测试：使用代码来测试结果的准确性。需在prompt里明确需要生成的函数名称、签名、和返回格式。然后使用代码与断言（assertion）进行测试。可以有多项单元测试并具有不同的权重。
4. 对话相似度：（尽量少使用这类评估标准）使用ROUGE分数来评估生成的答案与参考答案的接近程度。可以有多个参考答案，并动态调整分数的映射范围。需对参考答案进行适当的清洗，并尽量减少参考答案的程度。
5. 自定义：使用python函数func(response) -> (now_score: float, full_score: float, detail: *)来自定义评估规则
```

English translation:

For rewritten prompts, aim to be concise and clear while staying roughly faithful to the original question. Ensure completeness (no external URLs or image dependencies). For code modification and generation questions, clearly specify the requirements so that unit tests can be written, including the function name, signature, and other details.

Type Classification: Knowledge Question-Answering, Code Completion, Code Debugging.

Language and Domain Classification: For single-language issues, use language tags: JavaScript/Cpp/Python/SQL/Dart/C#/Java/Swift/..., etc. For multi-language or non-language issues, use domain tags: Web/Mobile/Cloud/OS/..., etc. If uncertain, use both language and domain tags.

Evaluation Criteria: Choose one of the five main evaluation criteria (or combine multiple criteria in rare cases):

1. Keyword Matching: List keywords to match, including any dependent rules (e.g., if keyword 1 is matched, then keyword 2 should also be matched). Keywords may have different weights and support fuzzy matching based on regular expressions.

2. Blank Filling: Provide a cloze test template in the prompt and give reference answers for each blank. Given the open-ended nature of cloze tests, it is recommended to use GPT-4/3.5 to generate an initial version and then consider all possible correct answers based on the generated results. Each blank can also have different weights and support fuzzy matching based on regular expressions.

3. Unit Testing: Use code to verify the accuracy of results. Clearly specify the function name, signature, and return format needed in the prompt. Then use code and assertions to test. Multiple unit tests with different weights can be included.

4. Dialogue Similarity (use sparingly): Use ROUGE scores to evaluate how closely the generated answer matches the reference answers. Multiple reference answers can be used, and the scoring range can be adjusted dynamically. Ensure that reference answers are appropriately cleaned and minimized in scope.

5. Customized: Use the Python function func(response) -> (now_score: float, full_score: float, detail: *) to define custom evaluation rules.
