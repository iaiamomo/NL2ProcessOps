## Tool RAG evaluation
- [TaskRAG.py](TaskRAG.py): extract task from process description
- [ModTaskRAG.py](ModTaskRAG.py): extract model and relative tasks from process description
- [ModTaskPreRAG.py](ModTaskPreRAG.py): extract model and relative tasks and preprocessing of tasks from process description

#### Results:
$precision=t_{p}/(t_{p}+f_{p})$ \
$recall=t_{p}/(t_{p}+f_{n})$ \
$t_{p}=$ correct tool extracted \
$f_{p}=$ no correct tool extracted \
$f_{n}=$ correct tool no extracted

```
            case few_shot  model    recall  precision
0           task       fs  gpt35  0.932919   0.915510  
1           task       fs   gpt4  0.882330   0.894918  
2           task      nfs  gpt35  0.061111   0.058730  
3           task      nfs   gpt4  0.066667   0.066667  
4       mod_task       fs  gpt35  0.928558   0.919644  
5       mod_task       fs   gpt4  0.932522   0.906694  
6       mod_task      nfs  gpt35  0.000000   0.000000  
7       mod_task      nfs   gpt4  0.000000   0.000000  
8   mod_task_pre       fs  gpt35  0.932661   0.931652  
9   mod_task_pre       fs   gpt4  0.947679   0.924564  
10  mod_task_pre      nfs  gpt35  0.000000   0.000000  
11  mod_task_pre      nfs   gpt4  0.000000   0.000000
```