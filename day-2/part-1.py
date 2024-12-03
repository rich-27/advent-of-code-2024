import pandas as pd
import numpy as np

reactor_reports = [np.array(report.split(), dtype=int) for report in np.loadtxt("day-2/input.txt", dtype=str, delimiter=',')]

def check_safety(report):
    differences = np.subtract(report[1:], report[:-1])
    signs, values = (np.sign(differences), np.abs(differences))
    return np.all(signs == signs[0]) and np.all(np.logical_and(values >= 1, values <= 3))

safe_report_count = np.sum([1 if check_safety(row) else 0 for row in reactor_reports])
print(safe_report_count)
