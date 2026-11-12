from __future__ import annotations

from dataclasses import dataclass, field

from tictactoe.common.constants import SIZE, WIN_LINES, CellValue


@dataclass(slots=True)
class GameField:
    matrix: list[list[CellValue]] = field(
        default_factory=lambda: [[CellValue.EMPTY] * SIZE for _ in range(SIZE)]
    )

    def copy(self) -> GameField:
        return GameField([row[:] for row in self.matrix])

    def free_cells(self) -> list[tuple[int, int]]:
        return [
            (row, col)
            for row in range(SIZE)
            for col in range(SIZE)
            if self.matrix[row][col] == CellValue.EMPTY
        ]

    def winners(self) -> set[CellValue]:
        result: set[CellValue] = set()
        for (row1, col1), (row2, col2), (row3, col3) in WIN_LINES:
            candidate = self.matrix[row1][col1]
            if (
                candidate != CellValue.EMPTY
                and candidate == self.matrix[row2][col2] == self.matrix[row3][col3]
            ):
                result.add(candidate)
        return result

    def winner(self) -> CellValue | None:
        winners = self.winners()
        return next(iter(winners)) if winners else None

    def is_full(self) -> bool:
        return all(
            self.matrix[row][col] != CellValue.EMPTY
            for row in range(SIZE)
            for col in range(SIZE)
        )

    def count(self, mark: CellValue) -> int:
        return sum(row.count(mark) for row in self.matrix)
