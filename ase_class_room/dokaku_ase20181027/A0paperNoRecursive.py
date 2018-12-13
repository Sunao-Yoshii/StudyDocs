#!/bin/python
# this code tested Python3.6+
"""
問題：A0-An の用紙があります。
用紙のレイアウトは 縦:横=1:√2 で、
A1 ２枚を合わせると丁度 A0 となり、同様に A2 の用紙２枚を合わせると A1 となります。
この時、各 An の枚数を格納したリストを引数に、A0 用紙が生成できるかどうかを判定する、
  canBuild(list)
関数を作成しなさい。
"""


def canBuild(papers):
    """A0 用紙が作成できるかどうかの判定.
    再帰を使わないパターン

    Arguments:
        papers {list} -- int で各用紙の枚数が入るリスト

    Returns:
        [bool] -- A0 用紙が作れれば True それ以外で False
    """
    sum_v = 0
    border = 1
    for n in papers:
        sum_v += n
        if sum_v >= border:
            return True
        else:
            sum_v *= 2
            border *= 2
    return False


# これがペーパーリスト(引数で設定してもいい)
test_list = [0,1,0,0,0,0,0,3,2,0,0,5,0,3,0,0,1,0,0,0,5]

if canBuild(test_list):
    print('Possible')
else:
    print('Impossible')
