import numpy as np
from itertools import combinations

adjacents = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])
corner_offsets = np.array([(0, 0), (0, 1), (1, 1), (1, 0)])

garden = np.genfromtxt("day-12/input.txt", dtype=str, delimiter=1)


def tuplify(array_of_array_of_ints):
    return [
        tuple(int(item) for item in array_of_ints)
        for array_of_ints in array_of_array_of_ints
    ]


def santitise(array):
    return tuple(tuplify(array))


class Edge(tuple[tuple[int, int]]):
    def __new__(cls, corners=...):
        return super(Edge, cls).__new__(cls, tuple(sorted(tuplify(corners))))

    def is_colinear(self, edge):
        return any(
            [
                len(set(tuple(np.ravel(values)))) == 1
                for values in np.unstack(np.stack([self, edge], axis=0), axis=-1)
            ]
        )

    def is_adjacent(self, edge):
        return any(corner in self for corner in edge)

    def is_contiguous(self, edge):
        return self.is_colinear(edge) and self.is_adjacent(edge)


class Side:
    def __init__(self, edges=[]):
        self.edges = set(sorted(edges))

    def is_contiguous(self, edge_or_side):
        if type(edge_or_side) == Edge:
            return any(edge.is_contiguous(edge_or_side) for edge in self.edges)
        if type(edge_or_side) == Side:
            return any(self.is_contiguous(edge) for edge in edge_or_side.edges)

    def append(self, edge):
        self.edges.add(edge)

    def concatenate(self, side):
        for edge in side.edges:
            self.append(edge)

    def __contains__(self, edge):
        return edge in self.edges

    def remove(self, edge):
        sorted_edges = sorted(self.edges)

        split_index = sorted_edges.index(edge)

        edge_sets = ([], [])
        for index, edge in enumerate(sorted_edges):
            if index < split_index:
                edge_sets[0].append(edge)
            if index > split_index:
                edge_sets[1].append(edge)

        return [Side(edge_set) for edge_set in edge_sets if len(edge_set) > 0]

    def get_vertices(self):
        return sorted(list(set(corner for edge in self.edges for corner in edge)))

    def intersection(self, side):
        for vertex in self.get_vertices()[1:-1]:
            if vertex in side.get_vertices()[1:-1]:
                return vertex

    def split(self, location):
        sorted_edges = sorted(self.edges)

        split_indices = []
        for edge in sorted_edges:
            if location in edge:
                split_indices.append(sorted_edges.index(edge))

        edge_sets = ([], [])
        for index, edge in enumerate(sorted_edges):
            if index <= split_indices[0]:
                edge_sets[0].append(edge)
            if index > -split_indices[1]:
                edge_sets[1].append(edge)

        return [Side(edge_set) for edge_set in edge_sets if len(edge_set) > 0]


class SideSet(set[Side]):
    def __init__(self, values=[]):
        super().__init__()

        for item in values:
            self.add(item)

    def __contains__(self, edge_or_side):
        if type(edge_or_side) == Edge:
            return any(edge_or_side in side for side in self)
        return super().__contains__(edge_or_side)

    def add_edge(self, edge, join):
        sides = [side for side in self if side.is_contiguous(edge)]

        if len(sides) == 0 or not join:
            super().add(Side([edge]))
            return

        sides[0].append(edge)
        for side in sides[1:]:
            self.remove(side)
            for edge in side.edges:
                sides[0].append(edge)

    def add_side(self, side, join):
        if join:
            for item in self:
                if not item.is_contiguous(side):
                    continue

                for edge in side.edges:
                    item.append(edge)

                return

        super().add(side)

    def add(self, edge_or_side, join=True):
        if type(edge_or_side) == Edge:
            self.add_edge(edge_or_side, join)
        if type(edge_or_side) == Side:
            self.add_side(edge_or_side, join)

    def remove_edge(self, edge):
        encapsulating_side = None

        for side in self:
            if edge in side:
                encapsulating_side = side
                break

        if encapsulating_side is not None:
            super().remove(encapsulating_side)
            for new_side in encapsulating_side.remove(edge):
                self.add(new_side)

    def remove(self, edge_or_side):
        if type(edge_or_side) == Edge:
            self.remove_edge(edge_or_side)
        if type(edge_or_side) == Side:
            super().remove(edge_or_side)


class Region:
    @property
    def area(self):
        return len(self.locations)

    @property
    def side_count(self):
        return len(self.sides)

    @property
    def value(self):
        return self.area * self.side_count

    def __init__(self, plant_type, locations=[]):
        self.plant_type = plant_type

        self.locations = []
        self.sides = SideSet()

        for location in locations:
            self.add(location)

    def add(self, location):
        self.locations.append(location)

        corners = np.add(location, corner_offsets)
        for edge in [
            Edge(corner_pair)
            for corner_pair in zip(corners, np.roll(corners, -1, axis=0))
        ]:
            if edge in self.sides:
                self.sides.remove(edge)
            else:
                self.sides.add(edge)

        return santitise(np.add(location, adjacents))

    def split_Xs(self):
        for sides in combinations(self.sides, 2):
            split_location = sides[0].intersection(sides[1])
            if split_location:
                for side in sides:
                    self.sides.remove(side)
                    for new_side in side.split(split_location):
                        self.sides.add(new_side, False)


regions: list[Region] = []
for plant_type in np.unique(garden):
    locations = tuplify(
        np.stack(np.indices(garden.shape), axis=-1)[garden == plant_type]
    )
    while len(locations) > 0:
        region = Region(plant_type)

        to_check = set(region.add(locations.pop(0)))

        while len(to_check) > 0:
            new_location = to_check.pop()
            if new_location not in locations:
                continue

            locations.remove(new_location)
            for adjacent_location in region.add(new_location):
                if adjacent_location not in region.locations:
                    to_check.add(adjacent_location)

        region.split_Xs()
        regions.append(region)


def get_width(regions, property):
    return len(str(max([getattr(region, property) for region in regions])))


area_width = get_width(regions, "area")
side_count_width = get_width(regions, "side_count")
value_width = get_width(regions, "value")

for region in regions:
    print(
        f"{region.plant_type} => area: {str(region.area):>{area_width}}, perimeter: {str(region.side_count):>{side_count_width}} => {region.value:>{value_width}}"
    )

print(sum([region.value for region in regions]))
