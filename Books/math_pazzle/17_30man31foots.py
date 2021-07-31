BOY = 'B'
GIRL = 'G'

n = 30
memo = {}


def add(current: list) -> int:
    counts = len(current)

    # 30 人並んだら終了
    if counts >= n:
        return 1

    # 前回並んだ人
    last = current[-1] if counts > 0 else 'N'

    # メモがあればそこから応答
    if (last, counts) in memo:
        return memo[(last, counts)]

    # 男女を繋げる
    cnt = 0
    for cur in [BOY, GIRL]:
        # 女性は連続して並べない
        if last == GIRL and cur == GIRL:
            continue
        # パターンをカウント
        cp = current[:]
        cp.append(cur)
        cnt += add(cp)

    # メモ化
    memo[(last, counts)] = cnt

    # カウント応答
    return cnt


print(add([]))
