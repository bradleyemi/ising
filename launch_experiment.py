import matplotlib.pyplot as plt
import numpy as np
from utils import *
import time

GRID_SIZE = 50
ITERATIONS_PER_SITE = 5000

temperature_range = np.arange(0.25, 5.0, 0.25)
all_metrics = []
for i, temperature in enumerate(temperature_range):
    print("Running simulation for temperature = {}".format(temperature))
    s = time.time()
    metrics = simulate_local(GRID_SIZE, ITERATIONS_PER_SITE, temperature)
    all_metrics.append(metrics)
    print("Time taken: ", time.time() - s, "s")
fig, axes = plt.subplots(2,2)
axes[0,0].errorbar(temperature_range,
	               [m.specific_heat for m in all_metrics],
	               yerr=[m.specific_heat_error for m in all_metrics]) 
axes[0,0].set_xlabel("Temperature")
axes[0,0].set_ylabel("Specific Heat per spin")
axes[0,0].set_title("Specific Heat per spin vs. Temperature")

axes[0,1].errorbar(temperature_range,
	               [m.magnetization for m in all_metrics],
	               yerr=[m.magnetization_error for m in all_metrics]) 
axes[0,1].set_xlabel("Temperature")
axes[0,1].set_ylabel("Magnetization per spin")
axes[0,1].set_title("Magnetization per spin vs. Temperature")

axes[1,0].errorbar(temperature_range,
	               [m.energy for m in all_metrics],
	               yerr=[m.energy_error for m in all_metrics]) 
axes[1,0].set_xlabel("Temperature")
axes[1,0].set_ylabel("Energy")
axes[1,0].set_title("Energy vs. Temperature")

axes[1,1].errorbar(temperature_range,
	           [m.susceptibility for m in all_metrics],
	           yerr=[m.susceptibility_error for m in all_metrics]) 
axes[1,1].set_xlabel("Temperature")
axes[1,1].set_ylabel("Magnetic Susceptibility")
axes[1,1].set_title("Magnetic Susceptibility vs. Temperature")

plt.show()