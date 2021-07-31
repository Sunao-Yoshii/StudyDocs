import itertools
import functools


def prime_generator():
    stream = itertools.count(2)

    def sieve(x, y): return x % y != 0

    while True:
        prime = next(stream)
        stream = filter(functools.partial(sieve, y=prime), stream)
        yield prime


if __name__ == "__main__":
    prime_gen = prime_generator()
    prime_nums = [next(prime_gen) for _ in range(6)]
    min_value = prime_nums[-1] ** 2
    min_datas = []

    for prime in itertools.permutations(prime_nums):
        friends = []

        # Head/Tail
        head = prime[0]
        tail = prime[-1]

        # Calc head*head, head*(head+1)...(tail-1)*tail
        for n in prime:
            friends.append(head * n)
            head = n

        # tail
        friends = friends + [tail**2]

        # update current result
        if min_value > max(friends):
            min_value = max(friends)
            min_datas = friends

    print(f'Minimum: {min_value} at Datas: {min_datas}')
