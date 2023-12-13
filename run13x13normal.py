import argparse
import threading

from snake.game import Game, GameConf, GameMode


def main(prod,choosen_solver, mode):
    dict_solver = {
        "greedy": "GreedySolver",
        "hamilton": "HamiltonSolver",
        "dqn": "DQNSolver",
    }

    dict_mode = {
        "normal": GameMode.NORMAL,
        "bcmk": GameMode.BENCHMARK,
    }

    parser = argparse.ArgumentParser(description="Run snake game agent.")
    parser.add_argument("-s", default="greedy", choices=dict_solver.keys(),
                        help="name of the solver to direct the snake (default: hamilton)")
    parser.add_argument("-m", default=mode, choices=dict_mode.keys(),
                        help="game mode (default: normal)")
    args = parser.parse_args()
    
    solver = dict_solver[choosen_solver]
    rows = 13*prod
    
    conf = GameConf(rows,solver)
    conf.solver_name = dict_solver[args.s]
    conf.mode = dict_mode[args.m]
    print(f"Solver: {conf.solver_name}   Mode: {conf.mode}")

    Game(conf).run()
    print(conf.solver_name)


if __name__ == "__main__":
    
    main(1,'greedy', 'normal')
    
    #for i in range(2):
    #    main(i+1,"greedy")
    #    main((i+1)*2,"hamilton")
    
    
    #provare a usare DQNsolver, che dovrebbe usare machine learning per apprendere come giocare
    