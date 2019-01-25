from functools import lru_cache

START_COIN = 10
TURNS = 24

@lru_cache()
def current_game(game:int , coins: int) -> int:
    if game == 0:
        return 1
    if coins == 0:
        return 0
    return current_game(game - 1, coins + 1) + current_game(game - 1, coins - 1)


print(current_game(TURNS, START_COIN))
