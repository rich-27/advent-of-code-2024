import numpy as np

wordsearch = np.genfromtxt("day-4/input.txt", dtype=str, delimiter=1)

def get_index_of_xmas_centre(diag_index, roll_amount, indices):
    return tuple(
        np.roll(np.diag(index_array, diag_index), -roll_amount)[1]
        for index_array in indices
    )


def get_diagonal_candidates(grid, indices):
    return {
        get_index_of_xmas_centre(diag_index, roll_amount, indices): np.roll(
            diagonal, -roll_amount
        )[:3]
        for diag_index, diagonal in {
            diag_index: np.diag(grid, diag_index)
            for diag_index in range(-(grid.shape[0] - 3), grid.shape[1] - 2)
        }.items()
        for roll_amount in range(len(diagonal) - 2)
    }


def get_candidates(grid):
    negatives = get_diagonal_candidates(
        np.flipud(grid),
        [np.flipud(index_grid) for index_grid in np.indices(grid.shape)],
    )
    return np.array(
        [
            [positive, negatives[centre_index]]
            for centre_index, positive in get_diagonal_candidates(
                grid, np.indices(grid.shape)
            ).items()
        ]
    )


x_mas_phrase = np.array(["M", "A", "S"])

x_mas_found_count = np.all(
    np.logical_or(
        *(
            np.all(get_candidates(wordsearch)[:, :] == phrase, axis=2)
            for phrase in [x_mas_phrase, np.flip(x_mas_phrase)]
        )
    ),
    axis=1,
).sum()

print(x_mas_found_count)
