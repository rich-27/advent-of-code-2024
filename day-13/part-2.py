def solve_for_tokens(a_x, a_y, b_x, b_y, goal_x, goal_y):
    # 1.:                       a_x * a_n + b_x * b_n = goal_x
    # 2.:                       a_y * a_n + b_y * b_n = goal_y
    # 3. Rearrange 2:           b_n = (goal_y - a_y * a_n) / b_y
    # 4. Substitute 3 into 1:   a_x * a_n + b_x * (goal_y - a_y * a_n) / b_y = goal_x
    # 5. Rearrange 4:           a_n = (goal_x - b_x * goal_y / b_y) / (a_x - b_x * a_y / b_y)
    a_n = round((goal_x - b_x * goal_y / b_y) / (a_x - b_x * a_y / b_y))
    b_n = round((goal_x - a_x * a_n) / b_x)
    if a_x * a_n + b_x * b_n == goal_x and a_y * a_n + b_y * b_n == goal_y:
        return 3 * a_n + b_n
    else:
        return 0


with open("day-13/input.txt", "r") as file:
    input = file.readlines()

tokens_to_win = 0
for index in range(0, len(input), 4):
    button_A_move, button_B_move = [
        [int(part.split("+")[1]) for part in line.split(",")]
        for line in [input[index], input[index + 1]]
    ]
    prize_coordinates = [
        int(part.split("=")[1]) + 10000000000000 for part in input[index + 2].split(",")
    ]
    tokens_to_win += solve_for_tokens(
        *button_A_move, *button_B_move, *prize_coordinates
    )

print(tokens_to_win)
