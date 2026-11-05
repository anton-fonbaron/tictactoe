"""Алгоритм «Минимакс» для поиска лучшего хода в крестиках-ноликах."""

from tictactoe.domain.model.game_field import GameField, PLAYER_X, PLAYER_O, EMPTY


def minimax(field: GameField, player: int, ai_player: int) -> tuple[int, tuple[int, int] | None]:
    """Возвращает (оценку позиции, лучший ход) для игрока player.

    Оценка считается от лица ai_player: победа ai_player = +10,
    поражение = -10, ничья = 0. Глубина учитывается, чтобы побеждать быстрее.
    """
    winner = field.winner()
    if winner == ai_player:
        return 10, None
    if winner is not None:
        return -10, None
    if field.is_full():
        return 0, None

    best_move: tuple[int, int] | None = None
    if player == ai_player:  # максимизирующий игрок
        best_score = -2
    else:  # минимизирующий игрок
        best_score = 2

    for row, col in field.free_cells():
        field.matrix[row][col] = player
        score, _ = minimax(field, PLAYER_X if player == PLAYER_O else PLAYER_O, ai_player)
        field.matrix[row][col] = EMPTY

        if player == ai_player:
            if score > best_score:
                best_score, best_move = score, (row, col)
        elif score < best_score:
            best_score, best_move = score, (row, col)

    return best_score, best_move


def find_best_move(field: GameField, ai_player: int = PLAYER_O) -> tuple[int, int] | None:
    """Лучший ход для ai_player согласно алгоритму Минимакс."""
    _, move = minimax(field.copy(), ai_player, ai_player)
    return move
