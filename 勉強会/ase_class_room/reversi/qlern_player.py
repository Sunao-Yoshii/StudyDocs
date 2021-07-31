from reversi import ReversiBoard, Player
import random
import pickle

# QLern で計算してみた。
# アルゴリズムは Qlerning
# 尚、学習時には Qlerning AI に先手後手を入れ替えながら自分で戦って学習してもらった。
# つまり、1試合で先手後手両方で学習してもらう。
# 先手後手で、同じように学習できるように、Qlerning 内のデータは、自分の石 S と敵の石 E の文字列で保持するようにした。

LOOP_MAX = 20000  # 学習回数
RANDOM_SEED = 8132  # ランダム関数シード

random.seed(RANDOM_SEED)


class Quantity:
    """Q 学習機本体"""
    def __init__(self, alpha, gamma, initial_q=50.0):
        """Q 値、学習係数、伝播係数の設定"""
        self._values = {}
        self._alpha = alpha
        self._gamma = gamma
        self._initial_q = initial_q

    def select_q(self, state, act):
        """状態とアクションをキーに、q 値取得"""
        if (state, act) in self._values:
            return self._values[(state, act)]
        else:
            # Q 値が未学習の状況なら、Q 初期値
            self._values[(state, act)] = self._initial_q
            return self._initial_q

    def save(self):
        with open('qlern.pickle', mode = 'wb') as f:
            pickle.dump(self._values, f)

    def load(self):
        with open('qlern.pickle', mode = 'rb') as f:
            self._values = pickle.load(f)

    def set(self, state, act, q_value):
        """Q 値設定"""
        self._values[(state, act)] = q_value

    def lerning(self, state, act, max_q):
        """Q 値更新"""
        pQ = self.select_q(state, act)
        new_q = pQ + self._alpha * (self._gamma * (max_q - pQ))
        self.set(state, act, new_q)

    def add_fee(self, state, act, fee):
        """報酬を与える"""
        pQ = self.select_q(state, act)
        new_q = pQ + self._alpha * (fee - pQ)
        self.set(state, act, new_q)


class LerningMachine(Player):
    WINNER_SCORE = 1000.0   # 勝利時の褒章スコア
    DEFAULT_ALPHA = 0.1  # 学習レート（スコア変動）は 1 割
    DEFAULT_GAMMA = 0.9  # 続行時のスコア変動レート
    DEFAULT_EPSILON = 0.3 # ランダムで置き場所を決定する確率

    def __init__(self, board, color):
        super().__init__(board, color)
        self._turn = 0
        self._last_board = None
        self._last_attack = None
        self._q = Quantity(LerningMachine.DEFAULT_ALPHA, LerningMachine.DEFAULT_GAMMA)
        self._e = LerningMachine.DEFAULT_EPSILON

    def reset(self):
        self._last_board = None
        self._last_attack = None
        self._turn = 0

    def get_state(self):
        return (self._turn, self._color, self._last_board, self._last_attack)

    def set_state(self, state):
        self._turn = state[0]
        self._color = state[1]
        self._last_board = state[2]
        self._last_attack = state[3]

    def set_epsilon(self, v):
        self._e = v

    def lerning(self, selectables, latest_board):
        if self._last_board is None:
            return  # 初手は学習対象外
        if self._board.is_game_end():
            # ゲーム終了してるなら、勝利か敗北かでスコア加算
            if self._board.is_win(self._color):
                # 勝利してれば前回の手（状態と着手手）にスコア加算
                self._q.add_fee(self._last_board, self._last_attack, LerningMachine.WINNER_SCORE)
        else:
            # ゲーム継続中
            if len(selectables) == 0:
                # 選択不能って学習できなくね？
                # むしろこの状況は悪手
                max_q = 0
            else:
                # 選択できる手があるならそのまま学習
                qs = []
                for index in selectables:
                    # 一手先の評価値情報を取得
                    qs.append(self._q.select_q(latest_board, index))
                # 評価値の最大値を取得
                max_q = max(qs)
            # 前回の手（状態と着手手）を学習
            self._q.lerning(self._last_board, self._last_attack, max_q)

    def converted_board(self):
        cur = self._color
        enemy = ReversiBoard.STONE_BLACK
        if cur == enemy:
            enemy = ReversiBoard.STONE_WHITE
        board_str = self._board.to_string()
        return board_str.replace(cur, 'S').replace(enemy, 'E')

    def save(self):
        self._q.save()

    def load(self):
        self._q.load()

    def put(self):
        self._turn += 1
        # 既存状態の確認
        current_board = self.converted_board()
        ables = self._board.able_to_puts(self._color)

        # 学習と次の手の準備
        self.lerning(ables, current_board)
        self._last_board = current_board

        # 次が打てないと諦め
        length = len(ables)
        if length == 0:
            return

        # 次の一手
        if random.random() < self._e:
            # 一定確率でランダム行動選択
            if length == 1:
                x, y = ables[0]
                self._last_attack = ables[0]
                self._board.put_stone(self._color, x, y)
            else:
                x, y = ables[random.randint(0, len(ables) - 1)]
                self._last_attack = (x, y)
                self._board.put_stone(self._color, x, y)
        else:
            # さもなくば、評価値の最もいいものを選択
            # 評価値リスト作成
            qs = []
            for index in ables:
                qs.append(self._q.select_q(current_board, index))
            
            # 最高座標を探す
            max_q = max(qs)
            if qs.count(max_q) > 1:
                # 同値 MAX の座標がある場合
                # max_q の座標からランダム決定
                vals = [i for i in range(len(ables)) if qs[i] == max_q]
                i = random.choice(vals)
            else:
                # MAX は一つしかない
                i = qs.index(max_q)
            # 移動先座標確定
            self._last_attack = ables[i]
            x, y = self._last_attack
            self._board.put_stone(self._color, x, y)


