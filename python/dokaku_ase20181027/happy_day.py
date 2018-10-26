#!/bin/python
# Python 3.6+ で動作します。
# 2015 年の中で 4/22 : 4 = 2 + 2 の様な日付を探します

import datetime

current_date = datetime.date(2015, 1, 1)
end_date = datetime.date(2016, 1, 1)
a_day_duration = datetime.timedelta(days=1)


def is_happy_day(date):
    m = date.month
    d = date.day
    if d < 10:
        return m == d
    else:
        str_d = str(d)
        s = int(str_d[0]) + int(str_d[1])
        return m == s


if __name__ == '__main__':
    """
    なんてことはない、１日づつカウントアップし、
    それが要件(月 = 日の一桁目＋二桁目)を満たすか判定するだけ。
    """
    count_of_happy_day = 0
    while current_date < end_date:
        if is_happy_day(current_date):
            print(f'isHappy: {current_date}')
            count_of_happy_day += 1
        current_date = current_date + a_day_duration
    print(count_of_happy_day)