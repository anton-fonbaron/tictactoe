from tictactoe.common.constants import SIZE, CellValue
from tictactoe.domain.model.game_field import GameField


def minimax(
    field: GameField,
    current_player: CellValue,
    ai_player: CellValue,
    depth: int,
) -> int:
    winner = field.winner()
    max_score = SIZE * SIZE + 1

    if winner == ai_player:
        return max_score - depth
    if winner is not None:
        return depth - max_score
    if field.is_full():
        return 0

    next_player = (
        CellValue.PLAYER_O
        if current_player == CellValue.PLAYER_X
        else CellValue.PLAYER_X
    )

    if current_player == ai_player:
        best_value = float("-inf")
        for row, col in field.free_cells():
            field.matrix[row][col] = current_player
            best_value = max(
                best_value, minimax(field, next_player, ai_player, depth + 1)
            )
            field.matrix[row][col] = CellValue.EMPTY
        return best_value

    best_value = float("inf")
    for row, col in field.free_cells():
        field.matrix[row][col] = current_player
        best_value = min(best_value, minimax(field, next_player, ai_player, depth + 1))
        field.matrix[row][col] = CellValue.EMPTY
    return best_value


def find_best_move(
    field: GameField, ai_player: CellValue = CellValue.PLAYER_O
) -> tuple[int, int] | None:
    best_score = float("-inf")
    best_move: tuple[int, int] | None = None

    for row, col in field.free_cells():
        field.matrix[row][col] = ai_player
        next_player = (
            CellValue.PLAYER_X
            if ai_player == CellValue.PLAYER_O
            else CellValue.PLAYER_O
        )
        score = minimax(field, next_player, ai_player, depth=1)
        field.matrix[row][col] = CellValue.EMPTY

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move
