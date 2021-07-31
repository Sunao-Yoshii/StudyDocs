import math
import random
import copy


MAXVALUE = 100  # 重さと価値の最大
N = 30  # 荷物の個数
WEIGHTLIMIT = N * MAXVALUE / 4  # 重量制限
POOLSIZE =30  # 遺伝子プールサイズ
LASTG = 50  # 打ち切り世代
MRATE = 0.01  # 突然変異確率
SEED = 32767  # 乱数シード

# 荷物リスト
parcel = [[0 for i in range(2)] \
    for j in range(N)]


def rand_int(n):
    return random.randint(0, n - 1)


def init_percel():
    """荷物リストを標準入力から初期化する。"""
    i = 0
    while i < N:
        try:
            line = input()
        except EOFError:
            break
        parcel[i] = [int(num) for num in line.split()]
        i += 1


def mating(pool, ngpool):
    """交叉（遺伝子交換）"""
    roulette = [0 for i in range(POOLSIZE)]
    totalfitness = 0

    for i in range(POOLSIZE):
        roulette[i] = evalfit(pool[i])  # 指定した遺伝プールの各遺伝子を評価に置き換える
        totalfitness += roulette[i]  # トータル遺伝評価を加算する
    for i in range(POOLSIZE):
        while(True):
            mam = selectp(roulette, totalfitness)
            dad = selectp(roulette, totalfitness)
            if mam != dad:
                break
        # 両親を選んだら交叉
        crossing(pool[mam], pool[dad], ngpool[i * 2], ngpool[i * 2 + 1])


def evalfit(g):
    """遺伝子を食わせて、その評価を行う。ただしフローしている奴は価値なしと判断する。"""
    value = 0
    weight = 0
    for pos in range(N):
        weight += parcel[pos][0] * g[pos]
        value += parcel[pos][1] * g[pos]
    if weight >= WEIGHTLIMIT:
        # フローしてたら遺伝子の価値なし（致死遺伝）
        value = 0
    return value


def selectp(roulette, totalfitness):
    """親遺伝子のインデックスを選択する"""
    acc = 0
    ball = rand_int(totalfitness)  # 遺伝子プール評価の合計をマックスに、閾値をランダム取得
    for i in range(POOLSIZE):
        acc += roulette[i]
        if acc > ball:  # 閾値を超えた瞬間のインデックスを取得
            return i


def crossing(m, d, c1, c2):
    """指定のあった 2 遺伝子の交叉"""
    cp = rand_int(N)  # 遺伝子を入れ替える座標
    for j in range(cp):
        # 両親から指定座標までの遺伝子をコピー
        c1[j] = m[j]
        c2[j] = d[j]
    for j in range(cp, N):
        # 遺伝子の残りを親を変えて取得
        c1[j] = d[j]
        c2[j] = m[j]


def mutation(ngpool):
    """突然変異"""
    for i in range(POOLSIZE * 2):
        for j in range(N):
            if random.random() < MRATE:
                # 遺伝子中の超特定部位が、MRATE 確率で反転する。
                ngpool[i][j] = 1 if ngpool[i][j] == 0 else 0


def selecting(ngpool, pool):
    totalfitness = 0
    roulette = [0 for i in range(POOLSIZE * 2)]
    acc = 0

    for i in range(POOLSIZE):
        totalfitness = 0
        # 次世代プールの遺伝的価値リストの作成と、
        # 遺伝価値合計の計算
        for c in range(POOLSIZE * 2):
            roulette[c] = evalfit(ngpool[c])
            totalfitness += roulette[c]

        # 染色体を選ぶ
        ball = rand_int(totalfitness)
        acc = 0
        for c in range(POOLSIZE * 2):
            acc += roulette[c]
            if acc > ball:
                break
        # 染色体を遺伝プールへコピー
        pool[i] = copy.deepcopy(ngpool[c])


def printp(pool):
    """結果出力"""
    totalfitness = 0
    bestfit = 0
    for i in range(POOLSIZE):
        fitness = evalfit(pool[i])
        if fitness > bestfit:  # Good 遺伝子
            bestfit = fitness
            elite = i
        #print(f'{pool[i]} :fitness = {fitness}')
        totalfitness += fitness
    print(f'Elites: {elite}, BestFit: {bestfit}, Mean: {totalfitness / POOLSIZE}')


random.seed(SEED)

pool = [[rand_int(2) for i in range(N)] for j in range(POOLSIZE)]
ngpool = [[0 for i in range(N)] for j in range(POOLSIZE * 2)]
generation = 0

# 初期化
init_percel()

for generation in range(LASTG):
    print(f'Gen: {generation}')

    mating(pool, ngpool)  # 交叉
    mutation(ngpool)  # 突然変異
    selecting(ngpool, pool)  # 次世代選択
    printp(pool)  # 出力結果
