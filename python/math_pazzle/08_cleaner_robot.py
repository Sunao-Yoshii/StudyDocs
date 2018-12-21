# 前後左右に移動できるロボットが、12 回移動したら、移動パターンは何通りありえるか？
# ただし、一度でも移動した場所は二度と通れないものとする。

def count_move(log, max_move):
    if len(log) == max_move + 1:
        return 1

    patterns = 0
    for move_to in [(0,1), (1,0), (0, -1), (-1, 0)]:
        x, y = log[-1]
        x += move_to[0]
        y += move_to[1]
        position = (x, y)
        if position in log:
            continue
        else:
            nlog = log[:]
            nlog.append(position)
            patterns += count_move(nlog, max_move)
    return patterns

print(count_move([(0, 0)], 12))
