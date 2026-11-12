import requests
from tictactoe.common.constants import EMPTY, PLAYER_O, PLAYER_X

BASE = "http://127.0.0.1:5000"

SYMBOL = {EMPTY: " ", PLAYER_X: "X", PLAYER_O: "O"}


def print_info():
    print("=" * 44)
    print("            КРЕСТИКИ-НОЛИКИ")
    print("=" * 44)
    print("Вы играете крестиками (X) и ходите первыми.")
    print("Компьютер играет ноликами (O) и отвечает сразу.")
    print()
    print("Обозначения на доске:")
    print(f"  {SYMBOL[EMPTY]} -  пустая клетка")
    print(f"  {SYMBOL[PLAYER_X]} -  ваш ход")
    print(f"  {SYMBOL[PLAYER_O]} -  ход компьютера")
    print()
    print("Как ходить: введите номер строки и номер столбца")
    print("через пробел. Оба числа — от 0 до 2.")
    print("Пример: '1 1' — центральная клетка, '0 2' —")
    print("правый верхний угол.")
    print()


def render(matrix):
    out = ["      0   1   2", "    +---+---+---+"]
    for row_index, row in enumerate(matrix):
        out.append(
            f"  {row_index} | " + " | ".join(SYMBOL[value] for value in row) + " |"
        )
        out.append("    +---+---+---+")
    return "\n".join(out)


def ask_move(matrix):
    size = len(matrix)
    while True:
        raw = input("Ваш ход (строка столбец): ").strip().replace(",", " ")
        parts = raw.split()
        if len(parts) != 2:
            print("  Нужно ровно два числа: строка и столбец.")
            continue
        try:
            row, column = int(parts[0]), int(parts[1])
        except ValueError:
            print("  Введите целые числа (0..2).")
            continue
        if not (0 <= row < size and 0 <= column < size):
            print(f"  Координаты должны быть в диапазоне 0..{size - 1}.")
            continue
        if matrix[row][column] != EMPTY:
            print("  Клетка уже занята, выберите другую.")
            continue
        return row, column


def result_text(winner):
    if winner == PLAYER_X:
        return "Вы победили! (X)"
    if winner == PLAYER_O:
        return "Победил компьютер. (O)"
    return "Ничья."


def main():
    game = requests.post(f"{BASE}/game").json()
    game_id = game["id"]
    matrix = game["field"]["matrix"]

    print_info()

    while not game["isOver"]:
        print("Текущая доска:")
        print(render(matrix))
        print()

        row, column = ask_move(matrix)
        matrix[row][column] = PLAYER_X

        game = requests.post(
            f"{BASE}/game/{game_id}",
            json={"field": {"matrix": matrix}},
        ).json()

        if "error" in game:
            print("Ошибка:", game["error"])
            matrix[row][column] = EMPTY
            continue

        matrix = game["field"]["matrix"]

    print("Итоговая доска:")
    print(render(matrix))
    print()
    print(result_text(game["winner"]))


if __name__ == "__main__":
    main()
