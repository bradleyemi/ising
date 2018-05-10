import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import subprocess

def simulate(grid_size, iterations_per_site, temperature, outfile):
    with open(outfile, 'w') as f:
        subprocess.run(["./ising", str(grid_size), str(iterations_per_site), str(temperature)], stdout=f)

def load_matrix(infile):
    with open(infile, 'r') as f:
        arr = np.loadtxt(f)
    return arr

def plot_matrix(arr):
    img = plt.imshow((arr + 1.) * 255. / 2.)
    plt.show()
