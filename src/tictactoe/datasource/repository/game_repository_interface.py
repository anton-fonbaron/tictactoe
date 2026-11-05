"""Интерфейс репозитория текущих игр."""

from abc import ABC, abstractmethod
from uuid import UUID

from tictactoe.domain.model.current_game import CurrentGame


class GameRepositoryInterface(ABC):
    """Репозиторий для сохранения и получения текущих игр."""

    @abstractmethod
    def save(self, game: CurrentGame) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, game_id: UUID) -> CurrentGame | None:
        raise NotImplementedError
