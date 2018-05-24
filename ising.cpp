// Ising model simulation for Physics 113
// Bradley Emi (Spr 2018)
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <random>
#include <csignal>
#include <sys/types.h>
#include <unistd.h>
#include <Eigen/Dense>

using namespace std;
using namespace Eigen;

const int BURN_IN_ITERATIONS = 1000;
const int SAMPLE_RATE = 10;

// initializes a grid with random spins. 
void initialize(MatrixXd &m, int grid_size) {
    default_random_engine generator;
    uniform_int_distribution<int> spin_distribution(0,1);
    for (size_t i = 0; i < grid_size; i++) {
        for (size_t j = 0; j < grid_size; j++) {
            m(i,j) = 1; //+ 2 * spin_distribution(generator);
        }
    }
}

// gets the index one under idx, wraps around the grid if idx = 0
int get_index_below(int idx, int grid_size) {
    if (idx == 0) return grid_size - 1;
    else return idx - 1;
}

// gets the index one above idx, wraps around the grid if idx = grid_size - 1
int get_index_above(int idx, int grid_size) {
    if (idx == grid_size - 1) return 0;
    else return idx + 1;
}

void simulate(int grid_size, int iterations_per_site, double temperature=2.0, double J=1.0) {
    // get pid of this process
    pid_t pid = getpid();

    // initialize random number generator
    default_random_engine generator;
    uniform_int_distribution<int> index_distribution(0, grid_size - 1);
    uniform_real_distribution<double> acceptance_distribution(0.0, 1.0);

    // initialize the grid
    MatrixXd m(grid_size, grid_size);
    initialize(m, grid_size);

    // simulate...
    int iterations = iterations_per_site * grid_size * grid_size;
    for (int i = 0; i < iterations; i++) {
        // pick a random spin
        int x = index_distribution(generator);
        int y = index_distribution(generator);

        // get neighbors enforcing periodic boundary conditions
        int left = m(get_index_below(x, grid_size), y);
        int right = m(get_index_above(x, grid_size), y);
        int top = m(x, get_index_above(y, grid_size));
        int bottom = m(x, get_index_below(y, grid_size));

        // calculate energy difference between states and decide whether to accept
        double dE = 2 * J * m(x,y) * (left + right + top + bottom);
        //cout << "dE: " << dE << endl;
        //cout << "acceptance p: " << exp(-dE / temperature) << endl;
        if (m(x,y) <= 0) {
            m(x,y) = -m(x,y);
        }
        else if (acceptance_distribution(generator) < exp(-dE / temperature)) {
            m(x,y) = -m(x,y);
        }
        if ((i % (grid_size * grid_size * SAMPLE_RATE) == 0) &&
            (i >= grid_size * grid_size * BURN_IN_ITERATIONS)) {
            cout << m << endl;
            cout << "STOP" << endl;
            kill(pid, SIGSTOP);
        }
    }
    cout << "DONE" << endl;
}

int main(int argc, char* argv[])
{
  if (argc == 3) {
    int grid_size = atoi(argv[1]);
    int iterations_per_site = atoi(argv[2]);
    if (grid_size == 0 || iterations_per_site == 0) {
        cerr << "Usage: ./ising <grid_size> <iterations_per_site> [<temperature>] [<J>]" << endl;
    }
    simulate(grid_size, iterations_per_site);
  }
  else if (argc == 4) {
    int grid_size = atoi(argv[1]);
    int iterations_per_site = atoi(argv[2]);
    double temperature = atof(argv[3]);
    if (grid_size == 0 || iterations_per_site == 0 || temperature == 0) {
        cerr << "Usage: ./ising <grid_size> <iterations_per_site> [<temperature>] [<J>]" << endl;
    }
    simulate(grid_size, iterations_per_site, temperature);
  }
  else if (argc == 5) {
    int grid_size = atoi(argv[1]);
    int iterations_per_site = atoi(argv[2]);
    double temperature = atof(argv[3]);
    double J = atof(argv[4]);
    if (grid_size == 0 || iterations_per_site == 0 || temperature == 0 || J == 0) {
        cerr << "Usage: ./ising <grid_size> <iterations_per_site> [<temperature>] [<J>]" << endl;
    }
    simulate(grid_size, iterations_per_site, temperature, J);
  }
  else {
    cout << "argc " << argc;
    cerr << "Usage: ./ising <grid_size> <iterations_per_site> [<temperature>] [<J>]" << endl;
  }
}