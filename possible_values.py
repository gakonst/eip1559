import numpy as np
import matplotlib.pyplot as plt


# possible values between 0.875-1.125 of the basefee
initial_basefee = 100.0
x = np.linspace(0, 10) # simulate over 10 blocks
y1 = initial_basefee * (1 + 0.125)**x
y2 = initial_basefee * (1 - 0.125)**x

fix, ax = plt.subplots()
ax.set_title("MAX/MIN_BASEFEE_i = (1±0.125)^i * BASEFEE", fontsize = 38)
ax.fill_between(x, y1, y2)
ax.set_ylabel("Gas Price", fontsize = 32)
ax.set_xlabel("Number of blocks until transaction gets confirmed", fontsize = 32)
ax.tick_params(axis='both', which='major', labelsize=28)
plt.show()
