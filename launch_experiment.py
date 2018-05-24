import matplotlib.pyplot as plt
import numpy as np
import utils

GRID_SIZE = 100
ITERATIONS_PER_SITE = 10000

temperature_range = np.arange(0.25, 5.0, 0.25)
mags = []
for i, temperature in enumerate(temperature_range):
    print("Running simulation for temperature = {}".format(temperature))
    avg_magnetization = utils.simulate(GRID_SIZE, ITERATIONS_PER_SITE, temperature)
    mags.append(avg_magnetization)

print("Plotting...")
print(temperature_range)
print(mags)
plt.plot(temperature_range, np.array(mags))
plt.xlabel("Temperature")
plt.ylabel("Mean magnetization")
plt.title("Magnetization for 100x100 grid (10,000 iterations per site, 1,000 iteration burn-in)")
plt.show()