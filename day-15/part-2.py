import numpy as np
import math
from PIL import Image, ImageFont, ImageDraw

with open("day-15/input.txt", "r") as file:
    warehouse_map, moves = [part.splitlines() for part in file.read().split("\n\n")]

expand_lookup = {"#": "##", "O": "[]", ".": "..", "@": "@."}
warehouse_map = np.array(
    [
        [expanded_item for item in line for expanded_item in expand_lookup[item]]
        for line in warehouse_map
    ]
)

moves = "".join(moves)

map_indices = np.stack(np.indices(warehouse_map.shape), axis=-1)


def sanitise_1d(array, type: type):
    return tuple(type(item) for item in array)


def sanitise_2d(array, type: type):
    return [sanitise_1d(item, type) for item in array]


robot_location = sanitise_1d(map_indices[warehouse_map == "@"][0], int)


def get_new_location(location, move):
    return {
        ">": (location[0], location[1] + 1),
        "v": (location[0] + 1, location[1]),
        "<": (location[0], location[1] - 1),
        "^": (location[0] - 1, location[1]),
    }[move]


def basic_rayfind(start_location: tuple[int, int], move: str, max_length: int = None):
    row_index, column_index = start_location
    direction = {">": 1, "v": 1, "<": -1, "^": -1}[move]

    ray = [
        str(symbol)
        for symbol in {
            ">": warehouse_map[row_index, column_index::direction],
            "v": warehouse_map[row_index::direction, column_index],
            "<": warehouse_map[row_index, column_index::direction],
            "^": warehouse_map[row_index::direction, column_index],
        }[move]
    ]

    if max_length is None:
        max_length = len(ray)
    ray = ray[:max_length]

    compression_index = max_length - 1

    if "#" in ray:
        slice_index = ray.index("#")
        ray = ray[:slice_index]
        compression_index = slice_index - 1

    if "." in ray:
        compression_index = ray.index(".")

    slices = {
        ">": (row_index, slice(column_index, column_index + compression_index + 1)),
        "v": (slice(row_index, row_index + compression_index + 1), column_index),
        "<": (row_index, slice(column_index, column_index - compression_index - 1, -1)),
        "^": (slice(row_index, row_index - compression_index - 1, -1), column_index),
    }[move]

    return (
        ray,
        compression_index,
        slices,
        {True: [".", *ray[:compression_index]], False: None}["." in ray],
    )


def rayfind(start_location: tuple[int, int], move: str):
    branch_results = []
    changed_locations = []

    def branching_rayfind(ray, compression_index, slices, compressed_ray):
        new_branch_locations = []
        if move in ["v", "^"]:
            new_locations = [
                get_new_location(location, {"[": ">", "]": "<"}[symbol])
                for symbol, location in zip(
                    ray, sanitise_2d(map_indices[*slices][:compression_index], int)
                )
                if symbol in ["[", "]"]
            ]

            if any(location in changed_locations for location in new_locations):
                return True

            for location in new_locations:
                changed_locations.append(location)

            new_branch_locations = new_locations

        if compressed_ray is None:
            return False

        branch_results.append((ray, slices, compressed_ray))

        return all(
            [
                branching_rayfind(
                    *basic_rayfind(new_location, move, len(compressed_ray))
                )
                for new_location in new_branch_locations
            ]
        )

    can_move = branching_rayfind(*basic_rayfind(start_location, move))
    return branch_results if can_move else []


class Output_Picture:
    def __init__(self, filename):
        self.filename = filename

        self.font = ImageFont.truetype("consola.ttf", size=40)

        self.background_colour = "#181818"
        self.text_colour = "#ccc"

        self.text = None

    def create(self, text):
        self.text = text

        font_points_to_pixels = lambda pt: round(pt * 96.0 / 72)
        self.margin_pixels = 20

        def get_size(text):
            left, top, right, bottom = self.font.getbbox(text)
            return right - left, bottom - top

        line_sizes = [get_size(line) for line in self.text]

        self.max_line_height = font_points_to_pixels(
            max((line_height for _, line_height in line_sizes))
        )

        image_width = int(
            math.ceil(
                max((line_width for line_width, _ in line_sizes))
                + (2 * self.margin_pixels)
            )
        )
        # 0.8 because apparently it measures a lot of space above visible content
        image_height = int(
            math.ceil(self.max_line_height * 0.8 * len(text) + 2 * self.margin_pixels)
        )
        self.image_size = (image_width, image_height)

        PIL_GRAYSCALE = "L"
        self.image = Image.new(PIL_GRAYSCALE, self.image_size, color=self.background_colour)
        self.draw = ImageDraw.Draw(self.image)

        for index, line in enumerate(self.text):
            self.draw_line(self.get_position(index), line)

        self.image.save(self.filename)

    def get_position(self, i):
        return (
            self.margin_pixels,
            int(round(self.margin_pixels + (i * 0.8 * self.max_line_height))),
        )

    def clear_line(self, position, text):
        box = self.draw.textbbox(position, text, font=self.font)
        self.draw.rectangle(box, fill=self.background_colour)

    def draw_line(self, position, text):
        self.draw.text(position, text, fill=self.text_colour, font=self.font)

    def update(self, text):
        if self.text is None:
            self.create(text)
            return

        for index, (old_line, new_line) in enumerate(zip(self.text, text)):
            if old_line != new_line:
                position = self.get_position(index)
                self.clear_line(position, old_line)
                self.draw_line(position, new_line)

        self.image.save(self.filename)


output_picture = Output_Picture("day-15/output.png")


def output_step(move_index, move):
    output_picture.update(
        [
            f"Warehouse map after move {move_index}({move}):\n",
            *(f"{''.join(line)}\n" for line in warehouse_map),
        ]
    )


output_step(0, None)
for move_index, move in enumerate(moves):
    rays = rayfind(robot_location, move)
    for _, slices, compressed_ray in rays:
        if compressed_ray != None:
            warehouse_map[*slices] = compressed_ray

    if len(rays) > 0:
        robot_location = get_new_location(robot_location, move)

    output_step(move_index + 1, move)
    input()

print(
    sum(sanitise_1d(np.sum(map_indices[warehouse_map == "["] * [100, 1], axis=-1), int))
)
