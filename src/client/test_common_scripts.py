import sys

import requests
from tictactoe.common.constants import SIZE, CellValue

BASE = "http://127.0.0.1:5000"
EMPTY_BOARD = [[CellValue.EMPTY] * SIZE for _ in range(SIZE)]


RESET = "\033[0m"
GREEN = "\033[32m"
RED = "\033[31m"
BOLD = "\033[1m"

passed_count = 0
failed_count = 0


def check(name, condition, detail=""):
    global passed_count, failed_count
    if condition:
        print(f"  {GREEN}[PASS]{RESET} {name}")
        passed_count += 1
    else:
        message = f"  {RED}[FAIL]{RESET} {name}"
        if detail:
            message += f" {RED}— {detail}{RESET}"
        print(message)
        failed_count += 1


def create_game():
    return requests.post(f"{BASE}/game").json()


def post_move(game_id, matrix):
    return requests.post(f"{BASE}/game/{game_id}", json={"field": {"matrix": matrix}})


def copy_matrix(matrix):
    return [list(row) for row in matrix]


def play_one_move(game, row, column):
    matrix = copy_matrix(game["field"]["matrix"])
    if matrix[row][column] != CellValue.EMPTY:
        return None
    matrix[row][column] = CellValue.PLAYER_X
    response = post_move(game["id"], matrix)
    if response.status_code != 200:
        return None
    return response.json()


def play_until_over(game):
    while not game["isOver"]:
        matrix = game["field"]["matrix"]
        played = False
        for row in range(3):
            for column in range(3):
                if matrix[row][column] == CellValue.EMPTY:
                    next_game = play_one_move(game, row, column)
                    if next_game is not None:
                        game = next_game
                        played = True
                        break
            if played:
                break
        if not played:
            break
    return game


def test_create_game():
    print("\n[Scenario: creating a new game]")
    response = requests.post(f"{BASE}/game")
    check("status is 201", response.status_code == 201, f"got {response.status_code}")
    body = response.json()
    check("response has id", "id" in body)
    check("field.matrix is empty 3x3", body["field"]["matrix"] == EMPTY_BOARD)
    check("winner is None", body["winner"] is None)
    check("isOver is False", body["isOver"] is False)


def test_invalid_uuid():
    print("\n[Scenario: invalid UUID format]")
    response = requests.post(
        f"{BASE}/game/not-a-uuid", json={"field": {"matrix": EMPTY_BOARD}}
    )
    check("status is 400", response.status_code == 400, f"got {response.status_code}")
    check("response contains error", "error" in response.json())


def test_nonexistent_game():
    print("\n[Scenario: move in a nonexistent game]")
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = requests.post(
        f"{BASE}/game/{fake_id}", json={"field": {"matrix": EMPTY_BOARD}}
    )
    check("status is 400", response.status_code == 400, f"got {response.status_code}")
    check(
        "error mentions 'не найдена'", "не найдена" in response.json().get("error", "")
    )


def test_missing_json_body():
    print("\n[Scenario: request without a JSON body]")
    game = create_game()
    response = requests.post(f"{BASE}/game/{game['id']}")
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_malformed_json():
    print("\n[Scenario: malformed JSON body]")
    game = create_game()
    response = requests.post(
        f"{BASE}/game/{game['id']}",
        data="this is definitely not json",
        headers={"Content-Type": "application/json"},
    )
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_json_not_object():
    print("\n[Scenario: JSON body is not an object]")
    game = create_game()
    response = requests.post(f"{BASE}/game/{game['id']}", json=[1, 2, 3])
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_missing_field_key():
    print("\n[Scenario: body without 'field']")
    game = create_game()
    response = requests.post(f"{BASE}/game/{game['id']}", json={})
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_missing_matrix_key():
    print("\n[Scenario: body without 'field.matrix']")
    game = create_game()
    response = requests.post(f"{BASE}/game/{game['id']}", json={"field": {}})
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_wrong_matrix_size():
    print("\n[Scenario: matrix is not 3x3]")
    game = create_game()
    response = post_move(game["id"], [[0, 0], [0, 0]])
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_invalid_cell_value():
    print("\n[Scenario: cell value outside 0/1/2]")
    game = create_game()
    matrix = copy_matrix(EMPTY_BOARD)
    matrix[0][0] = 5
    response = post_move(game["id"], matrix)
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_wrong_turn_count():
    print("\n[Scenario: two X marks placed on the first turn]")
    game = create_game()
    matrix = copy_matrix(EMPTY_BOARD)
    matrix[0][0] = CellValue.PLAYER_X
    matrix[0][1] = CellValue.PLAYER_X
    response = post_move(game["id"], matrix)
    check("status is 400", response.status_code == 400, f"got {response.status_code}")
    check("error mentions count", "количество" in response.json().get("error", ""))


def test_both_winners():
    print("\n[Scenario: both X and O have winning lines]")
    game = create_game()
    matrix = [
        [1, 1, 1],
        [2, 2, 2],
        [0, 0, 0],
    ]
    response = post_move(game["id"], matrix)
    check("status is 400", response.status_code == 400, f"got {response.status_code}")
    check(
        "error mentions two winners",
        "два победителя" in response.json().get("error", ""),
    )


