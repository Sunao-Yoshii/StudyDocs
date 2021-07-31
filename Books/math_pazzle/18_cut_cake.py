from math import sqrt


def is_square_pairs(n: int, cuts: list, squares: list) -> bool:
    prev = cuts[-1]
    if n == len(cuts):
        # 全要素が埋まった
        if (1 + prev) in squares:
            # 最初の一つ（固定 1）と最後の一つの合計がが平方数である
            print(f'Count: {n}, Cuts: {cuts}')
            return True
    else:
        # 接続し得る候補の計算
        maybe = [x for x in range(1, n + 1) if x not in cuts]
        # 候補を順に試していく
        for i in maybe:
            # 前回の値と今回の値の合計が
            if (prev + i) in squares:
                if is_square_pairs(n, cuts + [i], squares):
                    return True
    return False


n = 2

while True:
    sqrts = [x ** 2 for x in range(2, int(sqrt(n * 2) + 1))]
    if is_square_pairs(n, [1], sqrts):
        break
    n += 1

print(n)
