from abc import ABC, abstractmethod
from uuid import UUID

from tictactoe.domain.model.current_game import CurrentGame


class GameRepositoryInterface(ABC):
    @abstractmethod
    def save(self, game: CurrentGame) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, game_id: UUID) -> CurrentGame | None:
        raise NotImplementedError
