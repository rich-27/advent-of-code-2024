from math import floor
import numpy as np
from dataclasses import dataclass

# with open("day-5/test-input.txt", "r") as file:
with open("day-5/input.txt", "r") as file:
    print_instructions = file.readlines()

ordering_rules = np.array(
    [line.split("|") for line in print_instructions if "|" in line], dtype=int
)


@dataclass
class Page_Specification:
    antecedent_pages: np.ndarray
    subsequent_pages: np.ndarray


def get_page_rule(page_no, column_index):
    # Create bool array to filter rows with
    is_page_no = np.fliplr(ordering_rules)[:, column_index] == page_no
    return np.sort(ordering_rules[is_page_no, column_index])


rule_lookup = {
    page_no: Page_Specification(
        # other_pages_index:
        # 0 where ordering_rule is: antecedent_page_no | page_no
        # 1 where ordering_rule is: page_no | subsequent_page_no
        *(get_page_rule(page_no, other_pages_index) for other_pages_index in [0, 1])
    )
    for page_no in np.sort(np.unique(ordering_rules))
}


updates_to_print = [
    np.array(line.split(","), dtype=int) for line in print_instructions if "," in line
]


def does_not_overlap(page_rule: Page_Specification, update_spec: Page_Specification):
    return np.all(
        [
            len(np.intersect1d(update_values, rule_values)) == 0
            for update_values, rule_values in [
                (update_spec.antecedent_pages, page_rule.subsequent_pages),
                (update_spec.subsequent_pages, page_rule.antecedent_pages),
            ]
        ]
    )


def update_is_valid(update_to_print):
    return np.all(
        [
            does_not_overlap(
                rule_lookup[page_no],
                Page_Specification(
                    update_to_print[:page_index], update_to_print[page_index + 1 :]
                ),
            )
            for page_index, page_no in enumerate(update_to_print)
        ]
    )


valid_updates = [update for update in updates_to_print if update_is_valid(update)]

middle_page_numbers = [update[update.size // 2] for update in valid_updates]

print(np.sum(middle_page_numbers))
