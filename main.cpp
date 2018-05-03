// Ising model simulation
#include <iostream>
#include <random>
#include <Eigen/Dense>

using namespace std;
using namespace Eigen;

void simulate(int grid_size) {
    default_random_engine generator;
    uniform_int_distribution<int> distribution(0,1);
    MatrixXd m(grid_size, grid_size);
    for (size_t i = 0; i < grid_size; i++) {
        for (size_t j = 0; j < grid_size; j++) {
            m(i,j) = distribution(generator);
        }
    }
    cout << m << endl;
}

int main()
{
  simulate(10);
}