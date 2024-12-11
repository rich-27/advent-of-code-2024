import numpy as np

stones = np.genfromtxt("day-11/input.txt", dtype=int, delimiter=" ").tolist()


def iterate_stone(stone):
    if stone == 0:
        return [1]

    stone_string = str(stone)
    if len(stone_string) % 2 == 0:
        middle = len(stone_string) // 2
        return [int(stone_string[:middle]), int(stone_string[middle:])]

    return [stone * 2024]


def iterate_stones(stones):
    return [new_stone for stone in stones for new_stone in iterate_stone(stone)]


for _ in range(25):
    stones = iterate_stones(stones)

print(len(stones))
