import threading
from uuid import UUID

from tictactoe.datasource.model.current_game import CurrentGameEntity


class GameStorage:
    def __init__(self) -> None:
        self._games: dict[UUID, CurrentGameEntity] = {}
        self._lock = threading.RLock()

    def save(self, game: CurrentGameEntity) -> None:
        with self._lock:
            self._games[game.id] = game.copy()

    def get(self, game_id: UUID) -> CurrentGameEntity | None:
        with self._lock:
            game = self._games.get(game_id)
            if game is None:
                return None
            return game.copy()

    def remove(self, game_id: UUID) -> None:
        with self._lock:
            self._games.pop(game_id, None)

    def count(self) -> int:
        with self._lock:
            return len(self._games)
