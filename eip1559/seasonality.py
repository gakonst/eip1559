from itertools import chain, repeat, cycle, islice
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sys

LOW_SEASON_DURATION = int(sys.argv[1]) # hours
NUM_CYCLES = int(sys.argv[2]) # number of cycles to observe
NUM_EXTRA_BLOCKS = int(sys.argv[3])
# ETH = int(sys.argv[4])
ETH = 240

# EIP1559 constants
constants = {
    "BASEFEE_MAX_CHANGE_DENOMINATOR": 8.0,
    "TARGET_GAS_USED": 10000000.0,
    "MAX_GAS_EIP1559": 16000000,
    "EIP1559_DECAY_RANGE": 800000,
    "EIP1559_GAS_INCREMENT_AMOUNT": 10.0,
    "INITIAL_BASEFEE": 10000000000.0,
    "PER_TX_GASLIMIT": 8000000,
}

BLOCKS_PER_MINUTE = 4 # assume 15 sec per block for convenience

def generate_seasonal_data(low, high, low_reps, high_reps, num_cycles):
    # generate the iterators for each demand type
    low_demand_iter = repeat(low, low_reps)
    high_demand_iter = repeat(high, high_reps)

    # 1 cycle
    data = cycle(chain(low_demand_iter, high_demand_iter))

    # n cycles
    demand = islice(
        data,
        (low_reps + high_reps) * num_cycles
    )

    return demand

# runs the EIP1559 calculation in usd
def calculate_basefee(basefee, delta):
    new_basefee = basefee + basefee * delta / constants["TARGET_GAS_USED"] / constants["BASEFEE_MAX_CHANGE_DENOMINATOR"]
    # apply the clipping
    if new_basefee > 125 * basefee / 100:
        new_basefee = 125 * basefee / 100
    if new_basefee < 87.5 * basefee / 100:
        new_basefee = 87.5 * basefee / 100
    return new_basefee

def hours_to_blocks(duration):
    return duration * 60 * BLOCKS_PER_MINUTE # blocks

def gas_to_usd(gas_price, eth_price):
    usd = gas_price * 21000 * eth_price * 1e-18
    return usd

HIGH_SEASON_DURATION = LOW_SEASON_DURATION # high season lasts 1 hour more than low

LOW_DEMAND = 5000000 # gas
HIGH_DEMAND = 15000000 # gas

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
deltas = map(
        lambda block_consumption: 
            block_consumption - constants["TARGET_GAS_USED"], 
        demand
)


basefee = constants["INITIAL_BASEFEE"]
rows = [{"basefee_usd": gas_to_usd(basefee, ETH) , "delta": 0 }]

# generate the data
for delta in deltas:
    new_basefee = calculate_basefee(basefee, delta) 
    # update to the new value
    basefee = new_basefee
    rows += [{"basefee_usd": gas_to_usd(new_basefee, ETH), "delta": delta }]

# index = block number, cols = basefee, delta
df = pd.DataFrame(rows)

fig, ax = plt.subplots()
basefee_plot = ax.plot(df.basefee_usd)

ax.set_title(f"{NUM_CYCLES} cycles: \
Low Season: {LOW_SEASON_DURATION} hours ({low_season_blocks} blocks) | \
High Season: {HIGH_SEASON_DURATION} hours ({high_season_blocks} blocks) \
")
ax.set_ylabel("BASEFEE (USD)", color = "blue")
ax.set_xlim(xmin=0)
# ax.set_yscale('log')



ax2 = ax.twinx()
delta_plot = ax2.plot(df.delta, color = "red", ls = "dotted")
ax2.set_ylabel("delta", color = "red")
ax2.set_ylim([-10000000, 6000000])
ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))

plt.show()
