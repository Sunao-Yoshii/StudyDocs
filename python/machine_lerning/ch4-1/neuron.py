import math
import sys

INPUTNO = 2
MAX_INPUTNO = 100


def get_data(e: list) -> int:
    line_no = 0
    for line in sys.stdin:
        e[line_no] = [float(num) for num in line.split()]
        line_no += 1
    return line_no


def forward(w: list, e: list) -> float:
    u = 0.0
    for i in range(INPUTNO):
        u += e[i] * w[i]
    u -= w[INPUTNO]
    o = f(u)
    return o


def f(u: float) -> float:
    # ステップ
    #if u >= 0:
    #    return 1.0
    #else:
    #    return 0.0
    # シグモイド
    return 1.0 / (1.0 + math.exp(-u))


w = [1.0, 1.0, 1.5]
e = [[0.0 for i in range(INPUTNO)] for j in range(MAX_INPUTNO)]

n_of_e = get_data(e)
print(f'Data size: {n_of_e}')

for i in range(n_of_e):
    print(f'{i} : {e[i]} -> {forward(w, e[i])}')
