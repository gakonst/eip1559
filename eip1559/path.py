# path dependence check

from utils import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sys

b2_basefee = calculate_basefee(basefee, 500000)
b3_basefee = calculate_basefee(b2_basefee, 1000000)
print(b3_basefee)

s2_b2_basefee = calculate_basefee(basefee, 1000000)
s2_b3_basefee = calculate_basefee(s2_b2_basefee, 500000)
print(s2_b3_basefee)

s3_basefee = calculate_basefee(basefee, 1500000)
print(s3_basefee)
