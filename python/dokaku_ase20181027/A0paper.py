#!/bin/python
# this code tested Python3.6+
import sys
"""
問題：A0-An の用紙があります。
用紙のレイアウトは 縦:横=1:√2 で、
A1 ２枚を合わせると丁度 A0 となり、同様に A2 の用紙２枚を合わせると A1 となります。
この時、各 An の枚数を格納したリストを引数に、A0 用紙が生成できるかどうかを判定する、
  canBuild(list)
関数を作成しなさい。
"""


class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    末尾再帰最適化デコレータ.
    末尾再帰の条件を満たす関数にこのデコレータを指定すると、再帰のスタック階層が減る。
    末尾再帰最適化については調べるヨロシ
    """
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back \
                and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func


@tail_call_optimized
def calc_sum(res, denom, remain):
    """再帰しながら、合計値が 1 を超えるかどうか判定する.

    Arguments:
        res {number} -- 現在のペーパー合計サイズ
        denom {int} -- denominator(分母)値、ループごとに倍加する
        remain {list} -- 残りのペーパー

    Returns:
        bool -- 合計が 1 を超えるなら True それ以外は False
    """
    if len(remain) == 0:  # これ以上評価する紙はない
        return False

    head, *tail = remain  # 先頭 1 要素と、後ろを分離
    res += head / denom  # 先頭を分母で割って足す

    if res >= 1.0:
        return True

    return calc_sum(res, denom * 2, tail)


def canBuild(papers):
    """A0 用紙が作成できるかどうかの判定.

    Arguments:
        papers {list} -- int で各用紙の枚数が入るリスト

    Returns:
        [bool] -- A0 用紙が作れれば True それ以外で False
    """
    return calc_sum(0, 1, papers)


# これがペーパーリスト(引数で設定してもいい)
test_list = [
    0, 1, 0, 0, 0, 0, 0, 3, 2, 0,
    0, 5, 0, 3, 0, 0, 1, 0, 0, 0, 5
]

if canBuild(test_list):
    print('Possible')
else:
    print('Impossible')
