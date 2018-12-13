# 10 以上の数字で、2,8,10 進数表記で回文になるものを捜す。

def is_palindrome(v):
    bin_str = bin(v)[2:]
    oct_str = oct(v)[2:]
    dig_str = str(v)
    return bin_str == bin_str[::-1] and \
        oct_str == oct_str[::-1] and \
        dig_str == dig_str[::-1]


if __name__ == "__main__":
    tmp = 11
    while not is_palindrome(tmp):
        tmp += 2
    print(f'{tmp}, {bin(tmp)}, {oct(tmp)}')
