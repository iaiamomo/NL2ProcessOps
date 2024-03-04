import pandas as pd

cases = ["task", "mod_task", "mod_task_pre"]
models = ["gpt35", "gpt4"]
version = "v1"

res = []
for case in cases:
    for model in models:
        filename = f"data_{version}/eval_{case}_fs_{model}.csv"
        dataset = pd.read_csv(filename)

        recall = 0
        precision = 0

        for index, row in dataset.iterrows():
            recall += row["recall"]
            precision += row["precision"]

        recall = recall / len(dataset)
        precision = precision / len(dataset)

        res.append([case, model, recall, precision])

res_df = pd.DataFrame(res, columns=["case", "model", "recall", "precision"])

print(res_df)
