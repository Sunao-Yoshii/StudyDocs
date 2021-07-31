# 米式ルーレットと、ヨーロッパルーレットで、連続した N マスの合計値最大値を計算し、
# ...

# ルーレットのマスを作るのが面倒
eu = [0, 32, 15, 19, 4, 21, 2, 15, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
us = [0, 23, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 0, 27, 10, 25, 19, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2]


def sub_list(roulette, start, n):
    data = roulette[start:]
    if n > len(data):
        least = n - len(data)
        data = data + roulette[:least]
    else:
        data = data[:n]
    return data


def find_max(roulette, n):
    max = 0
    for st in range(len(roulette)):
        sub = sub_list(roulette, st, n)
        cur = sum(sub)
        if max < cur:
            max = cur
    return max


counter = 0
for n in range(2, 37):
    e_max = find_max(eu, n)
    u_max = find_max(us, n)
    if e_max < u_max:
        counter += 1

print(f'Found: {counter}')
