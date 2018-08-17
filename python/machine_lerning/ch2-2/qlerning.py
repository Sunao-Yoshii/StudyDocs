# Q学習サンプル
import random


# 定数系
LOOP_MAX = 1000
NODE_NUM = 15
LERN_RATE = 0.1
TEST_RATE = 0.9
RANDOM_RATE = 0.3
RANDOM_SEED = 32765


def selecta(olds, qvalue):
    """行動選択"""
    if random.random() < RANDOM_RATE:
        # 一定値以下のランダム値のケースでランダム行動
        if random.randint(0, 1) == 0:
            s = 2 * olds + 1
        else:
            s = 2 * olds + 2
    else:
        # Q 値最大値を選択
        if qvalue[2 * olds + 1] > qvalue[2 * olds + 2]:
            s = 2 * olds + 1
        else:
            s = 2 * olds + 2
    return s


def updateq(s, qvalue):
    """Q value 更新"""
    if s > 6:
        if s == 14:
            qv = qvalue[s] + int(LERN_RATE * (1000 - qvalue[s]))
        else:
            qv = qvalue[s]
    else:
        if qvalue[2 * s + 1] > qvalue[2 * s + 2]:
            qmax = qvalue[2 * s + 1]
        else:
            qmax = qvalue[2 * s + 2]
        qv = qvalue[s] + int(LERN_RATE * (TEST_RATE * qmax - qvalue[s]))
    return qv


# init random
random.seed(RANDOM_SEED)

# Q 値の設定
qvalue = [random.randint(0, 100) for i in range(NODE_NUM)]
print(qvalue)

# 学習本体
for i in range(LOOP_MAX):
    s = 0  # 行動の初期値
    # 最下段まで処理を繰り返す
    for t in range(3):
        # 行動選択
        s = selecta(s, qvalue)
        # Q 値更新
        qvalue[s] = updateq(s, qvalue)
    print(qvalue)
