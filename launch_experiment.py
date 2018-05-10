import matplotlib.pyplot as plt
import numpy as np
import utils

GRID_SIZE = 50
ITERATIONS_PER_SITE = 10000

temperature_range = np.arange(0.2, 5.0, 0.1)
mags = []
for i, temperature in enumerate(temperature_range):
    print("Running simulation for temperature = {}".format(temperature))
    utils.simulate(GRID_SIZE, ITERATIONS_PER_SITE, temperature, "./experiments/basic_temperature/ising_{}.txt".format(i))
    arr = utils.load_matrix("./experiments/basic_temperature/ising_{}.txt".format(i))
    mags.append(arr.mean())

print("Plotting...")
plt.plot(temperature_range, np.array(mags))
plt.xlabel("Temperature")
plt.ylabel("Mean magnetization")
plt.title("Ising model simulation for 50x50 grid after 10000 iterations per site")
plt.show()