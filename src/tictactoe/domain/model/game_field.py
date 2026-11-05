
from dataclasses import dataclass

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
SIZE = 3


@dataclass
class GameField:
    