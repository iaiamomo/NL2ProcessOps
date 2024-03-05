## Tools Retrieval evaluation
- [TaskRAG.py](TaskRAG.py): extract task from process description
- [ModTaskRAG.py](ModTaskRAG.py): extract model and relative tasks from process description
- [ModTaskPreRAG.py](ModTaskPreRAG.py): extract model and relative tasks and preprocessing of tasks from process description
- [ToolsManagerDB.py](ToolsManagerDB.py): retrieval module implementation

### Dataset
- [LLMtools2process_v2](eval_retrieval\LLMtools2process_v2\processes_tools.csv): set of 30 textual process descriptions generated with an [LLM](LLMtools2process_v2) from a set of 62 tools

### Results
$precision=t_{p}/(t_{p}+f_{p})$ \
$recall=t_{p}/(t_{p}+f_{n})$ \
$t_{p}=$ correct tool extracted \
$f_{p}=$ no correct tool extracted \
$f_{n}=$ correct tool no extracted

```
           case  model    recall  precision
0          task  gpt35  0.770327   0.742198
1          task   gpt4  0.773579   0.790755
2      mod_task  gpt35  0.762037   0.730392
3      mod_task   gpt4  0.764795   0.766513
4  mod_task_pre  gpt35  0.777326   0.756105
5  mod_task_pre   gpt4  0.761764   0.762833
```