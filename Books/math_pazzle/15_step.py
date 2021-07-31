N=10
memo = {}


def step_count(remain: int) -> int:
    if remain < 0:
        return 0
    if remain == 0:
        return 1

    if remain in memo:
        return memo[remain]

    counter = 0
    for u in range(1, 5):
        for d in range(1, 5):
            counter += step_count(remain - (u + d))

    memo[remain] = counter
    return counter

if __name__ == "__main__":
    print(step_count(N))
