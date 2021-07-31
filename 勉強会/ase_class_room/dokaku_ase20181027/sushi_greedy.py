# !/bin/python
# this code tested Python3.6+

"""
入力:
N
V1 V2 V3 …VN

例:
4
1 2 3 4

で入力された寿司の美味しさで、
皿を取ったら、2個目は1回開けなければならないとき、
美味しさの最大となる組み合わせを探せ。
上記の例なら、2 + 4 で 6 (2 を取ったので 3 は取れない)
"""

memories = {}  # メモ化キャッシュ


def select(index, scores):
    """scores から指定のインデックス要素と、その後ろを取得する。
    ※ただし、後ろ部分に関しては、問題の定義より一つ以上空白をあける。
    """
    tail_head_index = index + 2
    head = scores[index]
    if len(scores) <= tail_head_index:
        return (head, [])
    else:
        return (head, scores[tail_head_index:])


def max_score(scores):
    """scores で渡した点数リストから、最大スコアの組み合わせを計算する。
    ただし、選択したスコアから、次のスコアを選ぶときには、
    一つ以上隙間を用意しなければならない。
    再起を組みはするが、評価を始めるのは後ろ部分から評価する。
    確か部分最適化法とかいうアルゴリズムだったはず。

    Arguments:
        scores {list} -- スコアリスト

    Returns:
        int -- そのリストから計算できる最大スコア
    """
    tupled = tuple(scores)
    if tupled in memories:
        # キャッシュ済みならキャッシュから返す
        result = memories[tupled]
        print(f'Hit: {scores} ANS: {result}')
        return result

    list_length = len(scores)
    if list_length == 1:
        # 要素が一つならその値を返す
        memories[tupled] = scores[0]
        print(f'Req: {scores} ANS: {scores[0]}')
        return scores[0]

    # 今の scores 内での最大取得可能スコアを計算
    cur_score = 0
    for i in range(0, list_length):
        # N 番目要素を順に取得して試す。
        tmp_score, tail = select(i, scores)

        # 後ろの要素があるなら、その最大スコアを加算
        if len(tail) > 0:
            tmp_score = tmp_score + max_score(tail)

        # 現在計算しているスコアが大きければ置き換える
        cur_score = tmp_score if cur_score <= tmp_score else cur_score

    # スコアをキャッシュしてリターン
    memories[tupled] = cur_score
    print(f'Req: {scores} ANS: {cur_score}')
    return cur_score


if __name__ == '__main__':
    N = int(input())  # リストサイズ
    SCORES = [int(v) for v in input().split(' ')]  # 寿司おいしさリスト
    print(max_score(SCORES))
