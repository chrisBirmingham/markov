#!/usr/bin/env python3

__version__ = '1.0.0'

import argparse
import collections
import os
import pickle
import random

END_OF_SENTENCE = ['.', '!', '?']


def get_cache_dir() -> str:
    if os.environ.get('XDG_CACHE_HOME', False):
        return os.path.join(os.environ.get('XDG_CACHE_HOME'), 'markov')

    if os.environ.get('HOME', False):
        return os.path.join(os.environ.get('HOME'), '.cache', 'markov')

    return os.path.join(os.path.expanduser('~'), '.cache', 'markov')


def check_cache(input_file: str) -> bool:
    cache_dir = get_cache_dir()
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
        return False

    cache_file = os.path.join(cache_dir, input_file)

    if not os.path.exists(cache_file):
        return False

    return os.path.getmtime(cache_file) > os.path.getmtime(input_file)


def read_cache(input_file: str) -> collections.defaultdict:
    path = os.path.join(get_cache_dir(), input_file)
    with open(path, 'rb') as file:
        return pickle.load(file)


def write_cache(input_file: str, words: collections.defaultdict) -> None:
    path = os.path.join(get_cache_dir(), input_file)
    with open(path, 'wb') as file:
        pickle.dump(words, file)


def result_cacher(func):
    def wrapper(input_file: str):
        if check_cache(input_file):
            return read_cache(input_file)

        val = func(input_file)
        write_cache(input_file, val)
        return val

    return wrapper


@result_cacher
def parse_input(input_file: str) -> collections.defaultdict:
    words = collections.defaultdict(list)

    with open(input_file, 'r', encoding='UTF-8') as file:
        content = file.read()

    w1 = w2 = ''
    for word in content.split():
        words[w1, w2].append(word)
        w1, w2 = w2, word

    words[w1, w2].append('')
    words[w2, ''].append('')

    return words


def is_end_of_sentence(word: str) -> bool:
    if len(word) == 0:
        return False

    return word[-1] in END_OF_SENTENCE


def get_end_of_sentence(text: str) -> int:
    i = -1
    for c in END_OF_SENTENCE:
        search = text.rfind(c)
        if search > i:
            i = search

    return i


def generate_chain(words: collections.defaultdict) -> None:
    w1, w2 = random.choice([k for k in words if k[0][:1].isupper()])

    chain = [w1, w2]

    length = random.randrange(50, 100)
    for _ in range(length):
        last_word = (w1, w2)

        word = random.choice(words[last_word]) if last_word in words.keys() else ''

        if is_end_of_sentence(w2):
            word = word.title()

        chain.append(word)
        w1, w2 = w2, word

    text = ' '.join(chain)

    i = get_end_of_sentence(text)
    print(text[slice(0, i + 1)])


def main() -> None:
    parser = argparse.ArgumentParser(prog='markov',
                                     description='Program to generate "readable" random text from some text input')
    parser.add_argument('input_file',
                        type=str,
                        help='Source file to generate random text from')
    args = parser.parse_args()

    input_file = args.input_file
    words = parse_input(input_file)
    generate_chain(words)


if __name__ == '__main__':
    main()
