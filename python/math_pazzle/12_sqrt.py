# 平方根にしたとき、0-9 1の各文字が、最小の桁数で現れる自然数を求めよ。
# 整数部の有無でそれぞれ求めよ

from math import sqrt


def contain_nums(v):
    for n in range(10):
        str_n = str(n)
        if not str_n in v:
            return False
    return True


num = 0
while True:
    num += 1
    sq = '{0:10.10f}'.format(sqrt(num))
    sq = sq.replace('.', '')
    if contain_nums(sq[0:10]):
        print(f'num:{num}, value:{sqrt(num)}')
        break

num = 0
while True:
    num += 1
    sq = '{0:10.10f}'.format(sqrt(num))
    idx = sq.index('.') + 1
    sq = sq[idx:]
    if contain_nums(sq[0:10]):
        print(f'num:{num}, value:{sqrt(num)}')
        break
