# Initial template from asottile
from __future__ import annotations

import argparse

import pytest


def compute(s: str) -> int:
    # TODO: implement solution here!
    return 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
        ('', 0),
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
