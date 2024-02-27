from langchain.schema.runnable import Runnable, RunnableLambda, RunnablePassthrough, RunnableBranch
from ToolsManagerDB import ToolStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import dotenv
import os
import ast
import pandas as pd


TEMPLATE = """You are a very proficient assistant expert in Business Process Management tasks. You are able in taking a natural language process description and extracting the underline start event, end event, task, exclusive gateway and parallel gateway from the process description. Your goal is to output a list of the extracted tasks.

The output is a list of strings. Each string contains a high level description of a task.

If the process description does not contains any task, the output is an empty list.

Here are a few examples of process descriptions and the expected output:

1. Process description: When a pallet arrives at the working station, the system empties the scan results. Then the worker scans the order. Afterwards the system displays the scanning UI to the worker and in parallel, the worker assembles the part.
   Response: ["empty the scan results", "scan the order", "display the scanning UI", "assemble the part"]

2. Process description: The warehouse of Grimaldi is a warehouse that stores cardboard rolls. A cardboard roll is used to produce cardboards. There exists two types of cardboard: the white cardboard and the brown cardboard. The warehouse stores the cardboard rolls depending on the type of cardboard. When a new cardboard roll arrives at the warehouse, the worker checks the type of cardboard and enter this information inside the WMS system. The system automatically capture an image of the current status of the warehouse. By analyzing the image, the system identifies the location where the cardboard roll should be stored. Then the worker stores the cardboard rool in the warehouse and the system updates the quantity of that cardboard rolls in the warehouse.
   Response: ["check the type of cardboard", "enter the information inside the WMS system", "capture an image of the current status of the warehouse", "identify the location where the cardboard roll should be stored", "store the cardboard rool in the warehouse", "update the quantity of that cardboard rolls in the warehouse"]

Process description: {input}
Response:
"""


class TaskLLM():

    def __init__(self, model, openai_key, temperature=0.0):
        self.model = ChatOpenAI(model=model, openai_api_key=openai_key, temperature=temperature)

        self.prompt = PromptTemplate.from_template(TEMPLATE)

        self.output_parser = StrOutputParser()

    def get_chain(self) -> str:
        chain = self.prompt | self.model | self.output_parser
        return chain


class ProcessLLM:

    def __init__(self, model="gpt-3.5-turbo", openai_key=None, temperature=0.0):
        self.tasks_llm = TaskLLM(model, openai_key, temperature=temperature)

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

    def tasks_llm_parser(self) -> Runnable:
        task_llm_chain = self.tasks_llm.get_chain()

        task_llm_chain_output = {
            "tasks": task_llm_chain,
            "input": RunnablePassthrough()
        }

        return task_llm_chain_output

    def get_chain(self):
        task_llm_chain_output = self.tasks_llm_parser()

        chain = (
            task_llm_chain_output
            | RunnableLambda(
                lambda x: {
                    "tasks": x["tasks"],
                    "has_tasks": self.is_list_of_tasks(x["tasks"]),
                    "input": x["input"]
                }
            )
            | RunnableBranch(
                (lambda x: x["has_tasks"], RunnableLambda(lambda x: {
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

    for model in models:

        llm = ProcessLLM(model=model, openai_key=OPENAI_API_KEY)

        dataset = pd.read_csv("LLMtools2process_v2/processes_tools.csv")

        res_eval = []
        for index, row in dataset.iterrows():
            input_text = row["process"]
            res = llm.get_chain().invoke({"input": input_text})
            print(f"res: {res}")
            if res != "Your process description does not contain any task.":
                output = row["tools"]
                output = ast.literal_eval(output)
                tool_extracted = res["tools"]

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

                res_elem = [input_text, output, tool_correct, tool_no_correct, precision, recall]
            else:
                res_elem = [input_text, None, [], [], 0.0, 0.0]

            res_eval.append(res_elem)

        res_df = pd.DataFrame(res_eval, columns=["process", "tools", "correct", "no_correct", "precision", "recall"])

        if model == "gpt-3.5-turbo-16k":
            res_df.to_csv('eval_task_gpt35.csv', sep=',', index=False)
        else:
            res_df.to_csv('eval_task_gpt4.csv', sep=',', index=False)