# 年月日を 20181123 みたいな数字にして、二進数に変換して、前後反転。
# 元の年月日に戻る日付を、1964/10/10 - 2020/7/24 までで探す

from datetime import date, timedelta

current_date = date(1964, 10, 10)
end_date = date(2020, 7, 25)

while end_date > current_date:
    date_int = int(current_date.strftime('%Y%m%d'))
    str_bin = bin(date_int)[2:]
    reverse = str_bin[::-1]
    if str_bin == reverse:
        # 二進数で回文すれば同じ日付やろ
        print(current_date)
    current_date = current_date + timedelta(days = 1)

