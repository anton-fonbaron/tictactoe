"""Datasource-модель игрового поля (модель хранения)."""

from dataclasses import dataclass, field

SIZE = 3

@dataclass
class GameFieldEntity:
    """Игровое поле в виде целочисленной матрицы 3x3 для слоя хранения."""

    matrix: list[list[int]] = field(default_factory=lambda: [[0] * SIZE for _ in range(SIZE)])

    def copy(self) -> "GameFieldEntity":
        return GameFieldEntity([row[:] for row in self.matrix])
