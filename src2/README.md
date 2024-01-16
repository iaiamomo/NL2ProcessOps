## 9-16/01/2023

- [tools](tools) folder contains the specification of the tools. They are implemented either with the decorator <code>@tool</code> or by extending the <code>BaseTool</code> class.
- [CodeLLM.py](CodeLLM.py): LLM that takes as input a process description and output a python script that enact the process. The prompt contains the list of the tools he has access to. It is not an agent, but an LLM. The prompt contains the description of the tools however the LLM does not have the possibility to invoke them.
- [DataLLM.py](DataLLM.py): LLM that takes as input a process description and output the data flow. The prompt contains the list of the tools he has access to. It is not an agent, but an LLM. The prompt contains the description of the tools however the LLM does not have the possibility to invoke them.
- [MermaidLLM.py](MermaidLLM.py): LLm that takes as input a process description and output a mermaid.js representing the process model. The structure of the mermaid.js is such that it can be imported in the CPEE.

## Notes

What we can achieve is the development of an LLM agent which has access to 3 tools. Such tools are the 3 LLM that generates the process model, the data flow and simulate the process.