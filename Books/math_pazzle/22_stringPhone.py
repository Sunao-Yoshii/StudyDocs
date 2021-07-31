

def string_phone(N: int) -> int:
    def pair(n: int, indent: str) -> int:
        #print(f'{indent}pair({n})')
        if n < 2:
            return 1
        ans = 0
        for i in range(1, n, 2):
            ans += pair(i-1, indent + '  ') * pair(n - i - 1, indent + '  ')
        return ans
    return pair(N, '')


print(string_phone(16))
