from dataclasses import dataclass, field

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
SIZE = 3

WIN_LINES = [
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
]


@dataclass(slots=True)
class GameField:
    matrix: list[list[int]] = field(
        default_factory=lambda: [[EMPTY] * SIZE for _ in range(SIZE)]
    )

    def copy(self) -> "GameField":
        return GameField([row[:] for row in self.matrix])

    def is_empty_cell(self, row: int, col: int) -> bool:
        return self.matrix[row][col] == EMPTY

    def free_cells(self) -> list[tuple[int, int]]:
        return [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if self.matrix[r][c] == EMPTY
        ]

    def winner(self) -> int | None:
        for (r1, c1), (r2, c2), (r3, c3) in WIN_LINES:
            v = self.matrix[r1][c1]
            if v != EMPTY and v == self.matrix[r2][c2] == self.matrix[r3][c3]:
                return v
        return None

    def is_full(self) -> bool:
        return all(self.matrix[r][c] != EMPTY for r in range(SIZE) for c in range(SIZE))

    def count(self, mark: int) -> int:
        return sum(row.count(mark) for row in self.matrix)
