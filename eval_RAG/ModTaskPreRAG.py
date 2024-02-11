from langchain.schema.runnable import Runnable, RunnableLambda, RunnablePassthrough, RunnableBranch
from ToolsManagerDB import ToolStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import dotenv
import os
import re
import ast
import pandas as pd

TEMPLATE_MODEL_FS = """You are a very proficient assistant expert in Business Process Management. 

You are able to extract the process model in mermaid.js from a process description. To generate the process model you should extract the start event, end event, task, exclusive gateway and parallel gateway from the process description.

The mermaid.js process model should be generated according to the following rules:
The graph must use the LR (Left to Right) direction.
Each mermaid node must have the following structure:
    id:type:shape and text
        id - it is a unique identifier. Integer from 1 to n. Each node has a unique identifier
        type - defines the type of the element regarding to BPMN 2.0 notation.
            possible types are: start event, end event, task, exclusive gateway and parallel gateway.
        Based on the type of the node following shapes and texts are to be used:
            startevent: ((startevent))     i.e., id:startevent:((startevent))
            endevent: ((endevent))       i.e., id:endevent:((endevent))
            task: (task label)             i.e., id:task:(task label)
            exclusivegateway: {{x}}          i.e., id:exclusivegateway:{{x}}
            parallelgateway: {{AND}}         i.e., id:exclusivegateway:{{AND}}
All nodes that have occurred more than once should have following structure: id:type: (i.e., 2:task:) by futher occurrence.
All nodes are connected with each other with the help of the direction.
    direction: -->
If there are some conditions or annotations it is necessary to use text on links (i.e., edge labels)
    edge label: |condition or annotation|
Edge label is always located between 2 nodes: id:exclusivegateway:{{x}} --> |condition or annotation|id:task:(task label)

You are able to list the extracted task. The output is a list of strings. Each string contains an high level description of a task.

Include the mermaid.js process model within the ```mermaid and ``` markdown delimiters. Include the list of tasks within the ```tasks and ``` markdown delimiters. Do not add any other text, only mermaid.js code block and list of tasks.

Here are a few examples of process descriptions and the expected output:
1. Process description: Plastic injection molding is a manufacturing process for producing a variety of parts by injecting molten plastic material into a mold, and letting it cool and solidify into the desired end product. Our interest is in the quality assurance process which involves real-time monitoring of injection molding parameters. As each batch of molten plastic enters the mold, sensors capture data on temperature, pressure, and fill rates. The system analyzes this data to ensure that the molding parameters align with the specified standards. If any deviations are detected, the system triggers adjustments to the injection molding machine settings, allowing for immediate correction. Once the parameters are within the acceptable range, the system authorizes the production run to continue. This dynamic monitoring process guarantees the consistency and quality of the plastic molded components, minimizing the risk of defects and ensuring adherence to precise manufacturing specifications.
   Response: ```mermaid
   graph LR
   1:startevent:((startevent)) --> 2:task:(Batch enter the mold)
   2:task: --> 3:task:(Sensor capture data on temperature, pressure, and fill rates)
   3:task: --> 4:exclusivegateway:{{x}}
   4:exclusivegateway: --> |deviations detected| 5:task:(Adjust injection molding machine settings)
   4:exclusivegateway: --> |no deviations detected| 6:exclusivegateway:{{x}}
   5:task: --> 6:exclusivegateway:
   6:exclusivegateway: --> 7:task:(Continue production run)
   7:task: --> 8:endevent:((endevent))
   ```
   ```tasks
   ["batch of molten plastic enters the mold", "sensors capture temperature, pressure, anf fill rates of machine", "analysis of measured data", "settings of machine are adjusted", "plastic molded components are produced"]
    ```

2. Process description: The production of custom metal brackets begins with order processing. The warehouse department evaluates the parts lists and in parallel the production planning department configures the robotic assembly line accordingly. The automated precision machine cuts the metal and the welding machine assembles the parts into brackets. A computer vision inspection system then checks for quality assurance. If defective brakets are detected, the process ends. After inspection, a coating system enhances durability. Finally, the process is complete.
   Response: ```mermaid
   graph LR
   1:startevent:((startevent)) --> 2:task:(Order processing)
   2:task: --> 3:parallelgateway:{{AND}}
   3:parallelgateway: --> 4:task:(Configure robotic assembly line)
   3:parallelgateway: --> 5:task:(Warehouse parts evaluation)
   4:task: --> 6:parallelgateway:{{AND}}
   5:task: --> 6:parallelgateway:{{AND}}
   6:parallelgateway: --> 7:task:(Cut metal)
   7:task: --> 8:task:(Weld parts)
   8:task: --> 9:task:(Computer vision inspection)
   9:task: --> 10:exclusivegateway:{{x}}
   10:exclusivegateway: --> |defective brackets| 12:exclusivegateway:{{x}}
   10:exclusivegateway: --> |no defective brackets| 11:task:(Coating system)
   11:task: --> 12:exclusivegateway:
   12:exclusivegateway: --> 13:endevent:((endevent))
   ```
   ```tasks
   ["processing of the custom metal braket order", "evaluation of parts from warehouse", "configuration of the robotic assembly line", "cut the metal", "weld the metal part", "quality inspection of the produced brackets", "coating of the produced brackets"]

Process description: {input}
Answer:
"""

