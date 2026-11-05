"""Web-модель игрового поля (DTO для обмена с клиентом)."""

from dataclasses import dataclass

@dataclass
class GameFieldModel:
    """Игровое поле в виде JSON-совместимой матрицы 3x3."""

    matrix: list[list[int]]

    @staticmethod
    def empty() -> "GameFieldModel":
        return GameFieldModel(matrix=[[0] * 3 for _ in range(3)])
