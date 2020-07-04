import matplotlib
import matplotlib.pyplot as plt
font = {'family' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)
from utils import *

MAX_ITERS = 10000
NUM_FULL_BLOCKS = 100

# the initial basefee is going to be 1.125 ^ i * constants['basefee']
initial_basefee = eip1559_constants["INITIAL_BASEFEE"] * 1.125**NUM_FULL_BLOCKS
print("High congestion basefee", initial_basefee)

# calculates the number of blocks required to get back to the initial gas consumption
def pullback(gas):
    for k in range(0, MAX_ITERS):
        # generate a low consumption dist
        demand = repeat(gas, k)

        # the delta is the diff from the current value
        deltas = get_delta(demand)
        basefee = initial_basefee

        for delta in deltas:
            new_basefee = calculate_basefee(basefee, delta)
            if new_basefee < eip1559_constants["INITIAL_BASEFEE"]:
                # print(
                #     f"It took {k} blocks of {gas} gas for the basefee to get within 1e9 of its original value: new_basefee: {new_basefee}")
                return k
            # update to the new value
            basefee = new_basefee


fig = plt.figure()
ax = plt.subplot(111)

block_sizes = [0, 2.5e6, 5e6, 7.5e6]
num_blocks = []
for gas in block_sizes:
    num_blocks.append(pullback(gas))

print(num_blocks)
x = [b / 1e6 for b in block_sizes]
print(x)

plt.xticks(x, x)

ax.bar(x, num_blocks, align = 'center', )
ax.set_xlabel("Gas consumed per block (1e6)", fontsize = 32)
ax.set_ylabel("Number of blocks to get back to normal", fontsize = 32)
ax.set_title("Number of consecutive blocks required to reach the previous BASEFEE\n value after 100 consecutive full blocks", fontsize = 38)
ax.tick_params(axis='both', which='major', labelsize=28)

fig.tight_layout()
# ax.autoscale(tight=True)

plt.show()
