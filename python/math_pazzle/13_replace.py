# READ + WRITE + TALK = SKILL
# この文字列のうち、アルファベットお数字に置き換え、成立させてください。

import re
import itertools
import copy

src = 'READ + WRITE + TALK = SKILL'
num_expression = re.split('[^a-zA-Z]+', src)
unique_chars = list(set(''.join(num_expression)))
non_zero_chars = [n[0] for n in num_expression]


def is_invalid(kv: dict) -> bool:
    for c in non_zero_chars:
        if kv[c] == 0:
            return True
    return False


count = 0
for perm in itertools.permutations(range(10), len(unique_chars)):
    zipped = dict(zip(unique_chars, perm))

    if is_invalid(zipped):
        continue

    tmp_str = src
    for k in zipped.keys():
        tmp_str = tmp_str.replace(k, str(zipped[k]))

    if eval(tmp_str.replace('=', '==')):
        print(tmp_str)
        count += 1

print(count)
