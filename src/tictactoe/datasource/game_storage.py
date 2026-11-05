"""Класс-хранилище текущих игр на потокобезопасных коллекциях."""

import threading
from uuid import UUID

from tictactoe.datasource.model.current_game import CurrentGameEntity


class GameStorage:
    """Потокобезопасное хранилище текущих игр (словарь UUID -> сущность игры)."""

    def __init__(self) -> None:
        # Потокобезопасность обеспечивается замком: стандартный dict
        # не является потокобезопасным при записи, поэтому все операции
        # чтения/записи выполняются под lock.
        self._games: dict[UUID, CurrentGameEntity] = {}
        self._lock = threading.RLock()

    def save(self, game: CurrentGameEntity) -> None:
        with self._lock:
            self._games[game.id] = game

    def get(self, game_id: UUID) -> CurrentGameEntity | None:
        with self._lock:
            game = self._games.get(game_id)
            if game is None:
                return None
            # Возвращаем копию, чтобы внешние изменения не ломали хранилище.
            return CurrentGameEntity(id=game.id, field=game.field.copy())

    def remove(self, game_id: UUID) -> None:
        with self._lock:
            self._games.pop(game_id, None)

    def count(self) -> int:
        with self._lock:
            return len(self._games)
