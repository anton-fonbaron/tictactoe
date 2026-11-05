"""Web-модель текущей игры (DTO для обмена с клиентом)."""

from dataclasses import dataclass

from tictactoe.web.model.game_field import GameFieldModel


@dataclass
class CurrentGameModel:
    """Текущая игра: строковый UUID, поле и информация о состоянии игры."""

    id: str
    field: GameFieldModel
    winner: int | None = None   # 1 — X, 2 — O, None — нет победителя
    is_over: bool = False
