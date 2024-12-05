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

    def get_all_values(self):
        return np.concatenate([self.antecedent_pages, self.subsequent_pages])

    def is_empty(self):
        return len(self.antecedent_pages) == 0 and len(self.subsequent_pages) == 0


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


def rule_conflicts(page_rule: Page_Specification, update_spec: Page_Specification):
    return Page_Specification(
        *(
            np.intersect1d(update_values, rule_values)
            for update_values, rule_values in [
                (update_spec.antecedent_pages, page_rule.subsequent_pages),
                (update_spec.subsequent_pages, page_rule.antecedent_pages),
            ]
        )
    )


def get_conflicts(update_to_print):
    conflicts = {
        page_no: rule_conflicts(
            rule_lookup[page_no],
            Page_Specification(
                update_to_print[:page_index], update_to_print[page_index + 1 :]
            ),
        )
        for page_index, page_no in enumerate(update_to_print)
    }
    return {
        page_no: conflict
        for page_no, conflict in conflicts.items()
        if not conflict.is_empty()
    }


def swap_values(array, value_1, value_2):
    index_1, index_2 = [np.where(array == value) for value in [value_1, value_2]]
    array[index_1], array[index_2] = array[index_2], array[index_1]
    return array


def fix_update(update_to_print: np.ndarray):
    issues = get_conflicts(update_to_print)
    while len(issues.keys()) > 0:
        next_page_no, next_conflict = next(iter(issues.items()))
        new_update = swap_values(
            update_to_print, next_page_no, next_conflict.get_all_values()[0]
        )
        issues = get_conflicts(new_update)

    return new_update


fixed_updates = [
    fix_update(update)
    for update in updates_to_print
    if len(get_conflicts(update).values()) > 0
]

middle_page_numbers = [update[update.size // 2] for update in fixed_updates]

print(np.sum(middle_page_numbers))
