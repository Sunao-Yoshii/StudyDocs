# !/bin/python
# this code tested Python3.6+
# 使い方:
#   python maze_yoshii.py < maze.txt
"""
問題:
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

answers = []  # 答えを格納するバッファ
moves = []  # テンポラリ移動バッファ
start_pos = (0, 0)  # スタート地点座標
goal_pos = (0, 0)  # ゴール地点座標


START_SIG = 'S'
GOAL_SIG = 'G'
ROAD_SIG = '.'
WALL_SIG = '#'


def input_maze():
    """迷路をファイルから読み込み、maze に突っ込みます。"""
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
    """迷路上から、指定の記号を含む座標を取得します。"""
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
    """
    current_pos から、move_log で移動していない道で、進める道の座標を取得する。
    """
    x, y = current_pos
    movable = []
    if x - 1 >= 0 and (x - 1, y) not in move_log \
            and maze[y][x - 1] != WALL_SIG:
        movable.append((x - 1, y))
    if y - 1 >= 0 and (x, y - 1) not in move_log \
            and maze[y - 1][x] != WALL_SIG:
        movable.append((x, y - 1))
    if x + 1 < maze_width and (x + 1, y) not in move_log \
            and maze[y][x + 1] != WALL_SIG:
        movable.append((x + 1, y))
    if y + 1 < maze_height and (x, y + 1) not in move_log \
            and maze[y + 1][x] != WALL_SIG:
        movable.append((x, y + 1))
    return movable


def move(current_pos, move_log):
    """再起しながら移動可能な全ルートで探索（全幅探索）する。"""
    # 最初に移動を確定
    move_log.append(current_pos)

    # 終了条件
    if current_pos == goal_pos:
        answers.append(move_log[:])  # ゴールに到達したら、答えバッファに格納して
        move_log.pop()  # 末尾除去
        return

    # 次に移動できる場所を探して移動してみる
    for npos in next_movable(current_pos, move_log):
        move(npos, move_log)

    # 移動検証が終われば末尾除去して終了
    move_log.pop()


if __name__ == '__main__':
    input_maze()
    start_pos = find_pos('S')
    goal_pos = find_pos('G')

    move(start_pos, moves)  # 初期位置と、移動経路を引数にセット

    print(answers)

    steps = [len(route) for route in answers]  # ゴールまでのステップ数
    min_step = min(steps)  # 最も短いステップ数を取得
    index = steps.index(min_step)  # そのインデックスを拾い
    min_route = answers[index]  # 最小ステップルートを取得

    print(f'Min step count: {min_step}')
    print(f'Min step route: {min_route}')
