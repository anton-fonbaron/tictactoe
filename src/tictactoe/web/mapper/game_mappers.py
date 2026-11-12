from tictactoe.common.constants import CellValue
from tictactoe.domain.model.current_game import CurrentGame
from tictactoe.domain.model.game_field import GameField
from tictactoe.web.model.current_game import CurrentGameModel
from tictactoe.web.model.game_field import GameFieldModel


def web_field_to_domain(model: GameFieldModel) -> GameField:
    return GameField(
        matrix=[[CellValue(value) for value in row] for row in model.matrix]
    )


def domain_field_to_web(field: GameField) -> GameFieldModel:
    return GameFieldModel(
        matrix=[[int(value) for value in row] for row in field.matrix]
    )


def domain_game_to_web(
    game: CurrentGame, is_over: bool | None = None
) -> CurrentGameModel:
    winner = game.field.winner()
    if is_over is None:
        is_over = winner is not None or game.field.is_full()
    return CurrentGameModel(
        id=str(game.id),
        field=domain_field_to_web(game.field),
        winner=int(winner) if winner is not None else None,
        is_over=is_over,
    )
