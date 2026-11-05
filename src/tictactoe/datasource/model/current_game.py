"""Datasource-модель текущей игры (модель хранения)."""

from dataclasses import dataclass
from uuid import UUID

from tictactoe.datasource.model.game_field import GameFieldEntity

@dataclass
class CurrentGameEntity:
    """Текущая игра в слое хранения: UUID + сущность игрового поля."""

    id: UUID
    field: GameFieldEntity
