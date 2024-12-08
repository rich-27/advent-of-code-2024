import numpy as np
from itertools import combinations

antenna_map = np.genfromtxt("day-8/input.txt", dtype=str, delimiter=1)

indices = np.moveaxis(np.indices(antenna_map.shape), 0, -1)

unique_antennas = np.sort(np.unique(antenna_map[antenna_map != "."]))

map_layers = np.full([unique_antennas.size, *antenna_map.shape], ".")

for layer_index, layer_antenna in enumerate(unique_antennas):
    layer_filter = antenna_map == layer_antenna
    map_layers[layer_index, layer_filter] = layer_antenna

    for antenna_index_pair in combinations(indices[layer_filter], 2):
        difference = np.subtract(*antenna_index_pair)

        for antinode_index in [
            np.add(antenna_index_pair[0], difference),
            np.subtract(antenna_index_pair[1], difference),
        ]:
            if not np.any(np.all(indices == antinode_index, axis=2)):
                continue

            map_layers[layer_index, *antinode_index] = "#"

unique_antinode_positions = np.any(map_layers == "#", axis=0).sum()
print(unique_antinode_positions)
