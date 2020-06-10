from utils import gas_to_usd, ETH, BLOCKS_PER_MINUTE

import numpy as np
import matplotlib.pyplot as plt

duration = BLOCKS_PER_MINUTE * 30 # 30 mins
x = np.arange(0, duration)
y = gas_to_usd(1e9 * (1 + 0.125)**x, ETH)

# fees after 0, 1, 10, 100, 119 blocks
print(y[0])
print(y[1])
print(y[10])
print(y[100])
print(y[119])

fix, ax = plt.subplots()
ax.set_title("Exponential fee growth on full blocks over 30 minutes")
ax.plot(x, y)
# ax.set_yscale("log")
ax.set_ylabel("ETH Transfer Cost (USD)")
ax.set_xlabel("# Blocks")
plt.show()
