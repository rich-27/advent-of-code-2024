import numpy as np

location_lists = np.loadtxt("day-1/input.txt")

total_distance_between_lists = np.sum(
    np.abs(np.subtract(np.sort(location_lists[:, 0]), np.sort(location_lists[:, 1])))
)
print(total_distance_between_lists)