TEMPLATE_MODEL_NFS = """You are a very proficient assistant expert in Business Process Management. 

You are able to extract the process model in mermaid.js from a process description. To generate the process model you should extract the start event, end event, task, exclusive gateway and parallel gateway from the process description.

The mermaid.js process model should be generated according to the following rules:
The graph must use the LR (Left to Right) direction.
Each mermaid node must have the following structure:
    id:type:shape and text
        id - it is a unique identifier. Integer from 1 to n. Each node has a unique identifier
        type - defines the type of the element regarding to BPMN 2.0 notation.
            possible types are: start event, end event, task, exclusive gateway and parallel gateway.
        Based on the type of the node following shapes and texts are to be used:
            startevent: ((startevent))     i.e., id:startevent:((startevent))
            endevent: ((endevent))       i.e., id:endevent:((endevent))
            task: (task label)             i.e., id:task:(task label)
            exclusivegateway: {{x}}          i.e., id:exclusivegateway:{{x}}
            parallelgateway: {{AND}}         i.e., id:exclusivegateway:{{AND}}
All nodes that have occurred more than once should have following structure: id:type: (i.e., 2:task:) by futher occurrence.
All nodes are connected with each other with the help of the direction.
    direction: -->
If there are some conditions or annotations it is necessary to use text on links (i.e., edge labels)
    edge label: |condition or annotation|
Edge label is always located between 2 nodes: id:exclusivegateway:{{x}} --> |condition or annotation|id:task:(task label)

You are able to list the extracted task. The output is a list of strings. Each string contains an high level description of a task.

Include the mermaid.js process model within the ```mermaid and ``` markdown delimiters. Include the list of tasks within the ```tasks and ``` markdown delimiters. Do not add any other text, only mermaid.js code block and list of tasks.

Process description: {input}
Answer:
"""


class MermaidLLM:

    def __init__(self, model, openai_key, temperature=0.0, few_shot=False):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        if few_shot:
            self.prompt = PromptTemplate.from_template(TEMPLATE_MODEL_FS)
        else:
            self.prompt = PromptTemplate.from_template(TEMPLATE_MODEL_NFS)
        self.output_parser = StrOutputParser()

    def extract_mermaid_and_tasks(self, markdown_string):

        # Extract Mermaid diagram
        mermaid_pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
        mermaid_match = mermaid_pattern.search(markdown_string)
        
        if mermaid_match:
            mermaid_diagram = mermaid_match.group(1).strip()
        else:
            mermaid_diagram = None
        
        # Extract tasks
        tasks_pattern = re.compile(r'```tasks\n(.*?)\n```', re.DOTALL)
        tasks_match = tasks_pattern.search(markdown_string)
        
        if tasks_match:
            tasks_list = tasks_match.group(1).strip()
        else:
            tasks_list = None

        result = {
            'model': mermaid_diagram,
            'tasks': tasks_list
        }

        return result

    def get_chain(self) -> str:
        chain = (
            self.prompt
            | self.model
            | self.output_parser
            | RunnableLambda(lambda x: self.extract_mermaid_and_tasks(x))
        )
        return chain


