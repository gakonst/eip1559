from itertools import chain, repeat, cycle, islice

# eth price
ETH = 240

BLOCKS_PER_MINUTE = 4  # assume 15 sec per block for convenience

# returns the USD required for a simple 21k gas transaction


def gas_to_usd(gas_price, eth_price):
    usd = gas_price * 21000 * eth_price * 1e-18
    return usd

# returns a seasonal series of low/high gas consumptions repeating `num_cycles`
# times


def generate_seasonal_data(low, high, low_reps, high_reps, num_cycles, start_with_high=True):
    # generate the iterators for each demand type
    low_demand_iter = repeat(low, low_reps)
    high_demand_iter = repeat(high, high_reps)

    # 1 cycle
    if start_with_high:
        data = cycle(chain(high_demand_iter, low_demand_iter))
    else:
        data = cycle(chain(low_demand_iter, high_demand_iter))

    # n cycles
    demand = islice(
        data,
        (low_reps + high_reps) * num_cycles
    )

    return demand


# EIP1559 constants
eip1559_constants = {
    "BASEFEE_MAX_CHANGE_DENOMINATOR": 8.0,
    "TARGET_GAS_USED": 10000000.0,
    "EIP1559_DECAY_RANGE": 800000,
    "EIP1559_GAS_INCREMENT_AMOUNT": 10.0,
    "INITIAL_BASEFEE": float(1e9),
    "PER_TX_GASLIMIT": 8000000,
}
eip1559_constants["MAX_GAS_EIP1559"] = 2 * eip1559_constants["TARGET_GAS_USED"]

# runs the EIP1559 calculation in usd


def calculate_basefee(basefee, delta):
    new_basefee = basefee + basefee * delta / \
        eip1559_constants["TARGET_GAS_USED"] / \
        eip1559_constants["BASEFEE_MAX_CHANGE_DENOMINATOR"]
    # apply the clipping
    if new_basefee > 125 * basefee / 100:
        new_basefee = 125 * basefee / 100
    if new_basefee < 87.5 * basefee / 100:
        new_basefee = 87.5 * basefee / 100
    return new_basefee


def hours_to_blocks(duration):
    return duration * 60 * BLOCKS_PER_MINUTE  # blocks


def get_delta(demand):
    return map(
        lambda block_consumption:
        block_consumption - eip1559_constants["TARGET_GAS_USED"],
        demand
    )
