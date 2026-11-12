import requests

BASE = "http://127.0.0.1:5000"


EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2

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
    """Рисует доску с индексами строк/столбцов и клетками."""
    out = ["      0   1   2", "    +---+---+---+"]
    for r, row in enumerate(matrix):
        out.append(f"  {r} | " + " | ".join(SYMBOL[v] for v in row) + " |")
        out.append("    +---+---+---+")
    return "\n".join(out)


def ask_move(matrix):
    """Читает ход, пока пользователь не введёт корректную свободную клетку."""
    n = len(matrix)
    while True:
        raw = input("Ваш ход (строка столбец): ").strip().replace(",", " ")
        parts = raw.split()
        if len(parts) != 2:
            print("  Нужно ровно два числа: строка и столбец.")
            continue
        try:
            r, c = int(parts[0]), int(parts[1])
        except ValueError:
            print("  Введите целые числа (0..2).")
            continue
        if not (0 <= r < n and 0 <= c < n):
            print(f"  Координаты должны быть в диапазоне 0..{n - 1}.")
            continue
        if matrix[r][c] != EMPTY:
            print("  Клетка уже занята, выберите другую.")
            continue
        return r, c


def result_text(winner):
    if winner == PLAYER_X:
        return "Вы победили! (X)"
    if winner == PLAYER_O:
        return "Победил компьютер. (O)"
    return "Ничья."


def main():
    game = requests.post(f"{BASE}/game").json()
    gid = game["id"]
    matrix = game["field"]["matrix"]

    print_info()

    while not game["isOver"]:
        print("Текущая доска:")
        print(render(matrix))
        print()

        r, c = ask_move(matrix)
        matrix[r][c] = PLAYER_X

        game = requests.post(
            f"{BASE}/game/{gid}",
            json={"field": {"matrix": matrix}},
        ).json()

        if "error" in game:
            print("Ошибка:", game["error"])
            matrix[r][c] = EMPTY
            continue

        matrix = game["field"]["matrix"]

    print("Итоговая доска:")
    print(render(matrix))
    print()
    print(result_text(game["winner"]))


if __name__ == "__main__":
    main()
