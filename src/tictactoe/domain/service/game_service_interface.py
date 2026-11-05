"""Интерфейс сервиса бизнес-логики крестиков-ноликов."""

from abc import ABC, abstractmethod

from tictactoe.domain.model.current_game import CurrentGame
from tictactoe.domain.model.game_field import GameField

class GameServiceInterface(ABC):
    """Сервис: следующий ход (Минимакс), валидация поля, проверка окончания игры."""

    @abstractmethod
    def get_next_move(self, game: CurrentGame) -> CurrentGame:
        """Возвращает копию игры с обновлённым полем после хода компьютера (алгоритм Минимакс)."""
        raise NotImplementedError

    @abstractmethod
    def validate_field(self, game: CurrentGame, previous: GameField | None = None) -> None:
        """Проверяет корректность игрового поля (предыдущие ходы не изменены).

        Бросает ValueError с описанием ошибки, если поле некорректно.
        """
        raise NotImplementedError

    @abstractmethod
    def is_game_over(self, game: CurrentGame) -> bool:
        """Проверяет окончание игры (есть победитель либо поле заполнено)."""
        raise NotImplementedError
