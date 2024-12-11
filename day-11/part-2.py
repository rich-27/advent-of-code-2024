import numpy as np
from collections import Counter

stones = Counter(np.genfromtxt("day-11/input.txt", dtype=int, delimiter=" "))

stone_lookup = {0: [1]}


def add_stone(stone):
    stone_string = str(stone)
    if len(stone_string) % 2 == 0:
        middle = len(stone_string) // 2
        stone_lookup[stone] = [int(stone_string[:middle]), int(stone_string[middle:])]
    else:
        stone_lookup[stone] = [stone * 2024]


def iterate_stone(new_stones, stone, count):
    if stone not in stone_lookup:
        add_stone(stone)

    for new_stone in stone_lookup[stone]:
        new_stones[new_stone] += count


def iterate_stones(stones):
    new_stones = Counter()
    for stone in stones.keys():
        iterate_stone(new_stones, int(stone), stones[stone])
    return new_stones


for n in range(75):
    print(f"{n}: {sum(stones.values())}")
    stones = iterate_stones(stones)

print(f"75: {sum(stones.values())}")
