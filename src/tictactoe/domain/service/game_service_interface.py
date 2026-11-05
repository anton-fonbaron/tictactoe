from abc import ABC, abstractmethod
from uuid import UUID

from tictactoe.domain.model.current_game import CurrentGame
from tictactoe.domain.model.game_field import GameField


class GameServiceInterface(ABC):
    @abstractmethod
    def create_game(self) -> CurrentGame:
        raise NotImplementedError

    @abstractmethod
    def get_game(self, game_id: UUID) -> CurrentGame | None:
        raise NotImplementedError

    @abstractmethod
    def make_move_and_get_answer(
        self, game_id: UUID, incoming: CurrentGame
    ) -> CurrentGame:
        raise NotImplementedError

    @abstractmethod
    def get_next_move(self, game: CurrentGame) -> CurrentGame:
        raise NotImplementedError

    @abstractmethod
    def validate_field(
        self, game: CurrentGame, previous: GameField | None = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_game_over(self, game: CurrentGame) -> bool:
        raise NotImplementedError
