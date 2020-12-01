# Initial template from asottile
import argparse
from typing import List

import pytest


def compute(s: str) -> int:
    expenses = parse(s)
    while True:
        if len(expenses) <= 1:
            break
        (i1, *expenses) = expenses
        for i2 in expenses:
            if (2020 - i1 - i2) in expenses:
                return (2020 - i1 - i2) * i1 * i2

    return -1


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        # put given test cases here
        ("1721\n979\n366\n299\n675\n1456", 241861950),
        ("12\n13", -1)
    ),
)
def test_compute(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def parse(s: str) -> List[int]:
    return [int(i) for i in s.split("\n") if len(i) > 0]


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("", []),
        ("\n", []),
        ("1721\n979\n366\n299\n675\n1456", [1721, 979, 366, 299, 675, 1456]),
    ),
)
def test_parse(input_s: str, expected: List[int]) -> None:
    assert parse(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    exit(main())
