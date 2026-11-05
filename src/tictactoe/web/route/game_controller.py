"""Контроллер Flask: маршруты API крестиков-ноликов."""

from uuid import UUID

from flask import Blueprint, jsonify, request

from tictactoe.domain.service.game_service_interface import GameServiceInterface
from tictactoe.web.mapper.game_mappers import domain_game_to_web, web_field_to_domain
from tictactoe.web.module.serializers import game_dict_to_model, game_model_to_dict


class GameController:
    """Контроллер, реализующий эндпоинты игры поверх GameServiceInterface."""

    def __init__(self, service: GameServiceInterface) -> None:
        self._service = service
        self.blueprint = Blueprint("game", __name__)
        self._register_routes()

    def _register_routes(self) -> None:
        self.blueprint.add_url_rule(
            "/game", "create_game", self.create_game, methods=["POST"]
        )
        self.blueprint.add_url_rule(
            "/game/<uuid_str>", "make_move", self.make_move, methods=["POST"]
        )

    def create_game(self):
        game = self._service.create_game()
        model = domain_game_to_web(game)
        return jsonify(game_model_to_dict(model)), 201

    def make_move(self, uuid_str: str):
        try:
            game_id = UUID(uuid_str)
        except ValueError:
            return self._error(f"Некорректный UUID игры: '{uuid_str}'.", 400)

        payload = request.get_json(silent=True)
        if payload is None:
            return self._error("Ожидается корректное JSON-тело запроса.", 400)

        try:
            model = game_dict_to_model(payload)
            incoming_field = web_field_to_domain(model.field)
            result = self._service.make_move_and_get_answer(game_id, incoming_field)
        except ValueError as exc:
            return self._error(str(exc), 400)

        return jsonify(game_model_to_dict(domain_game_to_web(result))), 200

    @staticmethod
    def _error(description: str, code: int):
        return jsonify({"error": description}), code
