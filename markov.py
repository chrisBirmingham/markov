#!/usr/bin/env python3

__version__ = '1.0.0'

import argparse
import base64
import collections
import os
import pickle
import random
import sys

END_OF_SENTENCE = ['.', '!', '?']
FROM_STDIN = '-'


class FileCache:
    def __init__(self):
        self._cache_dir = self._get_cache_dir()

    def _get_cache_dir(self) -> str:
        if os.environ.get('XDG_CACHE_HOME', False):
            return os.path.join(os.environ.get('XDG_CACHE_HOME'), 'markov')

        if os.environ.get('HOME', False):
            return os.path.join(os.environ.get('HOME'), '.cache', 'markov')

        return os.path.join(os.path.expanduser('~'), '.cache', 'markov')

    def _check_cache(self, input_file: str, cache_file: str) -> bool:
        if not os.path.exists(self._cache_dir):
            os.mkdir(self._cache_dir)
            return False

        if not os.path.exists(cache_file):
            return False

        return os.path.getmtime(cache_file) > os.path.getmtime(input_file)

    def _get_cache_file(self, key: str) -> str:
        cache_file = base64.b64encode(key.encode()).decode('UTF-8')
        return os.path.join(self._cache_dir, cache_file)

    def get(self, key: str) -> collections.defaultdict | bool:
        cache_file = self._get_cache_file(key)

        if not self._check_cache(key, cache_file):
            return False

        with open(cache_file, 'rb') as file:
            return pickle.load(file)

    def set(self, key: str, value: collections.defaultdict) -> None:
        cache_file = self._get_cache_file(key)
        with open(cache_file, 'wb') as file:
            pickle.dump(value, file)


def parse_input(content: str) -> collections.defaultdict:
    words = collections.defaultdict(list)
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


def generate_chain(words: collections.defaultdict) -> str:
    capital_datums = [k for k in words if k[0][:1].isupper()]
    w1, w2 = random.choice(capital_datums if len(capital_datums) > 0 else list(words.keys()))

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
    return text[slice(0, i + 1)] if i > 0 else text


def process_file(input_file: str, paragraph_count: int) -> str:
    cache = FileCache()

    if input_file == FROM_STDIN:
        content = sys.stdin.read()
        words = parse_input(content)
    else:
        if not os.path.exists(input_file):
            print(f'Input file {input_file} does not exist or can\'t be read', file=sys.stderr)
            sys.exit(1)

        input_file = os.path.abspath(input_file)
        words = cache.get(input_file)

        if not words:
            with open(input_file, 'r', encoding='UTF-8') as file:
                words = parse_input(file.read())
                cache.set(input_file, words)

    text = [generate_chain(words) for _ in range(paragraph_count)]
    return "\n\n".join(text)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog='markov',
        description='Program to generate "readable" random text from some text input.')

    parser.add_argument(
        'input_file',
        type=str,
        help='Source file to generate random text from. Use `-` to read from stdin')

    parser.add_argument(
        '-p',
        dest='count',
        type=int,
        help='Number of paragraphs to generate',
        default=1)

    parser.add_argument(
        '-v',
        action='version',
        version=__version__)

    args = parser.parse_args()
    print(process_file(args.input_file, args.count))


if __name__ == '__main__':
    main()
