from flask import Flask

from tictactoe.di.container import Container
from tictactoe.web.route.game_controller import GameController


def create_app(container: Container | None = None) -> Flask:
    if container is None:
        container = Container()

    app = Flask(__name__)

    controller = GameController(service=container.game_service)
    app.register_blueprint(controller.blueprint)

    @app.get("/")
    def index():
        return (
            "Tic-Tac-Toe API. <br />"
            "POST /game - создать игру; <br />"
            "POST /game/<UUID> - сделать ход."
        )

    return app


def run_app():
    create_app().run(debug=True)


if __name__ == "__main__":
    run_app()
