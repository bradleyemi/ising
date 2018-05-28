import argparse
import numpy as np
from utils import simulate_local
import time

GRID_SIZE = 50
ITERATIONS_PER_SITE = 5000
BURN_IN = 1000
SAMPLE_RATE = 10

parser = argparse.ArgumentParser()
parser.add_argument("temperature", help="temperature to run the experiment at", type=float)
args = parser.parse_args()

print("Running simulation for temperature:", args.temperature)
s = time.time()
metrics = simulate_local(GRID_SIZE, ITERATIONS_PER_SITE, args.temperature, BURN_IN, SAMPLE_RATE)
print("Simulation took", time.time() - s, "s")