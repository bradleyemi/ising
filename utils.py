from copy import copy
import numpy as np
import random
import subprocess
import signal

class Metric(object):
    def __init__(self, magnetization, energy):
        self.abs_mean = np.absolute(magnetization)
        self.mean = magnetization
        self.mean_sq = magnetization ** 2
        self.energy = energy
        self.energy_sq = energy ** 2

class Metrics(object):
    def __init__(self, metrics, temperature, grid_size):
        self.temperature = temperature
        self.grid_size = grid_size
        self.metrics = metrics

        self.magnetization = self.calculate_magnetization(metrics)
        self.magnetization_error = self.calculate_error(self.calculate_magnetization)

        self.susceptibility = self.calculate_susceptibility(metrics)
        self.susceptibility_error = self.calculate_error(self.calculate_susceptibility)

        self.energy = self.calculate_energy(metrics)
        self.energy_error = self.calculate_error(self.calculate_energy)

        self.specific_heat = self.calculate_specific_heat(metrics)
        self.specific_heat_error = self.calculate_error(self.calculate_specific_heat)

    def calculate_magnetization(self, metrics_sample):
        return np.array([m.abs_mean for m in metrics_sample]).mean()

    def calculate_susceptibility(self, metrics_sample):
        return (self.grid_size ** 2 / self.temperature) * \
        (np.array([m.mean_sq for m in metrics_sample]).mean() - \
        np.array([m.mean for m in metrics_sample]).mean() ** 2)

    def calculate_energy(self, metrics_sample):
        return np.array([m.energy for m in metrics_sample]).mean()

    def calculate_specific_heat(self, metrics_sample):
        return (1. / (self.grid_size ** 2 * self.temperature ** 2)) * \
        (np.array([m.energy_sq for m in metrics_sample]).mean() - \
        np.array([m.energy for m in metrics_sample]).mean() ** 2)

    def calculate_error(self, metric_handle):
        ms = []
        m_sqs = []
        for _ in range(10):
            choice = np.random.choice(self.metrics, size=len(self.metrics), replace=True)
            m = metric_handle(choice)
            m_sq = metric_handle(choice) ** 2
            ms.append(m)
            m_sqs.append(m_sq)
        return np.sqrt(np.array(m_sqs).mean() - np.array(ms).mean() ** 2)

def get_energy(arr, J):
    energy = 0.
    up = np.roll(arr, 1, axis=0)
    down = np.roll(arr, -1, axis=0)
    left = np.roll(arr, -1, axis=1)
    right = np.roll(arr, 1, axis=1)
    return -J * np.multiply(arr, up + down + left + right)

def simulate_local(grid_size, iterations_per_site, temperature, J=1, burn_in=1000, sample_rate=10):
    metrics = []
    arr = np.ones((grid_size, grid_size))
    for i in range(int(grid_size ** 2 * iterations_per_site)):
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)

        left = arr[(x-1) % grid_size, y]
        right = arr[(x+1) % grid_size, y]
        up = arr[x, (y+1) % grid_size]
        down = arr[x, (y-1) % grid_size]

        dE = 2 * J * arr[x,y] * (left + right + up + down)
        if (dE <= 0):
            arr[x,y] = -arr[x,y]
        elif random.random() < np.exp(-dE / temperature):
            arr[x,y] = -arr[x,y]
        if (i % (grid_size ** 2 * sample_rate) == 0) and (i >= grid_size ** 2 * burn_in):
            metrics.append(Metric(arr.mean(), get_energy(arr, J)))
    return Metrics(metrics, temperature, grid_size)

def get_neighbors(spin, arr):
    x = spin[0]
    y = spin[1]
    grid_size = arr.shape[0]
    left = ((x-1) % grid_size, y, arr[(x-1) % grid_size, y])
    right = ((x+1) % grid_size, y, arr[(x+1) % grid_size, y])
    up = (x, ((y+1) % grid_size), arr[x, (y+1) % grid_size])
    down = (x, ((y-1) % grid_size), arr[x, (y-1) % grid_size])
    neighbors = [left, right, up, down]
    return neighbors

def simulate_wolff(grid_size, iterations_per_site, temperature, J=1, burn_in=1000, sample_rate=10):
    metrics = []
    arr = np.ones((grid_size, grid_size))
    flips = 0
    add_probability = 1 - np.exp(-2 * J / temperature)
    while flips < int(grid_size ** 2 * iterations_per_site):
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        # a spin is a tuple of x coordinate, y coordinate, spin
        seed = (x, y, arr[x, y])
        cluster = []
        cluster.append(seed)
        i = 0
        while i < len(cluster):
            spin = cluster[i]
            neighbors = get_neighbors(spin, arr)
            for neighbor in neighbors:
                if neighbor in cluster:
                    continue
                if (neighbor[2] == seed[2]) and (random.random() < add_probability):
                    cluster.append(neighbor)
            i += 1
        for spin in cluster:
            arr[spin[0], spin[1]] = -arr[spin[0], spin[1]]
        old_flips = copy(flips)
        flips += len(cluster)
        for it in range(old_flips, flips):
            if (it % (grid_size ** 2 * sample_rate) == 0) and (it >= grid_size ** 2 * burn_in):
                metrics.append(Metric(arr.mean(), get_energy(arr, J)))
    return Metrics(metrics, temperature, grid_size)




def simulate(grid_size, iterations_per_site, temperature, J=1):
    chld = subprocess.Popen(["./ising",
                             str(grid_size),
                             str(iterations_per_site),
                             str(temperature),
                             str(J)],
                             stdout=subprocess.PIPE)
    
    metrics = []
    def handler(signum, frame):
        arr = np.zeros((grid_size, grid_size))
        rows_parsed = 0
        for i, line in enumerate(chld.stdout):
            if line.decode().strip('\n') == "DONE":
                return
            if line.decode().strip('\n') == "STOP":
                break
            try:
                parse = np.array(list(filter(lambda x: x != '', line.decode().strip('\n').split(' '))))
                assert(len(parse) == grid_size)
            except:
                pass
            arr[i, :] = parse
        # error checking
        if np.any(np.logical_and(arr != -1, arr != 1)):
            chld.send_signal(signal.SIGCONT)
            return

        # postprocessing data analysis
        magnetization = arr.mean()
        energy = get_energy(arr, J)
        metrics.append(Metric(magnetization, energy))
        chld.send_signal(signal.SIGCONT)
    
    signal.signal(signal.SIGCHLD, handler)
    chld.wait()
    #print(means)
    return Metrics(metrics, temperature, grid_size)
