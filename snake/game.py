import errno
import os
import traceback
from enum import Enum, unique

from snake.base import Direc, Map, PointType, Pos, Snake
from snake.gui import GameWindow

# Add solver names to globals()
from snake.solver import GreedySolver


@unique
class GameMode(Enum):
    NORMAL = 0         
    BENCHMARK = 1      
   


class GameConf:

    def __init__(self,num_rows,solver):
        

        # Game mode
        self.mode = GameMode.NORMAL

        # solver scelto
        self.solver_name = solver  

        # mappa
        self.map_rows = num_rows
        self.map_cols = self.map_rows
        self.map_width = 800  
        self.map_height = self.map_width
        self.info_panel_width = 200  
        self.window_width = self.map_width + self.info_panel_width
        self.window_height = self.map_height
        self.grid_pad_ratio = 0.125

        
        self.show_grid_line = False
        self.show_info_panel = True

        # ritardo
        self.interval_draw = 25       # ms
        self.interval_draw_max = 50  # ms

        # Codici colori
        self.color_bg = '#000000'
        self.color_txt = '#F5F5F5'
        self.color_line = '#424242'
        self.color_wall = '#F5F5F5'
        self.color_food = '#7CFC00'
        self.color_head = '#0000FF'
        self.color_body = '#F5F5F5'
        self.color_obstrucle = '#d00002'

        # snake
        self.init_direc = Direc.RIGHT
        self.init_bodies = [Pos(1, 4), Pos(1, 3), Pos(1, 2), Pos(1, 1)]
        self.init_types = [PointType.HEAD_R] + [PointType.BODY_HOR] * 3

        # Font
        self.font_info = ('Arial', 9)

        # Info
        self.info_status = ['eating', 'dead', 'full'] 


class Game:

    def __init__(self, conf):
        self._conf = conf
        self._map = Map(conf.map_rows + 2, conf.map_cols + 2)
        self._snake = Snake(self._map, conf.init_direc,
                            conf.init_bodies, conf.init_types)
        self._pause = False
        self._solver = globals()[self._conf.solver_name](self._snake)
        self._episode = 1
        self._init_log_file()

    @property
    def snake(self):
        return self._snake

    @property
    def episode(self):
        return self._episode

    def run(self):
        if self._conf.mode == GameMode.BENCHMARK:
            self._run_benchmarks()
      
        else:
            window = GameWindow("Snake", self._conf, self._map, self, self._on_exit, (
                ('<r>', lambda e: self._reset()),
                ('<space>', lambda e: self._toggle_pause()),
                
                
            ))
            if self._conf.mode == GameMode.NORMAL:
                window.show(self._game_main_normal)
           

    def _run_benchmarks(self):
        steps_limit = 100000 #numero massimo di passi
        num_episodes = int(input("inserisci il numero di episodi: "))

        print(f"\nMap size: {self._conf.map_rows}x{self._conf.map_cols}")
        print(f"Solver: {self._conf.solver_name[:-6].lower()}\n")

        tot_len, tot_steps = 0, 0

        for _ in range(num_episodes):
            print(f"Episode {self._episode} - ", end="")
            while True:
                self._game_main_normal()
                if self._map.is_full():
                    print(f"FULL (len: {self._snake.len()} | steps: {self._snake.steps})")
                    break
                if self._snake.dead:
                    print(f"DEAD (len: {self._snake.len()} | steps: {self._snake.steps})")
                    break
                if self._snake.steps >= steps_limit:
                    print(f"STEP LIMIT (len: {self._snake.len()} | steps: {self._snake.steps})")
                    self._write_logs()  # Write the last step
                    break
            tot_len += self._snake.len()
            tot_steps += self._snake.steps
            self._reset()

        avg_len = tot_len / num_episodes
        avg_steps = tot_steps / num_episodes
        print(f"\n[Summary]\nAverage Length: {avg_len:.2f}\nAverage Steps: {avg_steps:.2f}\n")

        self._on_exit()

   
    def set_greedy_solver(self):
        self._conf.solver_name = "GreedySolver"
        self._solver = globals()[self._conf.solver_name](self._snake)
    def error_detected(self):
        print("Errore")
        
        self._on_exit()
    def _game_main_normal(self):
        if not self._map.has_food():
            self._map.create_rand_food()
          #------------------------------------------------------------------------------#  
        if not self._map.has_obstrucle():
            self._map.create_rand_obstrucle(int(self._map.num_rows*0))

        if self._pause or self._is_episode_end():
            return

        self._update_direc(self._solver.next_direc())

        if self._conf.mode == GameMode.NORMAL and self._snake.direc_next != Direc.NONE:
            self._write_logs()

        self._snake.move()

        if self._is_episode_end():
            self._write_logs()  

    def _plot_history(self):
        self._solver.plot()

    def _update_direc(self, new_direc):
        self._snake.direc_next = new_direc
        if self._pause:
            self._snake.move()

    def _toggle_pause(self):
        self._pause = not self._pause
    
    

    def _is_episode_end(self):
        return self._snake.dead or self._map.is_full()

    def _reset(self):
        self._snake.reset()
        self._episode += 1

    def _on_exit(self):
        if self._log_file:
            self._log_file.close()
        if self._solver:
            self._solver.close()

        
    def _init_log_file(self):
        try:
            os.makedirs("logs")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            self._log_file = None
            self._log_file = open("logs/snake.log", "w", encoding="utf-8")
        except FileNotFoundError:
            if self._log_file:
                self._log_file.close()

    def _write_logs(self):
        self._log_file.write(f"[ Episode {self._episode} / Step {self._snake.steps} ]\n")
        for i in range(self._map.num_rows):
            for j in range(self._map.num_cols):
                pos = Pos(i, j)
                t = self._map.point(pos).type
                if t == PointType.EMPTY:
                    self._log_file.write("  ")
                elif t == PointType.WALL:
                    self._log_file.write("# ")
                elif t == PointType.FOOD:
                    self._log_file.write("F ")
                elif t == PointType.HEAD_L or t == PointType.HEAD_U or \
                    t == PointType.HEAD_R or t == PointType.HEAD_D:
                    self._log_file.write("H ")
                elif pos == self._snake.tail():
                    self._log_file.write("T ")
                elif t == PointType.OBSTRUCLE:
                    self._log_file.write("O ")
                else:
                    self._log_file.write("B ")
            self._log_file.write("\n")
        self._log_file.write(f"[ last/next direc: {self._snake.direc}/{self._snake.direc_next} ]\n")
        self._log_file.write("\n")
