# 少年 20 人、少女 10 人が並んでいて、任意の場所で 2 グループに割る。
# この時、各グループで少年少女の人数が釣り合ってはならないとする。
# 並び方は何通り存在するか？

boy, girl = (20 + 1, 10 + 1)

# ヒントに従い、二次元マップとして考える。
# で、座標の一番終端(男子、女子が並び切った座標)に至る道順をカウントする。
# 例えば
#
# 1
# 1 2 X
# 1 1 1
#
# この X に至るルート数は、←と↓の合計になる。
# ヒントとして、男女の釣り合う状況というのは
#
# O O O X O
# O O X O O
# O X O O O
# O O O O O
#
# のように、X 座標 == Y 座標で強制的に 0 となる（到達禁止なので）
# これは座標の後ろからも同じことが言える。
map = [[0 for f in range(girl)] for m in range(boy)]
map[0][0] = 1

for f in range(girl):
    for m in range(boy):
        left = 0
        bottom = 0

        if m > 0:
            left = map[m - 1][f]
        if f > 0:
            bottom = map[m][f - 1]

        # 先頭グループが釣り合うケースはカウントしない
        # もしくは、後半グループが釣り合うケースでもカウントしない
        if m == f or (boy - m == girl - f):
            left = 0
            bottom = 0

        map[m][f] = map[m][f] + left + bottom

# どういうマップになっているのかの確認用
#for line in map:
#    print([format(v, "6d") for v in line])

print(map[19][10])
