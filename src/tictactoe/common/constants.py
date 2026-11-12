from enum import IntEnum


class CellValue(IntEnum):
    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2


SIZE = 3

WIN_LINES = [
    # строки
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    # столбцы
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    # диагонали
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
]

EMPTY = CellValue.EMPTY
PLAYER_X = CellValue.PLAYER_X
PLAYER_O = CellValue.PLAYER_O
