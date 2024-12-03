import numpy as np
from collections import Counter

location_lists = np.loadtxt("day-1/input.txt")
right_list_frequency = Counter(location_lists[:, 1])

list_similarity_score = np.sum(
    [location * right_list_frequency[location] for location in location_lists[:, 0]]
)
print(list_similarity_score)
