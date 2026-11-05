"""Доменная модель текущей игры."""

from dataclasses import dataclass
from uuid import UUID

from tictactoe.domain.model.game_field import PLAYER_O, PLAYER_X, GameField


@dataclass
class CurrentGame:
    """Текущая игра: идентификатор (UUID) и игровое поле.

    Человек играет за X, компьютер - за O. X ходит первым.
    """

    id: UUID
    field: GameField

    @property
    def current_mark(self) -> int:
        """Чей ход должен быть сейчас (X при равенстве меток, иначе O)."""
        return (
            PLAYER_X
            if self.field.count(PLAYER_X) == self.field.count(PLAYER_O)
            else PLAYER_O
        )
