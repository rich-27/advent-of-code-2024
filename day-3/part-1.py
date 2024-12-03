import re
import numpy as np

with open("day-3/input.txt", "r") as file:
    corrupted_memory = file.read()

valid_command_matcher = r"mul\(([0-9]+),([0-9]+)\)"

sum_of_mul_operations = np.sum(
    [
        int(mul_operand_1) * int(mul_operand_2)
        for mul_operand_1, mul_operand_2 in re.findall(
            valid_command_matcher, corrupted_memory
        )
    ]
)
print(sum_of_mul_operations)
