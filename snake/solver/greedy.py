from snake.base.pos import Pos
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class GreedySolver(BaseSolver):

    def __init__(self, snake):
        super().__init__(snake)
        self._path_solver = PathSolver(snake)

    def next_direc(self):
        
        s_copy, m_copy = self.snake.copy()

        # Viene creata una copia del serpente e della mappa e viene calcolato il percorso più breve alla posizione del cibo
        self._path_solver.snake = self.snake
        path_to_food = self._path_solver.shortest_path_to_food()

        if path_to_food:
            #Se esiste un percorso al cibo, la copia del serpente viene mosso lungo il percorso. Se la mappa è piena il solver ritorna la prima direzione del percorso.
            s_copy.move_path(path_to_food)
            if m_copy.is_full():
                return path_to_food[0]

            #  Se la mappa non è piena, con il serpente copiato  viene calcolato il percorso più lungo fino alla coda.
            self._path_solver.snake = s_copy
            path_to_tail = self._path_solver.longest_path_to_tail()
            if len(path_to_tail) > 1:
                return path_to_food[0]

        # fa la stessa cosa con il serpente reale
        self._path_solver.snake = self.snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) > 1:
            return path_to_tail[0]

        # viene eseguita una scansione delle direzioni adiacenti alla testa del serpente. Per ogni direzione adiacente sicura (non colpisci i bordi o il tuo corpo), viene calcolata la distanza di Chebyshev dalla posizione attuale del cibo. La direzione corrispondente alla minima distanza viene restituita come prossima direzione per il movimento del serpente.
        head = self.snake.head()
        direc, min_dist = self.snake.direc, -1
        for adj in head.all_adj():
            if self.map.is_safe(adj):
                dist = Pos.chebyshev_dist(adj, self.map.food)
                #dist = Pos.manhattan_dist(adj, self.map.food)
                if dist < min_dist:
                    min_dist = dist
                    direc = head.direc_to(adj)
        return direc