TEMPLATE_TASK_FS = """You are a very proficient assistant expert in Business Process Management.

You are able to better describe the list of tasks-activities from a process description. 
To generate the revised list of tasks-activities you have access to an already generated list of tasks-activities. The list of tasks-activities is specified after the "Tasks:" line.

The output is a list of strings. Each string contains a summarization of an task-activities.

Here are a few examples of process descriptions and the expected output:
1. Process description: Plastic injection molding is a manufacturing process for producing a variety of parts by injecting molten plastic material into a mold, and letting it cool and solidify into the desired end product. Our interest is in the quality assurance process which involves real-time monitoring of injection molding parameters. As each batch of molten plastic enters the mold, sensors capture data on temperature, pressure, and fill rates. The system analyzes this data to ensure that the molding parameters align with the specified standards. If any deviations are detected, the system triggers adjustments to the injection molding machine settings, allowing for immediate correction. Once the parameters are within the acceptable range, the system authorizes the production run to continue. This dynamic monitoring process guarantees the consistency and quality of the plastic molded components, minimizing the risk of defects and ensuring adherence to precise manufacturing specifications.
   Tasks: ["enter mold", "capture sensor", "analysis", "machine adjusted", "plastic produced"]
   Response: ["batch of molten plastic enters the mold", "sensors capture temperature, pressure, anf fill rates of machine", "analysis of measured data", "settings of machine are adjusted", "plastic molded components are produced"]

2. Process description: The warehouse of Grimaldi is a warehouse that stores cardboard rolls. A cardboard roll is used to produce cardboards. There exists two types of cardboard: the white cardboard and the brown cardboard. The warehouse stores the cardboard rolls depending on the type of cardboard. When a new cardboard roll arrives at the warehouse, the worker checks the type of cardboard and enter this information inside the WMS system. The system automatically capture an image of the current status of the warehouse. By analyzing the image, the system identifies the location where the cardboard roll should be stored. Then the worker stores the cardboard rool in the warehouse and the system updates the quantity of that cardboard rolls in the warehouse.
   Tasks: ["check type of cardboard", "enter information", "capture image", "identify location", "store", "update the quantity"]
   Response: ["the worker checks the type of cardboard", "the worker enters the information inside the WMS system", "the system captures an image of the current status of the warehouse", "the system identifies the location where the cardboard roll should be stored", "the worker stores the cardboard rool in the warehouse", "the system updates the quantity of that cardboard rolls in the warehouse"]

3. Process description: The production of custom metal brackets begins with order processing. The warehouse department evaluates the parts lists and in parallel the production planning department configures the robotic assembly line accordingly. The automated precision machine cuts the metal and the welding machine assembles the parts into brackets. A computer vision inspection system then checks for quality assurance. If defective brakets are detected, the process ends. After inspection, a coating system enhances durability. Finally, the process is complete.
   Tasks: ["process order", "evaluate parts", "configure assembly line", "cut metal", "weld metal", "inspect quality", "coat brackets"]
   Response: ["processing of the custom metal braket order", "evaluation of parts from warehouse", "configuration of the robotic assembly line", "cut the metal", "weld the metal part", "quality inspection of the produced brackets", "coating of the produced brackets"]

Process description: {input}
Tasks: {tasks}
Response:
"""


TEMPLATE_TASK_NFS = """You are a very proficient assistant expert in Business Process Management.

You are able to better describe the list of tasks-activities from a process description. 
To generate the revised list of tasks-activities you have access to an already generated list of tasks-activities. The list of tasks-activities is specified after the "Tasks:" line.

The output is a list of strings. Each string contains a summarization of an task-activities.

Process description: {input}
Tasks: {tasks}
Response:
"""

class TaskRetrieverLLM():

    def __init__(self, model, openai_key, temperature=0.0, few_shot=False):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)
        if few_shot:
            self.prompt = PromptTemplate.from_template(TEMPLATE_TASK_FS)
        else:
            self.prompt = PromptTemplate.from_template(TEMPLATE_TASK_NFS)
        self.output_parser = StrOutputParser()

    def get_chain(self) -> str:
        chain = self.prompt | self.model | self.output_parser
        return chain


