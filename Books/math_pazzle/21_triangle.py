count = 0
line = 1
row = 1

END = 2014

while count < END:
    row ^= row << 1
    count += len([v for v in bin(row) if v == '0'])
    line += 1

print(line)
