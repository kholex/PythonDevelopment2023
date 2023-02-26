from random import choice
import argparse
from urllib import request as urlreq, error as urlerr

def bullscows(guess: str, secret: str) -> (int, int):
    bulls, cows = 0, 0
    cows =  len(set(guess).intersection(set(secret)))
    for i, j in zip(list(guess), list(secret)):
        bulls += i == j

    return bulls, cows

def ask(prompt: str, valid: list[str] = None) -> str:
    while True:
        print(prompt)
        word = input()
        if valid is None or word in valid:
            return word

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    sec_word = choice(words)
    while True:
        word = ask("Введите слово: ", words)
        bulls, cows = bullscows(word, sec_word)
        inform("Быки: {}, Коровы: {}", bulls, cows)
        if word == sec_word:
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dict', help='Dictionary for game!', type=str, action='store')
    parser.add_argument('len', help='Length of words in game!', type=int, action='store', default=5, nargs='?')
    args = parser.parse_args()

    try:
        url = urlreq.urlopen(args.dict)
        words_dict = url.read().decode('utf-8').split()
    except Exception:
        try:
            file = open(args.dict, 'r');
            words_dict = file.read().split()
        except Exception:
            print('Wrong url or path to dictionary {}'.format(args.dict))

    words = [x for x in words_dict if len(x) == args.len]
    gameplay(ask, inform, words)

