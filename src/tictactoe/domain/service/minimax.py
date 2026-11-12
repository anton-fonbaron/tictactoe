from tictactoe.domain.model.game_field import EMPTY, PLAYER_O, PLAYER_X, GameField

SIZE = 3


def minimax(field: GameField, player: int, ai_player: int, depth: int) -> int:
    winner = field.winner()
    max_score = (SIZE * SIZE) + 1

    if winner == ai_player:
        return max_score - depth
    if winner is not None:
        return depth - max_score

    if field.is_full():
        return 0

    if player == ai_player:
        value = float("-inf")
        for row, col in field.free_cells():
            field.matrix[row][col] = player
            next_player = PLAYER_X if player == PLAYER_O else PLAYER_O
            value = max(value, minimax(field, next_player, ai_player, depth + 1))
            field.matrix[row][col] = EMPTY
        return value

    else:
        value = float("inf")
        for row, col in field.free_cells():
            field.matrix[row][col] = player
            next_player = PLAYER_X if player == PLAYER_O else PLAYER_O
            value = min(value, minimax(field, next_player, ai_player, depth + 1))
            field.matrix[row][col] = EMPTY
        return value


def find_best_move(
    field: GameField, ai_player: int = PLAYER_O
) -> tuple[int, int] | None:
    best_score = float("-inf")
    best_move: tuple[int, int] | None = None

    for row, col in field.free_cells():
        field.matrix[row][col] = ai_player
        next_player = PLAYER_X if ai_player == PLAYER_O else PLAYER_O

        score = minimax(field, next_player, ai_player, depth=1)

        field.matrix[row][col] = EMPTY

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move
