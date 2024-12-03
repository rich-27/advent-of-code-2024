import pandas as pd
import numpy as np
from itertools import combinations

reactor_reports = [
    np.array(report.split(), dtype=int)
    for report in np.loadtxt("day-2/input.txt", dtype=str, delimiter=",")
]


def check_safety(report):
    differences = np.subtract(report[1:], report[:-1])
    signs, values = (np.sign(differences), np.abs(differences))
    return np.all(signs == signs[0]) and np.all(
        np.logical_and(values >= 1, values <= 3)
    )


reports_are_safe = [
    np.any(
        [
            check_safety(report)
            for report in [report, *combinations(report, len(report) - 1)]
        ]
    )
    for report in reactor_reports
]

safe_report_count = np.sum(1 if is_safe else 0 for is_safe in reports_are_safe)
print(safe_report_count)
