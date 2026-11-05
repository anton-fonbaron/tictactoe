from dataclasses import dataclass


@dataclass(slots=True)
class GameFieldModel:
    matrix: list[list[int]]

    @staticmethod
    def empty() -> "GameFieldModel":
        return GameFieldModel(matrix=[[0] * 3 for _ in range(3)])
