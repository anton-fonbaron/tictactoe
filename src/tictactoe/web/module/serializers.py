from tictactoe.web.model.current_game import CurrentGameModel
from tictactoe.web.model.game_field import GameFieldModel


def game_model_to_dict(model: CurrentGameModel) -> dict:
    return {
        "id": model.id,
        "field": {"matrix": model.field.matrix},
        "winner": model.winner,
        "isOver": model.is_over,
    }


def game_dict_to_model(data: dict) -> CurrentGameModel:
    if not isinstance(data, dict):
        raise ValueError("Тело запроса должно быть JSON-объектом.")  # noqa: TRY004
    field_data = data.get("field")
    if not isinstance(field_data, dict):
        raise ValueError("Поле 'field' обязательно и должно быть объектом.")  # noqa: TRY004
    matrix = field_data.get("matrix")
    if not isinstance(matrix, list):
        raise ValueError("Поле 'field.matrix' обязательно и должно быть списком.")  # noqa: TRY004
    game_id = data.get("id")
    return CurrentGameModel(
        id=str(game_id) if game_id is not None else None,
        field=GameFieldModel(matrix=matrix),
    )
