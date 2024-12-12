import numpy as np
from dataclasses import dataclass

adjacents = np.array([(0, 1), (1, 0), (0, -1), (-1, 0)])

garden = np.genfromtxt("day-12/input.txt", dtype=str, delimiter=1)


@dataclass
class Region:
    plant_type: str
    locations: list
    perimeter: int

    @property
    def area(self):
        return len(self.locations)

    @property
    def value(self):
        return self.area * self.perimeter


regions: list[Region] = []
for plant_type in np.unique(garden):
    locations = [
        tuple(loc)
        for loc in np.stack(np.indices(garden.shape), axis=-1)[garden == plant_type]
    ]
    while len(locations) > 0:
        region = Region(plant_type, [locations.pop(0)], 4)

        to_check = set(tuple(loc) for loc in np.add(region.locations[-1], adjacents))

        while len(to_check) > 0:
            new_location = to_check.pop()
            if new_location not in locations:
                continue

            locations.remove(new_location)
            region.locations.append(new_location)
            region.perimeter += 4

            for adjacent_location in [
                tuple(loc) for loc in np.add(region.locations[-1], adjacents)
            ]:
                if adjacent_location in region.locations:
                    region.perimeter -= 2
                else:
                    to_check.add(adjacent_location)

        regions.append(region)


def get_width(regions, property):
    return len(str(max([getattr(region, property) for region in regions])))


area_width = get_width(regions, "area")
perimeter_width = get_width(regions, "perimeter")
value_width = get_width(regions, "value")

for region in regions:
    print(
        f"{region.plant_type} => area: {str(region.area):>{area_width}}, perimeter: {str(region.perimeter):>{perimeter_width}} => {region.value:>{value_width}}"
    )

print(sum([region.value for region in regions]))
