from dataclasses import dataclass

from tictactoe.web.model.game_field import GameFieldModel


@dataclass(slots=True)
class CurrentGameModel:
    id: str | None
    field: GameFieldModel
    winner: int | None = None
    is_over: bool = False
