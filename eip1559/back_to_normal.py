from utils import *
import sys

MAX_ITERS = 10000
NUM_FULL_BLOCKS = int(sys.argv[1])
LOW_DEMAND_GAS = int(sys.argv[2])

# the initial basefee is going to be 1.125 ^ i * constants['basefee']
initial_basefee = eip1559_constants["INITIAL_BASEFEE"] * 1.125**NUM_FULL_BLOCKS
print("High congestion basefee", initial_basefee)

# calculates the number of blocks required to get back to the initial gas consumption
def pullback():
    for k in range(0, MAX_ITERS):
        # generate a low consumption dist
        demand = repeat(LOW_DEMAND_GAS, k)

        # the delta is the diff from the current value
        deltas = get_delta(demand)
        basefee = initial_basefee

        for delta in deltas:
            new_basefee = calculate_basefee(basefee, delta)
            print(new_basefee)
            if new_basefee < eip1559_constants["INITIAL_BASEFEE"]:
                print(
                    f"It took {k} blocks of {LOW_DEMAND_GAS} gas for the basefee to get within 1e9 of its original value: new_basefee: {new_basefee}")
                return k
            # update to the new value
            basefee = new_basefee


k = pullback()
