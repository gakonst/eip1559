import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dataset = pd.read_csv("./processed_blocks.csv")
dataset = dataset.sort_values(by = "block_number", ignore_index = True)

# get utilization
dataset["utilization"] = dataset["gas_used"]/dataset["gas_limit"]

# Jan 1st
start = 9195000
view = dataset[dataset["block_number"] > start]
end = view["block_number"].iloc[-1]

gas = view[["block_number", "utilization"]]
non_zero = gas[gas["utilization"] != 0].reset_index(drop=True)

chunks = 6
length = int(len(non_zero) / chunks) * chunks
non_zero = non_zero.iloc[:length]
non_zero
# gas.plot()
# plt.show()

chunk_size = int(length / chunks)
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
]

# data to plot
n_groups = len(months)
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8

# colors = ['g', 'g']

utilizations = {}
for i in range(chunks):
    start = i * chunk_size
    end = (i + 1) * chunk_size
    segment = non_zero.iloc[start:end]

    # ensure we have excluded empty blocks
    assert len(segment [ segment["utilization"] == 0 ]) == 0

    util = segment["utilization"]

    print(f"\n{months[i]}")
    vals = []
    for idx, num in enumerate([0.5, 0.95]):
        count = util[util >= num].count()
        utilized = count / chunk_size * 100
        vals.append(utilized)
        print(f"Got {utilized}% blocks with at least {num * 100}% utilization")
        # plt.bar(i + idx * bar_width, vals, bar_width, alpha = opacity, color = '')
    utilizations[months[i]] = vals

print(utilizations)

# rects1 = plt.bar(index, means_frank, bar_width,
# alpha=opacity,
# color='b',
# label='Frank')
# 
# rects2 = plt.bar(index + bar_width, means_guido, bar_width,
# alpha=opacity,
# color='g',
# label='Guido')
# 
# plt.xlabel('Person')
# plt.ylabel('Scores')
# plt.title('Scores by person')
# plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
# plt.legend()
# 
# plt.tight_layout()
# plt.show()
