"""Реализация репозитория поверх класса-хранилища GameStorage."""

from uuid import UUID

from tictactoe.datasource.game_storage import GameStorage
from tictactoe.datasource.mapper.game_mappers import (
    domain_game_to_entity,
    entity_to_domain_game,
)
from tictactoe.datasource.repository.game_repository_interface import GameRepositoryInterface
from tictactoe.domain.model.current_game import CurrentGame


class GameRepository(GameRepositoryInterface):
    """Репозиторий текущих игр, работающий с потокобезопасным хранилищем."""

    def __init__(self, storage: GameStorage) -> None:
        self._storage = storage

    def save(self, game: CurrentGame) -> None:
        self._storage.save(domain_game_to_entity(game))

    def get(self, game_id: UUID) -> CurrentGame | None:
        entity = self._storage.get(game_id)
        if entity is None:
            return None
        return entity_to_domain_game(entity)
