import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import subprocess
import signal

def simulate(grid_size, iterations_per_site, temperature):
    
    chld = subprocess.Popen(["./ising",
                             str(grid_size),
                             str(iterations_per_site),
                             str(temperature)],
                             stdout=subprocess.PIPE)
    
    means = []
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
        #print(arr)
        means.append(arr.mean())
        if np.any(np.logical_and(arr != -1, arr != 1)):
            print(arr)
            print(np.logical_and(arr != -1, arr != 1))
            raise ValueError("Invalid array value.")
        chld.send_signal(signal.SIGCONT)
    
    signal.signal(signal.SIGCHLD, handler)
    chld.wait()
    #print(means)
    return np.array(means).mean()

def plot_matrix(arr):
    img = plt.imshow((arr + 1.) * 255. / 2.)
    plt.show()
