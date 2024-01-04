import random

from snake.base.point import Point, PointType
from snake.base.pos import Pos


class Map:
    """mappa di gioco."""

    def __init__(self, num_rows, num_cols):
        """Inizializza."""
        if not isinstance(num_rows, int) or not isinstance(num_cols, int):
            raise TypeError("\'numero di righe\' e \'colonne\' meglio se un intero")
        if num_rows < 5 or num_cols < 5:
            raise ValueError("\'numero di righe\' e \'colonne\' meglio >= 5")

        self._num_rows = num_rows
        self._num_cols = num_cols
        self._capacity = (num_rows - 2) * (num_cols - 2)
        self._content = [[Point() for _ in range(num_cols)] for _ in range(num_rows)]
        self.reset()

    def reset(self):
        self._food = None
        self._obstrucle = None
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                if i == 0 or i == self._num_rows - 1 or \
                   j == 0 or j == self._num_cols - 1:
                    self._content[i][j].type = PointType.WALL
                else:
                    self._content[i][j].type = PointType.EMPTY

    def copy(self):
        m_copy = Map(self._num_rows, self._num_cols)
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                m_copy._content[i][j].type = self._content[i][j].type
        return m_copy

    @property
    def num_rows(self):
        return self._num_rows

    
    

    @property
    def num_cols(self):
        return self._num_cols

    @property
    def capacity(self):
        return self._capacity

    @property
    def food(self):
        return self._food

    def point(self, pos):
       
        return self._content[pos.x][pos.y]

    def is_inside(self, pos):
        return pos.x > 0 and pos.x < self.num_rows - 1 \
            and pos.y > 0 and pos.y < self.num_cols - 1

    def is_empty(self, pos):
        return self.is_inside(pos) and self.point(pos).type == PointType.EMPTY

    def is_safe(self, pos):
        return self.is_inside(pos) and (self.point(pos).type == PointType.EMPTY
                                        or self.point(pos).type == PointType.FOOD)

    def is_full(self):
        """visualizza se la mappa è occupata da tutto il corpo ."""
        for i in range(1, self.num_rows - 1):
            for j in range(1, self.num_cols - 1):
                t = self._content[i][j].type
                if t.value < PointType.HEAD_L.value:
                    return False
        return True

    def has_food(self):
        return self._food is not None
    
    def has_obstrucle(self):
        return self._obstrucle is not None

    def rm_food(self):
        if self.has_food():
            self.point(self._food).type = PointType.EMPTY
            self._food = None

    def create_food(self, pos):
        self.point(pos).type = PointType.FOOD
        self._food = pos
        return self._food
    
    def create_obstrucle(self, pos):
        self.point(pos).type = PointType.OBSTRUCLE
        self._obstrucle = pos
        return self._obstrucle

    def create_rand_food(self):
        empty_pos = []
        for i in range(1, self._num_rows - 1):
            for j in range(1, self._num_cols - 1):
                t = self._content[i][j].type
                if t == PointType.EMPTY:
                    empty_pos.append(Pos(i, j))
                elif t == PointType.FOOD:
                    return None  # fermo se il cibo esiste
        if empty_pos:
            return self.create_food(random.choice(empty_pos))
        return None
    
    def create_rand_obstrucle(self,obsta):
        empty_pos = []
        obstrucles = []
        for i in range(1, self._num_rows - 1):
            for j in range(1, self._num_cols - 1):
                t = self._content[i][j].type
                if t == PointType.EMPTY:
                    empty_pos.append(Pos(i, j))
                elif t == PointType.OBSTRUCLE:
                    return None  # fermo se il cibo esiste
        if empty_pos:
            for _ in range(obsta):
                obstrucles.append(self.create_obstrucle(random.choice(empty_pos)))
            return obstrucles
        return None
