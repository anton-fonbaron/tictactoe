"""Реализация сервиса бизнес-логики, принимающая репозиторий через конструктор."""

from uuid import UUID, uuid4

from tictactoe.domain.model.current_game import CurrentGame
from tictactoe.domain.model.game_field import (
    EMPTY,
    PLAYER_O,
    PLAYER_X,
    SIZE,
    GameField,
)
from tictactoe.domain.repository.game_repository_interface import (
    GameRepositoryInterface,
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
        game = CurrentGame(id=uuid4(), field=GameField())
        self._repository.save(game)
        return game

    def get_game(self, game_id: UUID) -> CurrentGame | None:
        return self._repository.get(game_id)

    def make_move_and_get_answer(
        self, game_id: UUID, incoming_field: GameField
    ) -> CurrentGame:
        stored = self._repository.get(game_id)
        if stored is None:
            raise ValueError(f"Игра с идентификатором {game_id} не найдена.")

        self.validate_field(incoming_field, previous=stored.field)

        game = CurrentGame(id=game_id, field=incoming_field)
        self._repository.save(game)

        if self.is_game_over(game):
            return game

        return self.get_next_move(game)

    def get_next_move(self, game: CurrentGame) -> CurrentGame:
        result = game.copy()
        move = find_best_move(result.field, ai_player=PLAYER_O)
        if move is not None:
            row, col = move
            result.field.matrix[row][col] = PLAYER_O
        self._repository.save(result)
        return result

    def validate_field(
        self, field: GameField, previous: GameField | None = None
    ) -> None:
        matrix = field.matrix

        if len(matrix) != SIZE or any(len(row) != SIZE for row in matrix):
            raise ValueError("Игровое поле должно быть матрицей 3x3.")
        for row in matrix:
            for value in row:
                if value not in (EMPTY, PLAYER_X, PLAYER_O):
                    raise ValueError(
                        f"Недопустимое значение клетки: {value}. "
                        f"Допустимы 0 (пусто), 1 (X), 2 (O)."
                    )

        count_x = field.count(PLAYER_X)
        count_o = field.count(PLAYER_O)

        if count_x not in (count_o, count_o + 1):
            raise ValueError(
                f"Некорректное количество меток: X - {count_x}, O - {count_o}. "
                "X ходит первым, разница может быть не больше одного хода."
            )

        winners = field.winners()
        if len(winners) > 1:
            raise ValueError(
                "На поле одновременно два победителя - такого быть не может."
            )
        winner_x = PLAYER_X in winners
        winner_o = PLAYER_O in winners

        if previous is not None:
            if previous.winners():
                raise ValueError("Игра уже окончена: продолжать ходы нельзя.")

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
            if len(added) != 1:
                raise ValueError(
                    f"За один запрос нужно добавить ровно один ход, добавлено: {len(added)}."
                )
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
        return game.field.winner() is not None or game.field.is_full()
