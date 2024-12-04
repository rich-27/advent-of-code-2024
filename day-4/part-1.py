import numpy as np

wordsearch = np.genfromtxt("day-4/input.txt", dtype=str, delimiter=1)

def get_horizontal_candidates(grid):
    return [
        np.roll(row, -roll_amount)[:4]
        for row in grid
        for roll_amount in range(len(row) - 3)
    ]


def get_diagonal_candidates(grid):
    return np.array(
        [
            np.roll(diagonal, -roll_amount)[:4]
            for diagonal in [
                np.diag(grid, diag_index)
                for diag_index in range(-(grid.shape[0] - 4), grid.shape[1] - 3)
            ]
            for roll_amount in range(len(diagonal) - 3)
        ]
    )


xmas_phrase = np.array(["X", "M", "A", "S"])

candidates = np.concatenate(
    [
        [
            candidate
            for grid in [wordsearch, wordsearch.T]
            for candidate in get_horizontal_candidates(grid)
        ],
        [
            candidate
            for grid in [wordsearch, np.flipud(wordsearch)]
            for candidate in get_diagonal_candidates(grid)
        ],
    ]
)

xmas_found_count = np.sum([np.all(candidates[:] == phrase, axis=1).sum() for phrase in [xmas_phrase, np.flip(xmas_phrase)]])

print(xmas_found_count)
