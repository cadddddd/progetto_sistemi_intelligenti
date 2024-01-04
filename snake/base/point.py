from enum import Enum, unique


@unique
class PointType(Enum):
    """Tipi di punti sulla mappa."""
    EMPTY = 0
    WALL = 1
    FOOD = 2
    OBSTRUCLE = 3
    HEAD_L = 100
    HEAD_U = 101
    HEAD_R = 102
    HEAD_D = 103
    BODY_LU = 104
    BODY_UR = 105
    BODY_RD = 106
    BODY_DL = 107
    BODY_HOR = 108
    BODY_VER = 109


class Point:
    
    def __init__(self):
        self._type = PointType.EMPTY

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val
