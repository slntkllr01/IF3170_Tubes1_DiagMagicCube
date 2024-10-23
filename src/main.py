
from algorithm.restart import RandomRestart
from algorithm.stochastic import Stochastic

# main buat ngetes sementara, nanti ganti aja
def main():
    # random_restart_solver = RandomRestart()
    # max_restarts = 10
    # best_solution = random_restart_solver.solveCube(maxRestart=max_restarts)

    stochastic_solver = Stochastic()
    max_restarts = 10000
    best_solution = stochastic_solver.solveCube(max_restarts)

    print("Best Solution Cube:")
    best_solution.showCube()
    print(f"Best Heuristic Value: {best_solution.current_value}")

if __name__ == "__main__":
    main()
