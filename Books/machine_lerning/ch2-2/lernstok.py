import random

data_size = 10
gen_max = 10000
seed = 7
list_size = 100


def read_teacher_data(file_name):
    """教師データファイルの読み込み.

    利用できるファイルフォーマットは以下の通り.
    ```
    [data pattern list]  [answer]
    ```
    [data pattern list] は、スペースで区切られた 10 個の 0 or 1 のリスト.
    [answer] はその結果で、これも基本的に 0 or 1 のリスト.

    example:
    ```
    1 1 1 1 1 1 1 1 1 1  0
    1 0 0 0 0 0 0 1 0 0  1
    ...
    ```

    Parameters
    ------------------
    file_name : str
        教師データソースファイル名.

    Returns
    ------------------
    list
        教師データのリスト.
        教師データは、data_pattern （前述の[data pattern]を数字リストとしたもの）と、answer を持つハッシュ.
    """
    leran_list = []
    with open(file_name, 'r', encoding='ascii') as fp:
        leran_list = [v.split() for v in fp.readlines() if len(v) > 0]

    def toInt(v):
        return [int(s) for s in v]

    def toHash(ls):
        return {'data_pattern': toInt(ls[:data_size]), 'answer': ls[data_size]}

    leran_list = [toHash(ls) for ls in leran_list]
    return leran_list


def is_match(pattern, data_patern, answer):
    """pattern が data_pattern と比較した際に、 answer の値に位置するかどうか確認する.

    Parameters
    ---------------------
    pattern : list
        0, 1 or 2 の整数を 10 件保持するリスト.
        0, 1 は完全一致, 2 はワイルドカードです.
    data_pattern : list
        0 or 1 の整数を 10 件保持するリスト.
    answer : str
        結果　0 or 1 の値.
        一致時に 1 それ以外の場合に 0 と一致すべきの判断値

    Returns
    ---------------------
    bool
        pattern が data_pattern と一致させた際に、
        answer の期待値に一致する場合は True.
    """
    point = 0
    for i in range(data_size):
        if pattern[i] == 2:
            point += 1
        elif pattern[i] == data_patern[i]:
            point += 1

    if point == data_size and answer == '1':
        return True
    elif point != data_size and answer == '0':
        return True
    return False


def calc_test_score(pattern, teacher_datas):
    """全教師データに対してパターンがどれだけ一致するのかを確認する.

    Parameters
    --------------------
    pattern
        テスト対象一致パターン
    teacher_datas
        教師データリスト

    Returns
    --------------------
    int
        計算されたスコア
    """
    score = 0
    for teracher in teacher_datas:
        if is_match(pattern, teracher['data_pattern'], teracher['answer']):
            score += 1
    return score


if __name__ == '__main__':

    random.seed(seed)
    teacher_datas = read_teacher_data('ldata.txt')
    list_size = len(teacher_datas)

    current_result = []
    current_score = 0

    for i in range(gen_max):

        test = [random.randint(0, 2) for n in range(data_size)]
        tmp_score = calc_test_score(test, teacher_datas)

        if tmp_score > current_score:
            current_result = test
            current_score = tmp_score

    print('Good answer: ' + str(current_result))
    print('score      : ' + str(current_score))
