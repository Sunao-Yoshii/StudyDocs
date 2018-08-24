# QLern を使用して、先手後手の三目並べ評価値盤を作成する
import random


# 三目並べの碁盤＋ゲームルール定義
class TicTacToe:
    WHITE = 1
    BLACK = -1
    BLANK = 0

    """三目並べ盤"""
    def __init__(self):
        """盤を初期化"""
        self.bord = [TicTacToe.BLANK for i in range(9)]

    def __is_won(self, color):
        """指定したカラーが勝利したかどうか判定する"""
        # 横列で揃った場合
        for y in range(3):
            is_row = True
            for x in range(3):
                is_row = is_row and self.bord[y * 3 + x] == color
            if is_row:
                return True
        # 縦列で揃った場合
        for x in range(3):
            is_col = True
            for y in range(3):
                is_col = is_col and self.bord[y * 3 + x] == color
            if is_col:
                return True
        # 斜めで揃ったケース 1
        for i in range(3):
            x = i
            y = i * 3
            if self.bord[x + y] != color:
                break
            if i == 2:
                return True
        # 斜めで揃ったケース 2
        for i in range(3):
            x = 2 - i
            y = i * 3
            if self.bord[x + y] != color:
                break
            if i == 2:
                return True
        # それ以外は勝敗はついてない
        return False

    def putable(self):
        """石を置ける場所を返す"""
        return [i == TicTacToe.BLANK for i in self.bord]

    def display(self):
        """盤面を表示して見せる"""
        for y in range(3):
            st = y * 3
            print(self.bord[st:st + 3])
        print("----------")

    def put(self, index, color):
        """○/×を置く。勝敗が決すれば 1/-1 を、引き分けなら 0 続くなら None を返す"""
        self.bord[index] = color
        # 勝敗が決したなら color 応答
        if self.__is_won(color):
            return color
        # まだ置けるなら、None 応答
        if TicTacToe.BLANK in self.bord:
            return None
        # 続かないなら引き分け
        return TicTacToe.BLANK


LOOP_MAX = 10000  # 学習回数
RANDOM_SEED = 8132  # ランダム関数シード

random.seed(RANDOM_SEED)


class Quantity:
    """Q 学習機本体"""
    def __init__(self, alpha, gamma, initial_q=100):
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
            return self._initial_q

    def set(self, state, act, q_value):
        """Q 値設定"""
        self._values[(state, act)] = q_value

    def lerning(self, state, act, max_q):
        """Q 値更新"""
        pQ = self.select_q(state, act)
        new_q = pQ + int(self._alpha * (self._gamma * max_q - pQ))
        self.set(state, act, new_q)

    def add_fee(self, state, act, fee):
        """報酬を与える"""
        pQ = self.select_q(state, act)
        new_q = pQ + int(self._alpha * (fee - pQ))
        self.set(state, act, new_q)


def get_selectables(putables):
    """置ける座標リストを返す"""
    indexes = []
    for i in range(len(putables)):
        if putables[i]:
            indexes.append(i)
    return indexes


def select_random(putable):
    """石を置ける場所の中からランダムにおける場所のインデックスを応答する"""
    selectables = get_selectables(putable)
    return selectables[random.randint(0, len(selectables) - 1)]


def to_state_str(state):
    """int リストを文字列化する"""
    return '.'.join([str(i) for i in state])


class Player:
    def __init__(self, name='ランダムさん', color=TicTacToe.BLACK):
        """勝利カウントだけ持っとく"""
        self.win_count = 0
        self.name = name
        self.color = color

    def put(self, putable, current_board):
        """とりあえずランダムで置く"""
        return select_random(putable)

    def display_win_state(self):
        print(f'Player: {self.name} : WinCount: {self.win_count}')


