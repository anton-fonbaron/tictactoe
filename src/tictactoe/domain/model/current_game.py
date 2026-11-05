"""Доменная модель текущей игры."""

from dataclasses import dataclass
from uuid import UUID

from tictactoe.domain.model.game_field import PLAYER_O, PLAYER_X, GameField


@dataclass(slots=True)
class CurrentGame:
    """Текущая игра: идентификатор (UUID) и игровое поле.

    Человек играет за X, компьютер - за O. X ходит первым.
    """

    id: UUID
    field: GameField

    def copy(self) -> "CurrentGame":
        return CurrentGame(id=self.id, field=self.field.copy())

    @property
    def current_mark(self) -> int:
        """Чей ход должен быть сейчас (X при равенстве меток, иначе O)."""
        return (
            PLAYER_X
            if self.field.count(PLAYER_X) == self.field.count(PLAYER_O)
            else PLAYER_O
        )
