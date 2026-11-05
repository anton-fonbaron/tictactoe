"""Интерфейс сервиса бизнес-логики крестиков-ноликов."""

from abc import ABC, abstractmethod
from uuid import UUID

from tictactoe.domain.model.current_game import CurrentGame
from tictactoe.domain.model.game_field import GameField


class GameServiceInterface(ABC):
    """Сервис: создание игры, следующий ход (Минимакс), валидация поля, проверка окончания."""

    @abstractmethod
    def create_game(self) -> CurrentGame:
        raise NotImplementedError

    @abstractmethod
    def get_game(self, game_id: UUID) -> CurrentGame | None:
        raise NotImplementedError

    @abstractmethod
    def make_move_and_get_answer(
        self, game_id: UUID, incoming_field: GameField
    ) -> CurrentGame:
        raise NotImplementedError

    @abstractmethod
    def get_next_move(self, game: CurrentGame) -> CurrentGame:
        raise NotImplementedError

    @abstractmethod
    def validate_field(
        self, field: GameField, previous: GameField | None = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_game_over(self, game: CurrentGame) -> bool:
        raise NotImplementedError
