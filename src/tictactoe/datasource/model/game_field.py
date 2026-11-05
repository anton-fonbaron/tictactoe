from dataclasses import dataclass, field

SIZE = 3


@dataclass(slots=True)
class GameFieldEntity:
    matrix: list[list[int]] = field(
        default_factory=lambda: [[0] * SIZE for _ in range(SIZE)]
    )

    def copy(self) -> "GameFieldEntity":
        return GameFieldEntity([row[:] for row in self.matrix])
