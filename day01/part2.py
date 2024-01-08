# Initial template from asottile
from __future__ import annotations

import argparse
import re

import pytest

number_patterns = (
    (r'one', 'o1e'),
    (r'two', 't2o'),
    (r'three', 't3hree'),
    (r'four', 'f4ur'),
    (r'five', 'f5ve'),
    (r'six', 's6x'),
    (r'seven', 's7ven'),
    (r'eight', 'e8ght'),
    (r'nine', 'n9ne'),
)


def replace_words(text: str) -> str:
    for k, v in list(number_patterns):
        text = text.replace(k, v)
    return text


def compute(s: str) -> int:
    total = 0
    s = s.strip()
    s = s.lower()
    lines = s.splitlines()
    for line in lines:
        print('? ', line)
        # line = re.sub(re_match_nums, replace_numbers, line)
        line = replace_words(line)
        print('* ', line)
        line = re.sub(r'[^0-9]', '', line)
        print('** ', line)
        number = int(f'{line[0]}{line[-1]}')
        print('*** ', number)
        total += number
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
        ('1abc2', 12),
        ('onetwo', 12),
        ('onetwothree', 13),
        ('one1one', 11),
        ('threefour', 34),
        ('fivesix', 56),
        ('seveneight', 78),
        ('ninezero', 99),
        ('one1two2three3', 13),
        ('pqr3stu8vwx', 38),
        ('a1b2c3d4e5f', 15),
        ('treb7uchet', 77),
        ('two1nine', 29),
        ('eightwothree', 83),
        ('abcone2threexyz', 13),
        ('xtwone3four', 24),
        ('4nineeightseven2', 42),
        ('zoneight234', 14),
        ('7pqrstsixteen', 76),
        ('7pqrstsiXteen', 76),
        (
            'two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen\n',  # noqa
            281,
        ),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
