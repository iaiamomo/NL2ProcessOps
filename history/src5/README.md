## LLM and Processes

![architecture](architecture.png)

We have four LLMs chained together to output a python code and extracting the data flow of a process description:
- `TaskLLM`: extracts from the process description the list of tasks. The output of this LLM is fed to the ToolManager which retrieve the matching tools able to perform given tasks. ToolManager follows RAG approach.
- `ModelLLM`: extract the process model from the given process description.
- `CoodeLLM`: given the process description, the process model and the list of tools, generate a python code able to simulate the process. The python code is saved into `llm_process_code.py` for further execution.
- `DataLLM`: extract the data flow from the given process description, process model and python code.

### RAG - https://arxiv.org/abs/2312.10997
To improve the quality of your indexed data, you should:
1. remove irrelevant text/document for your specific task
2. reformat your indexed data to a format similar to what your end users may use 
3. add metadata to your documents for efficient and targeted retrieval.

To try:
- rewrite the user’s query - tasks in our case - in a format that is similar to what may be found in the vector DB before trying to match it. Query2doc: https://arxiv.org/abs/2303.07678, HyDE: https://arxiv.org/abs/2212.10496. Following such structure, I can ask to generate documentation for the extracted tasks and find in the DB the most similar tools.
- try different embeddings
- try to use score value from the retriever
- https://arxiv.org/abs/2401.08406

### TODO
- test RAG
    - play with the score outputs
    - store only tool description and actor (which refer to the name of the python file containing the tool definition) and see if the "tool search works better" - we can justify with this https://arxiv.org/abs/1909.09436
- find how to define tools 
    - refer OpenAPI standard (description, input, output)
- test with other process description
    - Spindle manufacturing
    - calibration process in Rotalaser
    - ...
- https://arxiv.org/abs/2104.05310

### IDEA
We realize a prototype that employs LLMs to interpret process description and generate the data flow of the underlying process (via execution-simulation of the process).

Our goal is to avoid training (fine-tuning) by applying in-context learning.

A running example: calibration process/chip manufacture

Evaluation?