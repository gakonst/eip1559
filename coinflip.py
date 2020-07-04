import random
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from utils import *

# biased coinflip which returns `low` if it falls on a number <p_hi
def flip(p_low, low, high):
    return low if random.random() < p_low else high

# number of blocks
n_blocks = 100

# gas
high_block = 20e6
low_block = 0e6

# probability of mining a `low_block`
probabilities = [0.2, 0.35, 0.5, 0.55]

# create the figure and 4 subfigures
fig, ax = plt.subplots()

for p in probabilities:
    basefee = eip1559_constants["INITIAL_BASEFEE"]
    rows = [{"basefee_usd": gas_to_usd(basefee, ETH), "delta": 0}]

    # simulate for this distribution
    for i in range(n_blocks):
        block = flip(p, low_block, high_block)
        delta = block - eip1559_constants["TARGET_GAS_USED"]

        new_basefee = calculate_basefee(basefee, delta)
        # update to the new value
        basefee = new_basefee
        rows += [{"basefee_usd": gas_to_usd(new_basefee, ETH), "delta": delta}]

    df = pd.DataFrame(rows)
    print(df)

    basefee_plot = ax.plot(df.basefee_usd)

ax.legend(loc='upper left', frameon=False)
plt.show()

# ax.set_title(f"{NUM_CYCLES} cycles: \
# Low Season: {LOW_SEASON_DURATION} hours ({low_season_blocks} blocks) | \
# High Season: {HIGH_SEASON_DURATION} hours ({high_season_blocks} blocks) \
# ")
# ax.set_ylabel("BASEFEE (USD)", color="blue")
# ax.set_xlim(xmin=0)
# # ax.set_yscale('log')
# 
# ax2 = ax.twinx()
# delta_plot = ax2.plot(df.delta, color="red", ls="dotted")
# ax2.set_ylabel("delta", color="red")
# ax2.set_ylim([-10000000, 6000000])
# ax2.yaxis.set_major_formatter(
#     mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
# 
# print(df)
# plt.show()
