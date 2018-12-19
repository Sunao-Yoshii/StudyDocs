# 1-100 までの裏返しのカードが裏返しの状態で並んでます
# 2 枚目から 1 枚おき（+2枚目）に最後まで裏返します。
# 次は 3 枚目から 2 枚おき(+3枚目)に最後まで…
# 繰り返したとき裏のままの番号を答えましょう

open_cards = [False for n in range(100)]

for step in range(2, 100):
    index = step - 1
    while index < 100:
        open_cards[index] = not open_cards[index]
        index += step

index = 0
close_indexes = []
for is_opened in open_cards:
    index += 1
    if not is_opened:
        close_indexes.append(index)

print(close_indexes)
