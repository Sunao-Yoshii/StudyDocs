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


LOOP_MAX = 10000  # 対戦回数は 10000 回
LERN_RATE = 0.1  # 学習レート（スコア変動）は 1 割
TEST_RATE = 0.9  # 続行時のスコア変動レート
RANDOM_RATE = 0.3  # ランダムで置き場所を決定する確率
RANDOM_SEED = 32765  # ランダム関数シード
WINNER_SCORE = 1000   # 勝利時の褒章スコア
EVEN_SCORE = 500   # 防衛時の褒章スコア
LOSE_SCORE = 0   # 負けた時のスコア


random.seed(RANDOM_SEED)

# 最初は評価値ランダムで設定
white_qvalue = [random.randint(0, 100) for i in range(9)]
black_qvalue = [random.randint(0, 100) for i in range(9)]


class LerningMachine:
    """学習機"""
    def __init__(self, pattern, color):
        """評価値テーブルと、自身の石を指定"""
        self.pattern = pattern
        self.color = color

    def __select_random(self, putable):
        """石を置ける場所の中からランダムにおける場所のインデックスを応答する"""
        counts = len([i for i in putable if i])
        selected_index = random.randint(0, counts - 1)
        for i in range(len(putable)):
            if putable[i] is False:
                continue
            selected_index -= 1
            if putable[i] and selected_index <= 0:
                return i

    def __select_max(self, qvalues):
        """評価値の最も高い場所を返す"""
        max_value = max(qvalues)
        return qvalues.index(max_value)
    
    def __filter_qvalues(self, putable):
        """置ける場所によって Q 値をフィルタしてやる"""
        qvalues = self.pattern[:]  # 評価値パターンをコピーして
        for i in range(len(qvalues)):  # 置ける場所でフィルタしてやる
            qvalues[i] = qvalues[i] if putable[i] else -1
        return qvalues

    def put(self, putable):
        """石の置ける場所を引数に、実際に石を置く場所を決める"""
        if random.random() < RANDOM_RATE:
            # ランダム行動セレクト
            return self.__select_random(putable)
        else:
            # Q 値最大をセレクト
            return self.__select_max(self.__filter_qvalues(putable))

    def __calc_qvalue(self, index, score):
        """引き分け時スコアを計算する"""
        increse_score = LERN_RATE * (score - self.pattern[index])
        return self.pattern[index] + int(increse_score)

    def updateq(self, putable, put_index, result, board):
        """Q 値を更新する"""
        if result == 0:
            # 引き分け(今石を置いてある場所にポイントを与える)
            for i in range(len(board)):
                if board[i] == self.color:
                    self.pattern[i] = self.__calc_qvalue(i, EVEN_SCORE)
        elif result is None:
            # まだ続行((置ける場所のスコアMAX*90% - 置いた場所のスコア) * 学習レート)
            qvalues = self.__filter_qvalues(putable)
            qmax = max(qvalues)
            inc_score = LERN_RATE * (TEST_RATE * qmax - self.pattern[put_index])
            self.pattern[put_index] = self.pattern[put_index] + int(inc_score)
        elif result == self.color:
            # 勝利(今石を置いてある場所にポイントを与える)
            for i in range(len(board)):
                if board[i] == self.color:
                    self.pattern[i] = self.__calc_qvalue(i, WINNER_SCORE)
        else:
            # 負けた場合(今石を置いてある場所のスコアを落とす)
            for i in range(len(board)):
                if board[i] == self.color:
                    self.pattern[i] = self.__calc_qvalue(i, LOSE_SCORE)


if __name__ == '__main__':
    print('START:')
    print(white_qvalue)
    print(black_qvalue)
    for i in range(LOOP_MAX):
        bord = TicTacToe()
        lerning_machines = [
            LerningMachine(white_qvalue, TicTacToe.WHITE),
            LerningMachine(black_qvalue, TicTacToe.BLACK)
        ]
        index = 0
        while True:
            attacker = lerning_machines[index % 2]
            putable = bord.putable()
            put_index = attacker.put(putable)
            result = bord.put(put_index, attacker.color)
            current_board = bord.bord
            if result is None:
                # 継続
                attacker.updateq(putable, put_index, None, current_board)
                index += 1
            else:
                # 決着
                lerning_machines[0].updateq(putable, put_index, result, current_board)
                lerning_machines[1].updateq(putable, put_index, result, current_board)
                # bord.display()
                break
    print('END:')
    print(white_qvalue)
    print(black_qvalue)
    
