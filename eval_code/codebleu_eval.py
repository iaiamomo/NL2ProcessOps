import pandas as pd
from codebleu import calc_codebleu

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
    res = []
    for i in range(1,11):
        process = f"p0{i}" if i < 10 else f"p{i}"

        filename = f"{run}/{process}_{model}.py"
        #filename = f"{run}/{process}.py"
        with open(filename, "r") as file:
            prediction = file.read()

        filename_ref = f"data/{process}/{process}_1.py"
        with open(filename_ref, "r") as file:
            reference = file.read()
        
        results = calc_codebleu([reference], [prediction], lang="python", weights = (0.1, 0.1, 0.4, 0.4), tokenizer = None)

        codebleu_res = results["codebleu"]
        bleu = results["ngram_match_score"]
        weighted_bleu = results["weighted_ngram_match_score"]
        sintax = results["syntax_match_score"]
        dataflow = results["dataflow_match_score"]

        res.append([model, process, codebleu_res, bleu, weighted_bleu, sintax, dataflow])

    print(f"Results for {run} - {model}")
    res_df = pd.DataFrame(res, columns=["model", "process", "codebleu", "bleu", "bleu_weight", "match_ast", "match_df"])
    print(res_df)

    # mean of codebleu
    mean_codebleu = res_df.groupby("model")["codebleu"].mean()
    mean_codebleu = pd.DataFrame([mean_codebleu])
    print(f"codebleu: {mean_codebleu.to_string(index=False, header=False).split()[0]}")

    # mean of bleu
    mean_bleu = res_df.groupby("model")["bleu"].mean()
    mean_bleu = pd.DataFrame([mean_bleu])
    print(f"bleu: {mean_bleu.to_string(index=False, header=False).split()[0]}")

    # mean of bleu_weight
    mean_bleu_weight = res_df.groupby("model")["bleu_weight"].mean()
    mean_bleu_weight = pd.DataFrame([mean_bleu_weight])
    print(f"bleu_weight: {mean_bleu_weight.to_string(index=False, header=False).split()[0]}")

    # mean of match_ast
    mean_match_ast = res_df.groupby("model")["match_ast"].mean()
    mean_match_ast = pd.DataFrame([mean_match_ast])
    print(f"match_ast: {mean_match_ast.to_string(index=False, header=False).split()[0]}")

    # mean of match_df
    mean_match_df = res_df.groupby("model")["match_df"].mean()
    mean_match_df = pd.DataFrame([mean_match_df])
    print(f"match_df: {mean_match_df.to_string(index=False, header=False).split()[0]}")

    print("_________________________")