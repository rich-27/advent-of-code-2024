import re

with open("day-3/input.txt", "r") as file:
    corrupted_memory = file.read()

valid_command_matcher = r"((?:mul)?(?:do)?(?:don't)?)\(([0-9]+)?,?([0-9]+)?\)"

valid_commands = [
    (operation, None if operation != "mul" else int(operand_1) * int(operand_2))
    for operation, operand_1, operand_2 in re.findall(
        valid_command_matcher, corrupted_memory
    )
    if operation in ("do", "don't") or (operation == "mul" and operand_1 and operand_2)
]

mul_operation_total = 0
sum_flag = True
for command, value in valid_commands:
    match command:
        case "don't":
            sum_flag = False
        case "do":
            sum_flag = True
        case "mul" if sum_flag:
            mul_operation_total += value

print(mul_operation_total)
