import pandas as pd
import matplotlib.pyplot as plt

dataset = pd.read_csv("./processed_blocks.csv")
dataset = dataset.sort_values(by = "block_number", ignore_index = True)

# get utilization
dataset["utilization"] = dataset["gas_used"]/dataset["gas_limit"]

# Jan 1st
start = 9195000
view = dataset[dataset["block_number"] > start]
end = view["block_number"].iloc[-1]

util = view["utilization"]
total = util.count()

num_empty = util[util == 0.0].count()
num_over_ninety = util[util >= 0.9].count()
num_over_ninetyfive = util[util >= 0.95].count()

print(f"Start: {start}. End: {end}")
print(f"Got {num_empty / total * 100}% empty blocks")

for num in [0.5, 0.9, 0.95]:
    count = util[util >= num].count()
    utilized = count / total * 100
    print(f"Got {utilized}% blocks with at least {num * 100}% utilization")

