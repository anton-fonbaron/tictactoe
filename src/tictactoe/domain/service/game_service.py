"""Реализация сервиса бизнес-логики, принимающая репозиторий через конструктор."""

from uuid import UUID, uuid4

from tictactoe.datasource.repository.game_repository_interface import GameRepositoryInterface
from tictactoe.domain.model.current_game import CurrentGame
from tictactoe.domain.model.game_field import (
    GameField,
    PLAYER_X,
    PLAYER_O,
    SIZE,
    EMPTY,
)
from tictactoe.domain.service.game_service_interface import GameServiceInterface
from tictactoe.domain.service.minimax import find_best_move

class GameService(GameServiceInterface):
    """Сервис крестиков-ноликов поверх репозитория текущих игр.

    Человек играет за X, компьютер - за O (алгоритм Минимакс).
    """

    def __init__(self, repository: GameRepositoryInterface) -> None:
        self._repository = repository

    def create_game(self) -> CurrentGame:
        """Создаёт новую игру и сохраняет её в репозитории."""
        game = CurrentGame(id=uuid4(), field=GameField())
        self._repository.save(game)
        return game

    def get_game(self, game_id: UUID) -> CurrentGame | None:
        return self._repository.get(game_id)

    def make_move_and_get_answer(self, game_id: UUID, incoming: CurrentGame) -> CurrentGame:
        """Обрабатывает ход пользователя: валидация, сохранение, ответ компьютера.

        Возвращает игру с добавленным ходом компьютера (если игра ещё не окончена).
        Бросает ValueError с описанием, если передана некорректная игра.
        """
        stored = self._repository.get(game_id)
        if stored is None:
            raise ValueError(f"Игра с идентификатором {game_id} не найдена.")

        incoming.id = game_id
        self.validate_field(incoming, previous=stored.field)
        self._repository.save(incoming)

        if self.is_game_over(incoming):
            return incoming

        return self.get_next_move(incoming)

    def get_next_move(self, game: CurrentGame) -> CurrentGame:
        """Ход компьютера по алгоритму Минимакс; сохраняет результат в репозитории."""
        result = game.copy() if hasattr(game, "copy") else CurrentGame(id=game.id, field=game.field.copy())
        move = find_best_move(result.field, ai_player=PLAYER_O)
        if move is not None:
            row, col = move
            result.field.matrix[row][col] = PLAYER_O
        self._repository.save(result)
        return result

    def validate_field(self, game: CurrentGame, previous: GameField | None = None) -> None:
        """Валидация игрового поля: структура, счётчики меток, очередность ходов,
        неизменность предыдущих ходов (поле previous), запрет победы у обоих игроков.
        """
        matrix = game.field.matrix

        if len(matrix) != SIZE or any(len(row) != SIZE for row in matrix):
            raise ValueError("Игровое поле должно быть матрицей 3x3.")
        for row in matrix:
            for value in row:
                if value not in (EMPTY, PLAYER_X, PLAYER_O):
                    raise ValueError(
                        f"Недопустимое значение клетки: {value}. "
                        f"Допустимы 0 (пусто), 1 (X), 2 (O)."
                    )

        count_x = game.field.count(PLAYER_X)
        count_o = game.field.count(PLAYER_O)

        if count_x not in (count_o, count_o + 1):
            raise ValueError(
                f"Некорректное количество меток: X - {count_x}, O - {count_o}. "
                "X ходит первым, разница может быть не больше одного хода."
            )

        winner_x = self._has_win_for(game.field, PLAYER_X)
        winner_o = self._has_win_for(game.field, PLAYER_O)

        if winner_x and winner_o:
            raise ValueError("На поле одновременно два победителя - такого быть не может.")

        if previous is not None:
            changed: list[tuple[int, int]] = []
            added: list[tuple[int, int]] = []
            for r in range(SIZE):
                for c in range(SIZE):
                    old, new = previous.matrix[r][c], matrix[r][c]
                    if old == new:
                        continue
                    if old == EMPTY:
                        added.append((r, c))
                    else:
                        changed.append((r, c))
            if changed:
                raise ValueError(
                    f"Изменены предыдущие ходы: клетки {changed}. Это запрещено."
                )
            if len(added) > 1:
                raise ValueError(
                    f"За один запрос можно добавить ровно один ход, добавлено: {len(added)}."
                )
            if self._has_win_for(previous, PLAYER_X) or self._has_win_for(previous, PLAYER_O):
                raise ValueError("Игра уже окончена: продолжать ходы нельзя.")
            if added:
                r, c = added[0]
                if matrix[r][c] != PLAYER_X:
                    raise ValueError(
                        "Пользователь играет за X (1): новый ход должен ставить метку 1."
                    )

        if winner_x and count_x != count_o + 1:
            raise ValueError("Победа X невозможна при текущем количестве меток.")
        if winner_o and count_x != count_o:
            raise ValueError("Победа O невозможна при текущем количестве меток.")

    def is_game_over(self, game: CurrentGame) -> bool:
        """Игра окончена, если есть победитель или поле заполнено."""
        return game.field.winner() is not None or game.field.is_full()

    @staticmethod
    def _has_win_for(field: GameField, mark: int) -> bool:
        return field.winner() == mark
