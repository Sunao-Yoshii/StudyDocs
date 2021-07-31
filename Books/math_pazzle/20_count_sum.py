from itertools import combinations

numns = [
    1, 14, 14, 4,
    11, 7, 6, 9,
    8, 10, 10, 5,
    13, 2, 3, 15
]

counts = {}

for i in range(1, len(numns) + 1):
    for c in combinations(numns, i):
        sum_val = sum(c)
        if sum_val in counts.keys():
            counts[sum_val] += 1
        else:
            counts[sum_val] = 1

sum_value = 0
counter = 0

for key in counts.keys():
    if counter < counts[key]:
        counter = counts[key]
        sum_value = key

print(f'Sum: {sum_value}, Counts: {counter}')