class ProcessLLM:

    def __init__(self, model="gpt-3.5-turbo", openai_key=None, temperature=0.0, few_shot=False):
        self.model_tasks_llm = MermaidLLM(model, openai_key, temperature=temperature, few_shot=few_shot)
        self.task_llm = TaskRetrieverLLM(model, openai_key, temperature=temperature, few_shot=few_shot)

        embedding_function = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=openai_key)
        self.tools_store = ToolStore(openai_key)
        self.tools_store.embed_tools(embedding_function)


    def tools_prompt_parser(self, task_llm_output: dict) -> str:
        """Retrieve the list of tools from the tasks list"""
        task_list = ast.literal_eval(task_llm_output)
        res_tool = {}
        for task in task_list:
            # retrieve the tool
            task_tool = []
            res = self.tools_store.search(task)['output']
            if res == []:
                continue
            else:
                for elem in res:
                    task_tool.append([elem["name"], elem["score"]])
            res_tool[task] = task_tool

        return res_tool


    def is_list_of_tasks(self, output: str) -> bool:
        """Check if the output from the task retriever is a list of tasks"""
        # convert a string to list
        try:
            result_list = ast.literal_eval(output)
            if not isinstance(result_list, list):
                return []
        except:
            result_list = []
        if len(result_list) == 0:
            return False
        
        return True

    def task_llm_parser(self) -> Runnable:
        task_llm_chain = self.task_llm.get_chain()

        task_llm_chain_output = {
            "tasks": task_llm_chain,
            "inputs": RunnablePassthrough()
        }

        task_llm_chain_output = (
            task_llm_chain_output
            | RunnableLambda(lambda x: {
                "tasks": x["tasks"],
                "input": x["inputs"]["input"],
                "model": x["inputs"]["model"]
                })
        )

        return task_llm_chain_output


    def model_tasks_llm_parser(self) -> Runnable:
        model_llm_chain = self.model_tasks_llm.get_chain()

        model_llm_chain_output = {
            "output": model_llm_chain,
            "inputs": RunnablePassthrough()
        }

        model_llm_chain_output = (
            model_llm_chain_output
            | RunnableLambda(lambda x: {
                "model": x["output"]["model"],
                "tasks": x["output"]["tasks"],
                "input": x["inputs"]["input"]
                })
        )

        return model_llm_chain_output


    def get_chain(self):
        model_tasks_llm_chain_output = self.model_tasks_llm_parser()
        task_llm_chain_output = self.task_llm_parser()

        chain = (
            model_tasks_llm_chain_output
            | task_llm_chain_output
            | RunnableLambda(
                lambda x: {
                    "tasks": x["tasks"],
                    "has_tasks": self.is_list_of_tasks(x["tasks"]),
                    "input": x["input"],
                    "model": x["model"]
                }
            )
            | RunnableBranch(
                (lambda x: x["has_tasks"], RunnableLambda(lambda x: {
                    "model": x["model"],
                    "tools": self.tools_prompt_parser(x["tasks"]),
                    "input": x["input"],
                    })),
                (lambda x: "Your process description does not contain any task.")
            )
        )

        return chain


if __name__ == "__main__":
    dotenv.load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    models = ["gpt-3.5-turbo-16k", "gpt-4-0125-preview"]
    few_shot = [True, False]

    for model in models:
        for fs in few_shot:

            llm = ProcessLLM(model=model, openai_key=OPENAI_API_KEY, few_shot=fs)

            dataset = pd.read_csv("LLMtools2process/processes_tools.csv")

            res_eval = []
            for index, row in dataset.iterrows():
                input_text = row["process"]
                res = llm.get_chain().invoke({"input": input_text})
                print(f"res: {res}")
                if res != "Your process description does not contain any task.":
                    output = row["tools"]
                    output = ast.literal_eval(output)
                    tool_extracted = res["tools"]
                    model_p = res["model"]

                    tool_correct = []
                    tool_no_correct = []
                    for task in tool_extracted.keys():
                        task_tool = tool_extracted[task]
                        for elem in task_tool:
                            if elem[0] in output:
                                if elem[0] not in tool_correct:
                                    tool_correct.append(elem[0])
                            else:
                                if elem[0] not in tool_no_correct:
                                    tool_no_correct.append(elem[0])

                    tool_correct_not_extracted = list(set(output) - set(tool_correct))

                    print(f"Output: {output}")
                    print(f"Correct: {tool_correct}")
                    print(f"No correct: {tool_no_correct}")
                    print(f"Correct not extracted: {tool_correct_not_extracted}")

                    precision = len(tool_correct) / (len(tool_correct) + len(tool_no_correct))
                    recall = len(tool_correct) / (len(tool_correct) + len(tool_correct_not_extracted))

                    print(f"Precision: {precision}")
                    print(f"Recall: {recall}")

                    res_elem = [input_text, output, model_p, tool_correct, tool_no_correct, precision, recall]
                else:
                    res_elem = [input_text, None, None, [], [], 0.0, 0.0]

                res_eval.append(res_elem)

            res_df = pd.DataFrame(res_eval, columns=["process", "tools", "model", "correct", "no_correct", "precision", "recall"])

            if fs:
                if model == "gpt-3.5-turbo-16k":
                    res_df.to_csv('eval_mod_task_pre_fs_gpt35.csv', sep=',', index=False)
                else:
                    res_df.to_csv('eval_mod_task_pre_fs_gpt4.csv', sep=',', index=False)
            else:
                if model == "gpt-3.5-turbo-16k":
                    res_df.to_csv('eval_mod_task_pre_nfs_gpt35.csv', sep=',', index=False)
                else:
                    res_df.to_csv('eval_mod_task_pre_nfs_gpt4.csv', sep=',', index=False)
