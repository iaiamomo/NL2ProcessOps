import json
import pandas as pd
import numpy as np

runs = ["run1", "run2", "run3", "run4", "run5"]
models = {
    "run1": "gpt4",
    "run2": "gpt",
    "run3": "gpt4",
    "run4": "gpt",
    "run5": "gpt4"
}

for run in runs:
    model = models[run]
    filename = f"{run}/eval_code_{model}.csv"
    dataset = pd.read_csv(filename)

    for index, row in dataset.iterrows():
        process = row["process"]
        code = row["code"]
        tools = row["tools"]

        new_code = ""

        if not pd.isnull(tools):
            tools = tools.split("\n")

            for tool in tools:
                if tool == "":
                    continue
                tool = json.loads(tool)
                new_code += f"from tools.{tool['actor']} import {tool['name']}\n"
            
            new_code += code
        else:
            print("No tools")

        new_py_file = f"{run}/{process}_{model}.py"
        with open(new_py_file, "w") as f:
            f.write(new_code)