def test_modify_previous_move():
    print("\n[Scenario: modifying a previous move]")
    game = create_game()
    matrix = copy_matrix(game["field"]["matrix"])
    matrix[0][0] = CellValue.PLAYER_X
    game = post_move(game["id"], matrix).json()
    check("first move accepted", game["isOver"] is False)

    board = copy_matrix(game["field"]["matrix"])

    x_position = None
    for row in range(3):
        for column in range(3):
            if board[row][column] == CellValue.PLAYER_X:
                x_position = (row, column)
                break
        if x_position:
            break

    free_position = None
    for row in range(3):
        for column in range(3):
            if board[row][column] == CellValue.EMPTY:
                free_position = (row, column)
                break
        if free_position:
            break

    old_row, old_column = x_position
    new_row, new_column = free_position
    board[old_row][old_column] = CellValue.EMPTY
    board[new_row][new_column] = CellValue.PLAYER_X

    response = post_move(game["id"], board)
    check("status is 400", response.status_code == 400, f"got {response.status_code}")
    check(
        "error mentions changed cells",
        "Изменены" in response.json().get("error", ""),
    )


def test_two_new_moves_at_once():
    print("\n[Scenario: two cells added in one request]")
    game = create_game()
    matrix = copy_matrix(game["field"]["matrix"])
    matrix[0][0] = CellValue.PLAYER_X
    game = post_move(game["id"], matrix).json()

    board = copy_matrix(game["field"]["matrix"])
    free_cells = [
        (row, column)
        for row in range(3)
        for column in range(3)
        if board[row][column] == CellValue.EMPTY
    ]
    (row_x, col_x), (row_o, col_o) = free_cells[0], free_cells[1]
    board[row_x][col_x] = CellValue.PLAYER_X
    board[row_o][col_o] = CellValue.PLAYER_O

    response = post_move(game["id"], board)
    check("status is 400", response.status_code == 400, f"got {response.status_code}")
    check(
        "error mentions 'добавлено'",
        "добавлено" in response.json().get("error", ""),
    )


def test_no_new_move():
    print("\n[Scenario: the same matrix is sent without a new move]")
    game = create_game()
    matrix = copy_matrix(game["field"]["matrix"])
    matrix[0][0] = CellValue.PLAYER_X
    game = post_move(game["id"], matrix).json()

    response = post_move(game["id"], copy_matrix(game["field"]["matrix"]))
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_full_game():
    print("\n[Scenario: full game — perfect AI must never lose]")
    game = play_until_over(create_game())
    check("game ended", game["isOver"] is True)
    check(
        "X did not win against the minimax AI",
        game["winner"] != CellValue.PLAYER_X,
        f"winner={game['winner']}",
    )
    if game["winner"] == CellValue.PLAYER_O:
        print("  (AI won — X was pushed into a losing line)")
    elif game["winner"] is None:
        print("  (game ended in a draw)")


def test_play_after_game_over():
    print("\n[Scenario: move after the game is already over]")
    game = play_until_over(create_game())
    check("game is over", game["isOver"] is True)
    response = post_move(game["id"], copy_matrix(game["field"]["matrix"]))
    check("status is 400", response.status_code == 400, f"got {response.status_code}")


def test_multiple_independent_games():
    print("\n[Scenario: multiple games run independently]")
    game_a = create_game()
    game_b = create_game()
    check("different ids", game_a["id"] != game_b["id"])

    matrix_a = copy_matrix(game_a["field"]["matrix"])
    matrix_a[0][0] = CellValue.PLAYER_X
    response_a = post_move(game_a["id"], matrix_a)
    check("game A accepted first move", response_a.status_code == 200)

    matrix_b = copy_matrix(game_b["field"]["matrix"])
    matrix_b[2][2] = CellValue.PLAYER_X
    response_b = post_move(game_b["id"], matrix_b)
    check("game B accepted first move", response_b.status_code == 200)

    state_a = response_a.json()
    state_b = response_b.json()
    check(
        "game A and game B have different boards",
        state_a["field"]["matrix"] != state_b["field"]["matrix"],
    )


def main():
    print(f"Running scenario tests against {BASE}")
    try:
        requests.get(f"{BASE}/", timeout=2)
    except requests.ConnectionError:
        print(f"{RED}ERROR: server is not running at {BASE}{RESET}")
        sys.exit(2)

    test_create_game()
    test_invalid_uuid()
    test_nonexistent_game()
    test_missing_json_body()
    test_malformed_json()
    test_json_not_object()
    test_missing_field_key()
    test_missing_matrix_key()
    test_wrong_matrix_size()
    test_invalid_cell_value()
    test_wrong_turn_count()
    test_both_winners()
    test_modify_previous_move()
    test_two_new_moves_at_once()
    test_no_new_move()
    test_full_game()
    test_play_after_game_over()
    test_multiple_independent_games()

    print("\n" + "=" * 50)
    summary_color = GREEN if failed_count == 0 else RED
    print(
        f"{summary_color}{BOLD}Passed: {passed_count}   Failed: {failed_count}{RESET}"
    )
    if failed_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
