"""DI-слой: контейнер зависимостей (граф зависимостей приложения)."""

from tictactoe.datasource.game_storage import GameStorage
from tictactoe.datasource.repository.game_repository import GameRepository
from tictactoe.datasource.repository.game_repository_interface import GameRepositoryInterface
from tictactoe.domain.service.game_service import GameService
from tictactoe.domain.service.game_service_interface import GameServiceInterface


class Container:
    """Контейнер зависимостей.

    Граф зависимостей:
        GameStorage (singleton) <- GameRepository <- GameService
    """

    def __init__(self) -> None:
        # Класс-хранилище — singleton: единственный экземпляр на контейнер.
        self._game_storage = GameStorage()

    @property
    def game_storage(self) -> GameStorage:
        return self._game_storage

    @property
    def game_repository(self) -> GameRepositoryInterface:
        return GameRepository(storage=self._game_storage)

    @property
    def game_service(self) -> GameServiceInterface:
        return GameService(repository=self.game_repository)
