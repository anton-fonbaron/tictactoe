"""Модуль сериализации web-моделей в JSON и обратно."""

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
    """Парсит JSON-тело запроса в web-модель. Бросает ValueError с описанием."""
    if not isinstance(data, dict):
        raise ValueError("Тело запроса должно быть JSON-объектом.")
    game_id = data.get("id")
    if not game_id:
        raise ValueError("Поле 'id' обязательно.")
    field_data = data.get("field")
    if not isinstance(field_data, dict):
        raise ValueError("Поле 'field' обязательно и должно быть объектом.")
    matrix = field_data.get("matrix")
    if not isinstance(matrix, list):
        raise ValueError("Поле 'field.matrix' обязательно и должно быть списком.")
    return CurrentGameModel(id=str(game_id), field=GameFieldModel(matrix=matrix))
