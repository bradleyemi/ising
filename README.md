# ising

A basic simulation of the 2D Ising model, implemented in C++. Right now we only simulate the zero-field case. More features to come!

## Installation

#### Dependencies:

C++11

g++ >= 4.2.1 (lower versions probably fine, but untested)

[Eigen](http://eigen.tuxfamily.org/dox/GettingStarted.html), source files inside or symlinked to `/usr/local/include`

On OS X you can simply:

```
brew install eigen
```

## Usage:

The basic program simulates for the specified number of iterations, and then prints the grid to the console.

```
make
```
```
./ising <grid_size> <iterations_per_site> [<temperature>] [<J>]
```

To save the grid to a file instead:

```
./ising <grid_size> <iterations_per_site> [<temperature>] [<J>] > myfile.txt
```

### Required arguments:

`grid_size` : height and width of the grid

`iterations_per_site` : number of iterations to run the algorithm per site


### Optional arguments:

`temperature`: temperature in energy units (i.e., k = 1). Alternatively, 1 / beta = `temperature`.

`J`: interaction strength constant

## Contact:

bemi@stanford.edu
