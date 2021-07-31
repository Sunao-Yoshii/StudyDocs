# 1000 までの数字で以下をみた偶数の数を数えなさい
# 1. 初回にのみ 3 倍して 1 を足します
# 2. Nが偶数なら 2 で割ります
# 3. N が奇数なら、3 倍して 1 を足します。
# 4. 2,3 を繰り返して初期値に戻る数を数えましょう

counter = 0
for start in range(2, 10000, 2):
    n = start * 3 + 1
    while True:
        n = n / 2 if n % 2 == 0 else n * 3 + 1
        if n == start:
            counter += 1
        elif n == 1:
            break

print(counter)
