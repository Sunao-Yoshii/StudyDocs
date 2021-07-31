# !/bin/python
# this code tested Python3.6+
# 使い方:
#   python maze_yoshii.py < maze.txt
import random
"""
問題:別解。趣味に走ったアリコロニー最適化法。
maze.txt で示した迷路の、最短経路を検索するプログラムを作成してください。
迷路は四角のマップで、記号は以下の通りです。
# : 壁
. : 通路
S : 開始地点
G : ゴール地点
"""

maze = []  # 迷路データ
maze_width = 0  # 迷路幅
maze_height = 0  # 迷路の高さ

start_pos = (0, 0)  # スタート地点座標
goal_pos = (0, 0)  # ゴール地点座標


START_SIG = 'S'
GOAL_SIG = 'G'
ROAD_SIG = '.'
WALL_SIG = '#'


def input_maze():
    first_line = list(input())
    maze.append(first_line)
    global maze_width
    global maze_height
    maze_width = len(first_line)
    maze_height = 1
    
    read_next = input()
    
    while read_next and len(read_next) == maze_width:
        maze_height += 1
        maze.append(list(read_next))
        read_next = input()


def find_pos(marker):
    X = 0
    Y = 0
    for line in maze:
        for col in line:
            if col == marker:
                return (X, Y)
            X += 1
        X = 0
        Y += 1
    return (-1, -1)  # ない筈だが、見つからなかった場合


def next_movable(current_pos, move_log):
    x, y = current_pos
    movable = []
    if x - 1 >= 0 and (x - 1, y) not in move_log and maze[y][x - 1] != WALL_SIG:
        movable.append((x - 1, y))
    if y - 1 >= 0 and (x, y - 1) not in move_log and maze[y - 1][x] != WALL_SIG:
        movable.append((x, y - 1))
    if x + 1 < maze_width and (x + 1, y) not in move_log and maze[y][x + 1] != WALL_SIG:
        movable.append((x + 1, y))
    if y + 1 < maze_height and (x, y + 1) not in move_log and maze[y + 1][x] != WALL_SIG:
        movable.append((x, y + 1))
    return movable


NUM_ANTS = 10  # 蟻の数
ILIMIT = 50  # ループ検証回数
Q = 3  # フェロモン更新定数
RHO = 0.9  # 蒸発定数
EPSILON = 0.15  # ランダム行動定数
SEED = 35  # ランダムシード
pheromone = {}  # フェロモン値
is_debug = False


def get_pheromone(pheromone, x, y):
    if (x, y) in pheromone:
        return pheromone[(x, y)]
    else:
        return 0


def find_max_indexes(ph):
    i = 0
    indexes = []
    max_p = max(ph)
    for v in ph:
        if v == max_p:
            indexes.append(i)
        i += 1
    return indexes


def ant_move(maze_map, pheromone, answer, current_pos, move_log, e = EPSILON):
    """蟻を1匹歩かせて、その結果のルートを answer に詰める。行き止まりに着いたら何もしない"""
    move_log.append(current_pos)
    if is_debug:
        print(move_log)

    # ゴールに辿りついてたら、そのルートを記録
    if current_pos == goal_pos:
        if is_debug:
            print('End ans GOAL')
        answer.append(move_log[:])
        return

    # ゴールまで行って無いなら動けるルートを探す
    moveable = next_movable(current_pos, move_log)

    if len(moveable) == 0:
        # もう移動できない、積んだ積んだー
        if is_debug:
            print('End ans NO More move')
        return
    elif len(moveable) == 1:
        # 行先一つしかないなら計算しない
        ant_move(maze_map, pheromone, answer, moveable[0], move_log, e)
        return

    # アルゴリズム的な挙動
    if random.random() <= e:
        # EPSILON 確立以下で、ランダム行動
        if is_debug:
            print('Random')
        moves_to = moveable[random.randint(0, len(moveable) - 1)]
        ant_move(maze_map, pheromone, answer, moves_to, move_log, e)
    else:
        # フェロモンの濃いルートを進む
        max_m = start_pos
        ph = [get_pheromone(pheromone, pos[0], pos[1]) for pos in moveable]

        # フェロモン最大値のインデックスを探して
        indexes = find_max_indexes(ph)

        if is_debug:
            print(f'Pheromone: {ph}')

        # そのインデックスで移動先を決定
        if len(indexes) == 1:
            # 一つしかないならよし
            max_m = moveable[indexes[0]]
        else:
            # 二つ以上ならランダム決定
            random_idx = random.randint(0, len(indexes) - 1)
            max_m = moveable[indexes[random_idx]]
        # 移動先が決まれば移動
        if is_debug:
            print('Pheromone move')
        ant_move(maze_map, pheromone, answer, max_m, move_log, e)


def wark(maze_map, pheromone):
    """蟻 NUM_ANTS 匹を歩かせて、ゴールにたどり着いた蟻のルートを返す"""
    answers = []
    for _ in range(NUM_ANTS):
        ant_move(maze_map, pheromone, answers, start_pos, [])
    return answers


def update_pheromone(pheromone, answers):
    """フェロモンマップの濃度を更新する"""
    # 既存のフェロモン蒸発
    for key in pheromone:
        pheromone[key] = pheromone[key] * RHO

    # フェロモンの上塗り
    for route in answers:  # ゴールまでの全ルート取得
        # 移動距離の 2 乗に反比例する形で新規のフェロモン濃度を算出
        lm = len(route)
        p = Q * (1.0 / (lm * lm))
        # ルート上にフェロモンを塗る
        for pos in route:  # ルート中の座標に上塗り
            pheromone[pos] = get_pheromone(pheromone, pos[0], pos[1]) + p


if __name__ == '__main__':
    input_maze()
    start_pos = find_pos('S')
    goal_pos = find_pos('G')

    random.seed(SEED)  # ランダムシード初期化
    for i in range(ILIMIT):  # ループしながら
        ans = wark(maze, pheromone)  # 歩かせる
        update_pheromone(pheromone, ans)  # フェロモン更新
        print("--pheromone--")
        print(pheromone)

    # で結局答えはどうなってんの？
    ans = []
    is_debug = True
    ant_move(maze, pheromone, [], start_pos, ans, 0)
    print(ans)
