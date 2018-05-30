import argparse
import pickle
import numpy as np
from utils import simulate_local
import time

GRID_SIZE = 50
ITERATIONS_PER_SITE = 5000
BURN_IN = 1000
SAMPLE_RATE = 10

parser = argparse.ArgumentParser()
parser.add_argument("temperature", help="temperature to run the experiment at", type=float)
parser.add_argument("grid_size", help="size of the grid to use", type=float)
parser.add_argument("outfile", help="name of the place to write the metrics to", type=str)
args = parser.parse_args()

print("Running simulation for temperature:", args.temperature)
s = time.time()
metrics = simulate_local(args.grid_size, ITERATIONS_PER_SITE, args.temperature, burn_in=BURN_IN, sample_rate=SAMPLE_RATE)

with open(args.outfile, 'wb') as f:
    pickle.dump(metrics, f)
print("Simulation took", time.time() - s, "s")