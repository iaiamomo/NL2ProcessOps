import json
import pandas as pd
import numpy as np

filename = "results.csv"
dataset = pd.read_csv(filename)

val_1_1 = []
val_1_2 = []
val_1_3 = []

val_2_1 = []
val_2_2 = []
val_2_3 = []

for index, row in dataset.iterrows():
    columns = dataset.columns
    columns = columns[2:]
    for i in range(0, len(columns), 6):
        val_1_1.append(row[columns[i]])
        val_1_2.append(row[columns[i + 1]])
        val_1_3.append(row[columns[i + 2]])

        val_2_1.append(row[columns[i + 3]])
        val_2_2.append(row[columns[i + 4]])
        val_2_3.append(row[columns[i + 5]])

print("NL2ProcessOps")
res_1_1 = np.mean(val_1_1)
res_1_2 = np.mean(val_1_2)
res_1_3 = np.mean(val_1_3)
print(f"Criterion 1: {res_1_1}")
print(f"Criterion 2: {res_1_2}")
print(f"Criterion 3: {res_1_3}")

res_1_1 = np.var(val_1_1)
res_1_2 = np.var(val_1_2)
res_1_3 = np.var(val_1_3)
print(f"Variance Criterion 1: {res_1_1}")
print(f"Variance Criterion 2: {res_1_2}")
print(f"Variance Criterion 3: {res_1_3}")

import matplotlib.pyplot as plt
elems = (1,2,3,4,5)
val_1_1 = [val_1_1.count(1), val_1_1.count(2), val_1_1.count(3), val_1_1.count(4), val_1_1.count(5)]
val_1_2 = [val_1_2.count(1), val_1_2.count(2), val_1_2.count(3), val_1_2.count(4), val_1_2.count(5)]
val_1_3 = [val_1_3.count(1), val_1_3.count(2), val_1_3.count(3), val_1_3.count(4), val_1_3.count(5)]
crit = {
    "criterion_1": val_1_1,
    "criterion_2": val_1_2,
    "criterion_3": val_1_3,
}
x = np.arange(len(elems))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in crit.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xticks(x + width, elems)
ax.legend(loc='upper left', ncols=3)

plt.show(block=False)


print("Copilot")
res_2_1 = np.mean(val_2_1)
res_2_2 = np.mean(val_2_2)
res_2_3 = np.mean(val_2_3)
print(f"Criterion 1: {res_2_1}")
print(f"Criterion 2: {res_2_2}")
print(f"Criterion 3: {res_2_3}")

res_2_1 = np.var(val_2_1)
res_2_2 = np.var(val_2_2)
res_2_3 = np.var(val_2_3)
print(f"Variance Criterion 1: {res_2_1}")
print(f"Variance Criterion 2: {res_2_2}")
print(f"Variance Criterion 3: {res_2_3}")

elems = (1,2,3,4,5)
val_2_1 = [val_2_1.count(1), val_2_1.count(2), val_2_1.count(3), val_2_1.count(4), val_2_1.count(5)]
val_2_2 = [val_2_2.count(1), val_2_2.count(2), val_2_2.count(3), val_2_2.count(4), val_2_2.count(5)]
val_2_3 = [val_2_3.count(1), val_2_3.count(2), val_2_3.count(3), val_2_3.count(4), val_2_3.count(5)]
crit = {
    "criterion_1": val_2_1,
    "criterion_2": val_2_2,
    "criterion_3": val_2_3,
}
x = np.arange(len(elems))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in crit.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xticks(x + width, elems)
ax.legend(loc='upper left', ncols=3)

plt.show()