class LerningMachine(Player):
    """学習機"""
    WINNER_SCORE = 1000   # 勝利時の褒章スコア
    EVEN_SCORE = 500   # 防衛時の褒章スコア
    LOSE_SCORE = 0   # 負けた時のスコア
    DEFAULT_ALPHA = 0.1  # 学習レート（スコア変動）は 1 割
    DEFAULT_GAMMA = 0.9  # 続行時のスコア変動レート
    DEFAULT_EPSILON = 0.3  # ランダムで置き場所を決定する確率

    def __init__(self, color, e=DEFAULT_EPSILON, alpha=DEFAULT_ALPHA, gamma=DEFAULT_GAMMA):
        """評価値テーブルと、自身の石を指定"""
        super().__init__('Q学習さん', color)
        self._q = Quantity(alpha, gamma)
        self._e = e
        self._last_move = None
        self._last_board = None
        self.is_debug = False
        self._action_count = 0

    def set_e(self, e):
        """e 値を上書き"""
        self._e = e

    def put(self, putable, current_board):
        """石の置ける場所を引数に、実際に石を置く場所を決める"""
        self._last_board = current_board[:]
        act_count = self._action_count
        self._action_count += 1

        if random.random() < (self._e / (act_count // LOOP_MAX + 1)):
            # ランダム行動セレクト
            return select_random(putable)
        else:
            # Q 値最大をセレクト
            qs = []
            selectables = get_selectables(putable)

            # Q 値テーブル作成(置ける場所限定で)
            for index in selectables:
                state = to_state_str(current_board)
                qs.append(self._q.select_q(state, index))

            # DEBUG モードなら、評価テーブルを表示する
            if self.is_debug:
                print(qs)

            # Q MAX の座標を返す
            max_q = max(qs)
            if qs.count(max_q) > 1:
                # 同値 MAX の座標がある場合
                # max_q の座標からランダム決定
                vals = [i for i in range(len(selectables)) if qs[i] == max_q]
                i = random.choice(vals)
            else:
                # MAX は一つしかない
                i = qs.index(max_q)

            # 移動先座標確定
            move_index = selectables[i]
            self._last_move = move_index
            return move_index

    def lerning(self, putable, board, result):
        """Q 値を更新する"""
        if self._last_board is None:
            return

        # 前回の状況を state にまとめる
        state = to_state_str(self._last_board)
        if result == self.color:
            # 勝利(自分のターンのみ)
            self._q.add_fee(state, self._last_move, LerningMachine.WINNER_SCORE)
            self._last_move = None
            self._last_board = None
        elif result == TicTacToe.BLANK:
            # 引き分け
            self._q.add_fee(state, self._last_move, LerningMachine.EVEN_SCORE)
            self._last_move = None
            self._last_board = None
        elif result is None:
            # 継続中
            # Q 値テーブル作成(置ける場所限定で)
            qs = []
            selectables = get_selectables(putable)
            for index in selectables:
                current = to_state_str(current_board)
                qs.append(self._q.select_q(current, index))
            # max_q 取得
            max_q = max(qs)
            self._q.lerning(state, self._last_move, max_q)
        else:
            # 負けた(最後に打った状態が既に積みだった)
            self._q.add_fee(state, self._last_move, 0)
            self._last_move = None
            self._last_board = None


if __name__ == '__main__':
    white_machine = LerningMachine(TicTacToe.WHITE)

    # Q 学習機の用意
    lerning_machines = [
        white_machine,
        LerningMachine(TicTacToe.BLACK)
    ]

    for i in range(LOOP_MAX):
        bord = TicTacToe()
        index = 0
        while True:
            attacker = lerning_machines[index % 2]
            defender = lerning_machines[1 - index % 2]
            putable = bord.putable()

            # 攻撃側は前回の一手の状況から学習する
            attacker.lerning(putable, bord.bord, None)

            # 攻撃側が石を置く
            put_index = attacker.put(putable, bord.bord)
            result = bord.put(put_index, attacker.color)
            current_board = bord.bord

            if result is None:
                # 継続
                index += 1
            else:
                # 決着
                lerning_machines[0].lerning(putable, current_board, result)
                lerning_machines[1].lerning(putable, current_board, result)
                # 学習機を入れ替え
                lerning_machines = [
                    lerning_machines[1],
                    lerning_machines[0]
                ]
                break

    # Q学習 vs ランダムさん
    players = [
        white_machine,
        Player('ランダムさん', TicTacToe.BLACK)
    ]
    white_machine.set_e(0)  # 因みに学習モードは切っておく
    white_machine.is_debug = True

    print('Battle start!')
    for i in range(1000):
        bord = TicTacToe()
        index = 0

        if i % 100 == 0:
            print(f'{i} 回時点:')
            for p in players:
                p.display_win_state()

        while True:
            attacker = players[index % 2]
            putable = bord.putable()

            # bord.display()

            # 攻撃側が石を置く
            put_index = attacker.put(putable, bord.bord)
            result = bord.put(put_index, attacker.color)

            # input()

            if result is None:
                index += 1
            else:
                # bord.display()
                # print('Game set.')
                # input()
                # 勝敗
                # 攻撃側だけがポイント
                if result == attacker.color:
                    attacker.win_count += 1
                break
        # 先攻後攻入れ替え
        players = [
            players[1],
            players[0]
        ]

    # 勝敗は？
    print('1000 回総合:')
    for p in players:
        p.display_win_state()
