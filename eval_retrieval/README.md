## Tools Retrieval evaluation
- [TaskRAG.py](TaskRAG.py): extract task from process description
- [ModTaskRAG.py](ModTaskRAG.py): extract model and relative tasks from process description
- [ModTaskPreRAG.py](ModTaskPreRAG.py): extract model and relative tasks and preprocessing of tasks from process description

### Datasets
- [data_v2](eval_retrieval\LLMtools2process_v2\processes_tools.csv): set of 30 textual process descriptions generated with an [LLM](LLMtools2process_v2) from a set of 62 tools

### Results
$precision=t_{p}/(t_{p}+f_{p})$ \
$recall=t_{p}/(t_{p}+f_{n})$ \
$t_{p}=$ correct tool extracted \
$f_{p}=$ no correct tool extracted \
$f_{n}=$ correct tool no extracted

```
           case  model    recall  precision
0          task  gpt35  0.721623   0.869582
1          task   gpt4  0.738922   0.896920
2      mod_task  gpt35  0.733307   0.867197
3      mod_task   gpt4  0.726447   0.887861
4  mod_task_pre  gpt35  0.737394   0.881759
5  mod_task_pre   gpt4  0.710419   0.862740
```