import numpy as np
from itertools import product

def split_equation_string(result: str, operands: str):
    return int(result), [int(op) for op in operands.strip().split(' ')]


with open("day-7/input.txt", "r") as file:
    calibration_equations = [split_equation_string(*line.split(':')) for line in file.readlines()]

def evaluate_equation(operands: list[int], operations: list[str]):
    result = operands.pop(0)
    while len(operands) > 0:
        match operations.pop(0):
            case '+':
                result += operands.pop(0)
            case '*':
                result *= operands.pop(0)
    return result

total_calibration_result = 0
for result, operands in calibration_equations:
    operations = list(product(['+', '*'], repeat=len(operands) - 1))
    print(f'Evaluating {len(operations)} for {result}')
    for operation_set in operations:
        if evaluate_equation(operands.copy(), list(operation_set)) == result:
            total_calibration_result += result
            print(f'Found: {operation_set}')
            break

print(total_calibration_result)