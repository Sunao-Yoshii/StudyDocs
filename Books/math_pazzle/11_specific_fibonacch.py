# フィボナッチ数の中で、各桁を足し合わせた数で割り切れるものを探せ
# 1, 3, 5,8, 21,144 まではわかっているので、それ以降を探しなさい。

start = 144
limit = 5


def is_matched(num):
    str_num = str(num)
    for idx in range(len(str_num) - 1, 0, -1):
        str_num = str_num[:idx] + '+' + str_num[idx:]
    sum_val = eval(str_num)
    return num % sum_val == 0


def limted_fib(left, right, results):
    next = left + right
    # 再起終了条件
    if is_matched(next) and next > start:
        results.append(next)
        if len(results) >= limit:
            return results
    # fib 継続
    return limted_fib(right, next, results)


results = limted_fib(1, 1, [])
print(results)
