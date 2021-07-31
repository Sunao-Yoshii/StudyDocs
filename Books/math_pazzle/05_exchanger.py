# 1000 円札を両替機に入れた時、両替のパターンはいくつかるか？
# 条件として
# 1. 硬貨は 500,100,50,10 円のみである
# 2. 15 枚を超えることはない

coins = [500, 100, 50, 10]
max_stack = 15
memo = {}

def exchange(remain, usables, coin_stack):
    # メモがあるならそこから返す
    key = (remain, len(usables), len(coin_stack))
    if key in memo:
        return memo[key]

    if remain == 0:
        # 再起の果てで、0 円達成 = 両替できたらOK終了
        print(coin_stack)
        return 1
    elif len(coin_stack) >= max_stack:
        # コインの組み合わせが 15 を超えそうなら、NG
        return 0

    counter = 0

    for next in range(len(usables)):
        next_coins = usables[next:]  # 使えるコインの種類は、そのままか先頭から１種類減る
        next_remain = remain - next_coins[0]  # 残りの支払い金額計算して
        next_stack = coin_stack[:]
        next_stack.append(next_coins[0])  # コインスタックを増やす(表示用)
        counter += exchange(next_remain, next_coins, next_stack)

    # 戻ってきたらメモに記録
    memo[key] = counter
    return counter


print(exchange(1000, [500, 100, 50, 10], []))
