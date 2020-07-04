import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import numpy as np

data = {'January': [69.91352170809841, 50.141917350433495], 'February': [79.47924908293174, 66.34981935276836], 'March': [83.4955377644006, 73.03625670165266], 'April': [87.50850674176574, 80.36726993067352], 'May': [97.45157381638717, 92.88919380985841], 'June': [99.47438018357964, 97.04601663171756]}

fifty = []
ninety = []
for d in data.values():
    fifty.append(d[0])
    ninety.append(d[1])

fig, ax = plt.subplots()
ax.plot(fifty, marker = 'x', linewidth = 4, markersize = 12)
ax.plot(ninety, marker = 'x', linewidth = 4, markersize = 12)

ax.set_title("")
ax.set_xlabel("Month", size = 22)
ax.set_ylabel("Percentage of blocks\nabove % utilization during each month", size = 22)

ax.legend(['>50% utilization', '>95% utilization'], prop={'size': 16})
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

plt.xticks(np.arange(6), (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
))
ax.tick_params(axis='both', which='major', labelsize=20)
plt.ylim([0, 100])
plt.show()
