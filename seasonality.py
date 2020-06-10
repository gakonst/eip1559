from utils import *

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sys

LOW_SEASON_DURATION = int(sys.argv[1])  # hours
NUM_CYCLES = int(sys.argv[2])  # number of cycles to observe
NUM_EXTRA_BLOCKS = int(sys.argv[3])

# high season lasts 1 hour more than low
HIGH_SEASON_DURATION = LOW_SEASON_DURATION

LOW_DEMAND = 5000000  # gas
HIGH_DEMAND = 15000000  # gas

low_season_blocks = hours_to_blocks(LOW_SEASON_DURATION)
high_season_blocks = hours_to_blocks(HIGH_SEASON_DURATION) + NUM_EXTRA_BLOCKS

demand = generate_seasonal_data(
    LOW_DEMAND,
    HIGH_DEMAND,
    low_season_blocks,
    high_season_blocks,
    NUM_CYCLES
)

# the delta is the diff from the current value
deltas = get_delta(demand)

basefee = eip1559_constants["INITIAL_BASEFEE"]
rows = [{"basefee_usd": gas_to_usd(basefee, ETH), "delta": 0}]

# generate the data
for delta in deltas:
    new_basefee = calculate_basefee(basefee, delta)
    # update to the new value
    basefee = new_basefee
    rows += [{"basefee_usd": gas_to_usd(new_basefee, ETH), "delta": delta}]

# index = block number, cols = basefee, delta
df = pd.DataFrame(rows)

fig, ax = plt.subplots()
basefee_plot = ax.plot(df.basefee_usd)

ax.set_title(f"{NUM_CYCLES} cycles: \
Low Season: {LOW_SEASON_DURATION} hours ({low_season_blocks} blocks) | \
High Season: {HIGH_SEASON_DURATION} hours ({high_season_blocks} blocks) \
")
ax.set_ylabel("BASEFEE (USD)", color="blue")
ax.set_xlim(xmin=0)
# ax.set_yscale('log')

ax2 = ax.twinx()
delta_plot = ax2.plot(df.delta, color="red", ls="dotted")
ax2.set_ylabel("delta", color="red")
ax2.set_ylim([-10000000, 6000000])
ax2.yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, p: format(int(x), ',')))

print(df)
plt.show()
