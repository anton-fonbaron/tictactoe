"""DI-слой: контейнер зависимостей."""

from tictactoe.datasource.game_storage import GameStorage
from tictactoe.datasource.repository.game_repository import GameRepository
from tictactoe.domain.repository.game_repository_interface import (
    GameRepositoryInterface,
)
from tictactoe.domain.service.game_service import GameService
from tictactoe.domain.service.game_service_interface import GameServiceInterface


class Container:
    """Контейнер зависимостей.

    Граф зависимостей:
        GameStorage (singleton) <- GameRepository <- GameService
    """

    def __init__(self) -> None:
        self._game_storage = GameStorage()
        self._game_repository = GameRepository(storage=self._game_storage)
        self._game_service = GameService(repository=self._game_repository)

    @property
    def game_storage(self) -> GameStorage:
        return self._game_storage

    @property
    def game_repository(self) -> GameRepositoryInterface:
        return self._game_repository

    @property
    def game_service(self) -> GameServiceInterface:
        return self._game_service