class QPlayer(LerningMachine):
    def __init__(self, board, color):
        super().__init__(board, color)
        self.set_epsilon(0.0)
        self.load()

    def put(self):
        # 既存状態の確認
        current_board = self.converted_board()
        ables = self._board.able_to_puts(self._color)

        # 次が打てないと諦め
        length = len(ables)
        if length == 0:
            return

        # 次の一手
        # 評価値リスト作成
        qs = []
        for index in ables:
            qs.append(self._q.select_q(current_board, index))

        # 最高座標を探す
        max_q = max(qs)
        if qs.count(max_q) > 1:
            # 同値 MAX の座標がある場合
            # max_q の座標からランダム決定
            vals = [i for i in range(len(ables)) if qs[i] == max_q]
            i = random.choice(vals)
        else:
            # MAX は一つしかない
            i = qs.index(max_q)
        # 移動先座標確定
        self._last_attack = ables[i]
        x, y = self._last_attack
        self._board.put_stone(self._color, x, y)


class RandomPlayer(Player):
    def __init__(self, board, color):
        super().__init__(board, color)

    def put(self):
        putable = self._board.able_to_puts(self._color)
        if len(putable) == 0:
            return
        x, y = putable[random.randint(0, len(putable) - 1)]
        self._board.put_stone(self._color, x, y)


def lerning_at50000():
    # 50,000 回対戦して学習
    board = ReversiBoard()
    lerning = LerningMachine(board, ReversiBoard.STONE_BLACK)
    stones = [ReversiBoard.STONE_BLACK, ReversiBoard.STONE_WHITE]
    lern_loops = 0

    # 2 週目以降なら、学習の途中から再開できる
    #lerning.load()

    for n in range(50000):
        lern_loops += 1
        turn = 0
        caches = [None, None]
        board.initialize()
        color = stones[turn]
        # BattleCount
        if lern_loops % 1000 == 0:
            print(f'Lerning at {lern_loops}')
        
        lerning.reset()

        while not board.is_game_end():
            color = stones[turn % 2]
            cache = caches[turn % 2]
            if cache != None:
                lerning.set_state(cache)
            else:
                lerning.set_color(color)
            lerning.put()
            cache = lerning.get_state()
            caches[turn % 2] = cache
            turn += 1
        # 勝者確定
        cache = caches[0]
        lerning.set_state(cache)
        lerning.lerning([], lerning.converted_board())
        cache = caches[1]
        lerning.set_state(cache)
        lerning.lerning([], lerning.converted_board())
    lerning.save()


def vs_random():
    color_index = 0
    winner_p1 = 0
    winner_p2 = 0
    board = ReversiBoard()
    player1 = QPlayer(board, ReversiBoard.STONE_BLACK)
    for n in range(1000):
        board.initialize()
        is_atk_player1 = color_index % 2 == 0
        p1_color = ReversiBoard.STONE_BLACK if is_atk_player1 else ReversiBoard.STONE_WHITE
        p2_color = ReversiBoard.STONE_WHITE if is_atk_player1 else ReversiBoard.STONE_BLACK
        player1.set_color(p1_color)
        player2 = RandomPlayer(board, p2_color)
        players = [player1, player2] if is_atk_player1 else [player2, player1]

        turn = 0
        while not board.is_game_end():
            players[turn % 2].put()
            turn += 1
        winner_p1 += (1 if board.is_win(p1_color) else 0)
        winner_p2 += (1 if board.is_win(p2_color) else 0)

        color_index += 1
        if color_index % 100 == 0:
            print(f'Battle at {color_index}, {winner_p1} vs {winner_p2}')
    
    print(f'Qlern: {winner_p1}, Random: {winner_p2}, {winner_p1/1000.0}')


def vs_player():
    board = ReversiBoard()
    players = [
        QPlayer(board, ReversiBoard.STONE_BLACK),
        Player(board, ReversiBoard.STONE_WHITE),
    ]
    loop = 0
    while not board.is_game_end():
        players[loop % 2].put()
        loop += 1
    if board.is_draw():
        print('Draw game.')
    elif board.is_win(ReversiBoard.STONE_BLACK):
        print('Black win.')
    else:
        print('White win')
    board.show()


if __name__ == "__main__":
    # 学習する
    # lerning_at50000()

    # ランダムさんと 1000 回勝負
    vs_random()

    # プレイヤーとバトル
    vs_player()



