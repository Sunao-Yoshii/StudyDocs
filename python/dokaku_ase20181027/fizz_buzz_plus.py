# !/bin/python
# this code tested Python3.6+
# Use:
#   > python gbp_yoshii.py 52
#   Buzz!
#   >
import sys
"""
問題：
3 の倍数で Fizz!
5 の倍数で Buzz!
という他、文字中に 3 や 5 があっても反応する FizzBuzz.
例えば 52 はどちらの倍数でもないが、文字中に 5 を含むので Buzz
"""


def is_match(i, n):
    if i % n == 0:
        return True
    elif str(n) in str(i):
        return True
    else:
        return False


def is_fizz(i):
    return is_match(i, 3)


def is_buzz(i):
    return is_match(i, 5)


def conv(i):
    fizz = is_fizz(i)
    buzz = is_buzz(i)
    if fizz and buzz:
        return "FizzBuzz!"
    elif fizz:
        return "Fizz!"
    elif buzz:
        return "Buzz!"
    else:
        return str(i)


if __name__ == '__main__':
    print(conv(int(sys.argv[1])))
