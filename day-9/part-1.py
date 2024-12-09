import numpy as np

dense_file_map = np.append(np.genfromtxt("day-9/input.txt", dtype=int, delimiter=1), [0]).reshape([-1, 2])

blocks, free_space = np.sum(dense_file_map, axis=0)

file_map = [block for index, (file_size, free_size) in enumerate(dense_file_map) for block in [*(index for _ in range(file_size)), *(-1 for _ in range(free_size))]]

def scan(head, tail):
    while file_map[head] != -1:
        head += 1

    while file_map[tail] == -1:
        tail -= 1
    
    return head, tail

head, tail = scan(0, len(file_map) - 1)
while head < tail:
    file_map[head], file_map[tail] = file_map[tail], file_map[head]
    head, tail = scan(head, tail)

print(np.sum(np.multiply(file_map[:head], range(head)), dtype=np.int64))