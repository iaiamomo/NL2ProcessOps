# NL2ProcessOps

## About

NL2ProcessOps, a novel approach leveraging Large Language Models (LLMs) and concepts such as Retrieval Augmented Generation (RAG), agents, and tools for code generation to streamline process deployment operations. The proposed approach is designed to work with textual process descriptions and focuses on the different operations of process deployment, from extracting the control flow in terms of a process model, over retrieving required tools associated with each task, to generating executable script for manual refinement purposes and deployment in a process engine.

#### Architecture

![architecture](images/architecture.png)

The first stage of the proposed approach starts with a textual process description that is given as input (1) to the [Tasks-Model extractor](src/TasksModelLLM.py). This component is an LLM prompted to extract the tasks and the control flow of the process and generates the model representation as a Mermaid.js. The list of tasks paired with the textual process description (i.e., `[proc_desc, tasks]`) is given as input (2a) to the [Tasks pre-processing](src/TasksPreProcessingLLM.py) component, starting the second stage of the proposed approach. At the same time, the process model paired with the textual process description (i.e., `[proc_desc, model]`) is given as input (2b) to the [Code generator](src/CodeLLM.py) component which, however, waits for the end of the second stage before moving on. The second stage of the proposed approach is inspired by the RAG concept to retrieve the relevant tools for the particular textual process description. The [Tasks pre-processing](src/TasksPreProcessingLLM.py) component leverages an LLM to refine the descriptions of the extracted tasks based on the textual process description. The refined list of tasks is then handled (3) by the [Tools retriever](src/ToolsManagerDB.py) component. The latter interacts (4) with the vector database **Tools DB** and retrieves the most similar embedded tools for each embedded task. **Tools DB** stores vectors consisting of the embeddings of the descriptions of the tools. The list of retrieved tools is provided (5) to the [Code generator](src/CodeLLM.py) component so that the third (and final) stage of the proposed approach begins. The [Code generator](src/CodeLLM.py) LLM that from the textual process description, process model and the list of tools implementing process tasks generates (6) a Python program that represents the process.

## Structure of the repository

```
.
├── eval_code           # sources for code generation evaluation
|   ├── README.md       # evaluation results of code generation
|   └── ...
├── eval_human          # sources for the human evaluation
|   ├── README.md       # evaluation results of human evaluation
|   └── ...
├── eval_retrieval      # sources for retrieval evaluation
|   ├── README.md       # evaluation results of retrieval
|   └──...
├── src                 # source code of proposed approach
|   └──...
├── .env                # .env file with OpenAI API key
└──...
```


## Getting Started

- Create a new [conda](https://docs.anaconda.com/free/miniconda/) environment:
    ```bash
    conda create -n pyllm python=3.10
    conda activate pyllm
    ```

- Install the dependencies:
    ```bash
    pip install -r requirements.py
    ```

- Set up an [OpenAI API key](https://platform.openai.com/overview) and create a `.env` file in the root directory containing this line:
    ```env
    OPENAI_API_KEY=<your key, should start with sk->
    ```


## Usage

- Run the LLM:
    ```bash
    cd src
    python ProcessLLM.py
    ```

- Input a textual process description. \
    **Example**: `The calibration process of cardboard production consists of continuously capturing a photo of the cardboard being produced. Each photo is analyzed to check if all the markers identified are ok. If markers are not ok, the calibration process continues. If the markers are ok, the speed of the die-cutting machine is set to 10000 RPM and the process ends.`

- The LLM will generate a `llm_process_code.py` file with the Python program representing the textual process description given as input to the LLM. \
Given the **Example**, the LLM will generate a Python program as follows.
    ```python
    from tools.camera import CaptureImage
    from tools.vision_is import CheckMarkers
    from tools.die_machine import SetSpeedDieMachine

    import numpy as np

    def calibrate_cardboard_production():
        while True:
            # Capture a photo of the cardboard
            captured_image = CaptureImage.call()
            
            # Analyze the photo to check if all markers are ok
            markers_ok = CheckMarkers.call(image=captured_image)
            
            # If markers are not ok, continue the calibration process
            if not markers_ok:
                continue
            
            # If markers are ok, set the speed of the die-cutting machine to 10000 RPM
            speed_set = SetSpeedDieMachine.call(speed=10000)
            
            # If the speed was successfully set, end the process
            if speed_set:
                break
        
        return "Calibration process completed."

    if __name__ == "__main__":
        result = calibrate_cardboard_production()
        print(result)
    ```

## Experiments

To evaluate the proposed approach we perform separate assessments for the retrieval of appropriate tools and process code generation. We do not evaluate the process model generation stage as it is based on related work by authors in where the proposed approach has been already evaluated based on quantitative and qualitative assessments.

### Retrieval experiments

[eval_retrieval](eval_retrieval) folder contains the results of the experiments. The three strategies evaluated are: *(i)* an LLM - [TaskRAG.py](eval_retrieval/TaskRAG.py) - extracting the list of tasks from the textual process description (with few-shot prompting approach), *(ii)* an LLM - [ModTaskRAG.py](eval_retrieval/ModTaskRAG.py) -that extracts the control flow and the list of tasks from the textual process description, *(iii)* two separate LLMs - [ModTaskPreRAG.py](eval_retrieval/ModTaskPreRAG.py) - which extract the control flow and the list of tasks and then refine the description of the extracted tasks. 

The dataset of the 30 textual process descriptions with the related tools is contained in [LLMtools2process](eval_retrieval/LLMtools2process) - [processes_tools.csv](eval_retrieval/LLMtools2process/processes_tools.csv).

To replicate the experiments:
1. Run each Python file related to the different strategies.
2. They will create several `.csv` files to be moved into the [data](eval_retrieval/data) folder.
3. Display precision and recall.
    ```python
    cd eval_retrieval
    python res_values.py
    ```


### Code generation experiments

[eval_code](eval_code) folder contains the results of the experiments. It contains several folders `runX` where `X` is the number of the run: *(i)* [run1](eval_code/run1) contains results with the pre-processing component using GPT-4, *(ii)* [run2](eval_code/run2) contains results with the pre-processing component using GPT-3.5 and GPT-4, *(iii)* [run3](eval_code/run3) contains results without the pre-processing component using GPT-4, *(iv)* [run4](eval_code/run4) contains results without the pre-processing component using GPT-3.5 and GPT-4, *(v)* [run5](eval_code/run5) contains results not including the process model in the prompt for the code generation component using GPT-4, *(vi)* [copilot](eval_code/copilot) contains results of the baseline GitHub Copilot.

The dataset of the 10 textual process descriptions and related Python code used for these experiments is contained in [data](eval_code/data).

To replicate the experiments:
1. The Python file contained in each `runX` folder need to be moved into the [src](src). 
2. Then run it.
3. It will generate a `.csv` file that need to be moved back to the `runX` folder. 
4. Then organize the results in single Python script.
    ```python
    cd eval_code
    python fix_data.py
    ```
5. Finally, compute CodeBLEU results.
    ```python
    cd eval_code
    python codebleu_eval.py
    ```

[res_human](eval_code/res_human.csv) contains the results of the human evaluation. They can be displayed with
```python
cd eval_code
python human_eval.py
```

### Human evaluation

[eval_human](eval_human) contains the sources of the human evaluation: the [questionnaire](eval_human/questionnaire.pdf) and the [results](eval_human/results.csv).

Evaluation is performed comparing GitHub Copilot and NL2ProcessOps results.

## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.