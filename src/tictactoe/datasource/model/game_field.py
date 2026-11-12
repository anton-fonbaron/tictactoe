from __future__ import annotations

from dataclasses import dataclass, field

from tictactoe.common.constants import SIZE, CellValue


@dataclass(slots=True)
class GameFieldEntity:
    matrix: list[list[CellValue]] = field(
        default_factory=lambda: [[CellValue.EMPTY] * SIZE for _ in range(SIZE)]
    )

    def copy(self) -> GameFieldEntity:
        return GameFieldEntity([row[:] for row in self.matrix])
