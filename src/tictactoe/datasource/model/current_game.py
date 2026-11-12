from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from tictactoe.datasource.model.game_field import GameFieldEntity


@dataclass(slots=True)
class CurrentGameEntity:
    id: UUID
    field: GameFieldEntity

    def copy(self) -> CurrentGameEntity:
        return CurrentGameEntity(id=self.id, field=self.field.copy())
