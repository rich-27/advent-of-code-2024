import numpy as np

with open("day-13/input.txt", "r") as file:
    input = file.readlines()


def solve_for_tokens(button_A, button_B, result):
    tokens = []
    for A_presses in range(101):
        A_answer = np.multiply(A_presses, button_A)
        if np.any(A_answer > result):
            break
        for B_presses in range(101):
            B_answer = np.add(A_answer, np.multiply(B_presses, button_B))
            if np.any(B_answer > result):
                break
            if np.any(B_answer < result):
                continue
            tokens.append(3 * A_presses + B_presses)
    return min(tokens) if len(tokens) > 0 else 0


tokens_to_win = 0
for index in range(0, len(input), 4):
    button_A, button_B = [
        [int(part.split("+")[1]) for part in line.split(",")]
        for line in [input[index], input[index + 1]]
    ]
    result = [int(part.split("=")[1]) for part in input[index + 2].split(",")]
    tokens_to_win += solve_for_tokens(button_A, button_B, result)

print(tokens_to_win)
