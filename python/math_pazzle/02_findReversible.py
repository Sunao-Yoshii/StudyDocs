# 351 は 3 * 51 = 153 と演算子を挟むと順序を逆にできる
# 1000 - 9999 までの数字で、そんなことができる数字を探せ
if __name__ == "__main__":
    # 演算子を割り込ませる場所
    insert_pos = [
        [3, 2, 1],
        [3, 2],
        [2, 1],
        [3, 1],
        [3], [2], [1]
    ]

    # Python だと eval 使えるから余裕
    for n in range(1111, 9999):
        str_num = str(n)

        # 挿入できる箇所は限られる
        for pos in insert_pos:
            # 区切り箇所を片っ端から nums に突っ込む
            # int(XX) してやれば int(01) = 1 にしてくれる
            test = str_num[:]
            nums = []
            for i in pos:
                nums.append(str(int(test[i:])))
                test = test[:i]
            nums.append(str(int(test)))

            test = '*'.join(nums)
            calc = str(eval(test))
            if calc[::-1] == str_num:
                print(f'{str_num} : {test} = {calc}')
