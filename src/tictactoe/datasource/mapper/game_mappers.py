"""Мапперы domain <-> datasource для игрового поля и текущей игры."""

from tictactoe.datasource.model.current_game import CurrentGameEntity
from tictactoe.datasource.model.game_field import GameFieldEntity
from tictactoe.domain.model.current_game import CurrentGame
from tictactoe.domain.model.game_field import GameField


def domain_field_to_entity(field: GameField) -> GameFieldEntity:
    return GameFieldEntity(matrix=[row[:] for row in field.matrix])


def entity_to_domain_field(entity: GameFieldEntity) -> GameField:
    return GameField(matrix=[row[:] for row in entity.matrix])


def domain_game_to_entity(game: CurrentGame) -> CurrentGameEntity:
    return CurrentGameEntity(id=game.id, field=domain_field_to_entity(game.field))


def entity_to_domain_game(entity: CurrentGameEntity) -> CurrentGame:
    return CurrentGame(id=entity.id, field=entity_to_domain_field(entity.field))
