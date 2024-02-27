# NL2ProcessOps

### Architecture

![architecture](images/architecture.png)

The first stage of the proposed approach starts with a textual process description that is given as input (1) to the [Tasks-Model extractor](src/TasksModelLLM.py). This component is an LLM prompted to extract the tasks and the control flow of the process and generates the model representation as a Mermaid.js. The list of tasks paired with the textual process description (i.e., `[proc_desc, tasks]`) is given as input (2a) to the [Tasks pre-processing](src/TasksPreProcessingLLM.py) component, starting the second stage of the proposed approach. At the same time, the process model paired with the textual process description (i.e., `[proc_desc, model]`) is given as input (2b) to the [Code generator](src/CodeLLM.py) component which, however, waits for the end of the second stage before moving on. The second stage of the proposed approach is inspired by the RAG concept to retrieve the relevant tools for the particular textual process description. The [Tasks pre-processing](src/TasksPreProcessingLLM.py) component leverages an LLM to refine the descriptions of the extracted tasks based on the textual process description. The refined list of tasks is then handled (3) by the [Tools retriever](src/ToolsManagerDB.py) component. The latter interacts (4) with the vector database **Tools DB** and retrieves the most similar embedded tools for each embedded task. **Tools DB** stores vectors consisting of the embeddings of the descriptions of the tools. The list of retrieved tools is provided (5) to the [Code generator](src/CodeLLM.py) component so that the third (and final) stage of the proposed approach begins. The [Code generator](src/CodeLLM.py) LLM that from the textual process description, process model and the list of tools implementing process tasks generates (6) a Python function that simulates the process. 


### Setup

Create a new conda environment
```bash
conda create -n pyllm python=3.10
conda activate pyllm
```

Install the dependencies
```bash
pip install -r requirements.py
```

Set up OpenAI API key. Create a `.env` file containing this line:
```env
OPENAI_API_KEY=<your key, should start with sk->
```


### Usage

Run the LLM-based solution
```bash
python src/ProcessLLM.py
```

It will generate/update a `llm_process_code.py` file with the Python code simulating the textual process description given as input to the LLM.