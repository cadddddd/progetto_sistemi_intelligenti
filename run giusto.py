import argparse
import threading

from snake.game import Game, GameConf, GameMode


def main(prod,choosen_solver, mode):
    dict_solver = {
        "greedy": "GreedySolver"    
    }

    dict_mode = {
        "normal": GameMode.NORMAL,
        "bcmk": GameMode.BENCHMARK,
    }

    parser = argparse.ArgumentParser(description="Run snake game agent.")
    parser.add_argument("-s", default="greedy", choices=dict_solver.keys(),
                        help="algoritmo")
    parser.add_argument("-m", default=mode, choices=dict_mode.keys(),
                        help="modalità di gioco default: normal")
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
    
   
    