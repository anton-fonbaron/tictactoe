from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from tictactoe.domain.model.game_field import CellValue, GameField


@dataclass(slots=True)
class CurrentGame:
    """Текущая игра: идентификатор (UUID) и игровое поле.

    Человек играет за X, компьютер - за O. X ходит первым.
    """

    id: UUID
    field: GameField

    def copy(self) -> CurrentGame:
        return CurrentGame(id=self.id, field=self.field.copy())

    @property
    def current_mark(self) -> CellValue:
        """Чей ход должен быть сейчас (X при равенстве меток, иначе O)."""
        return (
            CellValue.PLAYER_X
            if self.field.count(CellValue.PLAYER_X)
            == self.field.count(CellValue.PLAYER_O)
            else CellValue.PLAYER_O
        )
