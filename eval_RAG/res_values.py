import pandas as pd

cases = ["task", "mod_task", "mod_task_pre"]
few_shot = ["fs", "nfs"]
models = ["gpt35", "gpt4"]

res = []
for case in cases:
    for fs in few_shot:
        for model in models:
            filename = f"data/eval_{case}_{fs}_{model}.csv"
            dataset = pd.read_csv(filename)

            recall = 0
            precision = 0

            for index, row in dataset.iterrows():
                recall += row["recall"]
                precision += row["precision"]

            recall = recall / len(dataset)
            precision = precision / len(dataset)

            res.append([case, fs, model, recall, precision])

res_df = pd.DataFrame(res, columns=["case", "few_shot", "model", "recall", "precision"])

print(res_df)
