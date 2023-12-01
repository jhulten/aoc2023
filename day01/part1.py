# Initial template from asottile
from __future__ import annotations

import argparse
import re

import pytest


def compute(s: str) -> int:
    total = 0
    s = s.strip()
    s = re.sub(r'[^0-9\n]', '', s)
    lines = s.splitlines()
    for line in lines:
        number = int(f"{line[0]}{line[-1]}")
        total += number
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
        ('1abc2', 12),
        ('pqr3stu8vwx', 38),
        ('a1b2c3d4e5f', 15),
        ('treb7uchet', 77),
        ('1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet\n', 142)
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
