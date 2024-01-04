from snake.base.pos import Pos
from snake.solver.base import BaseSolver
from snake.solver.path import PathSolver


class GreedySolver(BaseSolver):

    def __init__(self, snake):
        super().__init__(snake)
        self._path_solver = PathSolver(snake)

    def next_direc(self):
        
        s_copy, m_copy = self.snake.copy()

        # Viene creata una copia del serpente (s_copy) e della mappa (m_copy). Viene impostato il serpente nel PathSolver con il serpente attuale. Viene calcolato il percorso più breve alla posizione del cibo
        self._path_solver.snake = self.snake
        path_to_food = self._path_solver.shortest_path_to_food()

        if path_to_food:
            #Se esiste un percorso al cibo, la copia del serpente viene mosso lungo il percorso. Se la mappa è piena il solver ritorna la prima direzione del percorso.
            s_copy.move_path(path_to_food)
            if m_copy.is_full():
                return path_to_food[0]

            #  Se la mappa non è piena, il PathSolver è impostato con il serpente copiato e viene calcolato il percorso più lungo fino alla coda. Se il percorso ha una lunghezza maggiore di 1, il solver ritorna la prima direzione del percorso al cibo.
            self._path_solver.snake = s_copy
            path_to_tail = self._path_solver.longest_path_to_tail()
            if len(path_to_tail) > 1:
                return path_to_food[0]

        # Se non c'è un percorso al cibo, il PathSolver è reimpostato con il serpente originale e viene calcolato il percorso più lungo fino alla coda. Se il percorso ha una lunghezza maggiore di 1, il solver ritorna la prima direzione del percorso alla coda.
        self._path_solver.snake = self.snake
        path_to_tail = self._path_solver.longest_path_to_tail()
        if len(path_to_tail) > 1:
            return path_to_tail[0]

        # Se non ci sono percorsi validi al cibo o alla coda, viene eseguita una scansione delle direzioni adiacenti alla testa del serpente. Per ogni direzione adiacente sicura (non colpisci i bordi o il tuo corpo), viene calcolata la distanza di Chebyshev dalla posizione attuale del cibo. La direzione corrispondente alla massima distanza viene restituita come prossima direzione per il movimento del serpente.
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