# 要するにもっとも長くしりとりが続く順番を求めよ

words = [
    'Brazil', 'Croatia', 'Mexico',
    'Cameroon', 'Spain', 'Netherlands',
    'Chile', 'Australia', 'Colombia',
    'Greece', 'Cort d\'Ivoire', 'Japan',
    'Uruguay', 'Costa Rica', 'England',
    'Italy', 'Switzerland', 'Equador',
    'France', 'Honduras', 'Argentina',
    'Bosnia and Harzegovina', 'Iran', 'Nigeria',
    'Germany', 'Portugal', 'Ghana',
    'USA', 'Belgium', 'Algeria',
    'Russia', 'Korea Republic'
]

longst_chain = []


def chain(word: str, current_chain: list, usables: list):
    global longst_chain
    current_chain.append(word)
    print(f'Start: {current_chain[0]}, List: {current_chain}')
    #print(f'  Usables: {usables}')
    #input()

    if len(current_chain) > len(longst_chain):
        longst_chain = current_chain[:]

    for next_word in usables:
        if word[-1] != next_word[0]:
            #print(f'Skip {word}, {next_word}')
            continue

        pos = usables.index(next_word)
        arg_words = usables[:]
        arg_words.pop(pos)
        chain(next_word, current_chain[:], arg_words)


if __name__ == "__main__":
    upper_words = [v.upper() for v in words]
    for word in upper_words:
        pos = upper_words.index(word)
        arg_words = upper_words[:]
        arg_words.pop(pos)
        chain(word, [], arg_words)
    print(f'Length: {len(longst_chain)}, List: {longst_chain}')
