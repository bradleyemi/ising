import argparse
import pickle
import numpy as np
from utils import simulate_local, simulate_wolff
import time

ITERATIONS_PER_SITE = 5000
BURN_IN = 1000
SAMPLE_RATE = 10

parser = argparse.ArgumentParser()
parser.add_argument("grid_size", help="size of the grid to use", type=int)
parser.add_argument("temperature", help="temperature to run the experiment at", type=float)
parser.add_argument("outfile", help="name of the place to write the metrics to", type=str)
parser.add_argument("--wolff", help="use the Wolff algorithm", action='store_true')
args = parser.parse_args()


s = time.time()
if args.wolff:
    print("Running Wolff simulation for temperature:", args.temperature)
    metrics = simulate_wolff(args.grid_size, ITERATIONS_PER_SITE, args.temperature, burn_in=BURN_IN, sample_rate=SAMPLE_RATE)
    print("Specific heat:", metrics.specific_heat)
else:
    print("Running Metropolis simulation for temperature:", args.temperature)
    metrics = simulate_local(args.grid_size, ITERATIONS_PER_SITE, args.temperature, burn_in=BURN_IN, sample_rate=SAMPLE_RATE)
    print("Energy:", metrics.energy)
    print("Specific heat:", metrics.specific_heat)

with open(args.outfile, 'wb') as f:
    pickle.dump(metrics, f)
print("Simulation took", time.time() - s, "s")