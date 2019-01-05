# プログラマ脳を鍛える数学パズル16問目
# 問題の内容はコードから察して
from itertools import combinations
from math import gcd

N = 500
count = 0

# sq * sq
#   = ((sq - x) + (sq + x)) + ((sq - y) * (sq * y))
#   = (sq*sq - x*x) + (sq*sq - y*y)
# -sq^2 = -x^2 -y^2
# sq^2 = x^2 + y^2

for n in range(1, int(N / 4) + 1):
    sqrt = n * n
    # 正方形に一辺を超えない範囲で二つの四角の一辺補正値を選ぶ
    # モノが四角形の一辺の為、正方形の一辺を超えると、
    # 四角形のくせに１辺がマイナス長とか意味不明な事象が起きるので
    for x, y in combinations(range(1, n), 2):
        if sqrt == x*x + y*y:
            if gcd(x, y) == 1:  # 同じ比率の整数倍を弾く
                count += 1

print(count)
