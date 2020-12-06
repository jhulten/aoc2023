# Initial template from asottile
import argparse
from typing import List

import pytest

test_data = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""


def parse_records(s: str) -> List[str]:
    return s.split("\n\n")


def test_parse_records() -> None:
    result = parse_records(test_data)
    assert len(result) == 5


def compute(s: str) -> int:
    groups = parse_records(s)
    records = [g.split() for g in groups]
    common = [set.intersection(*[set(r2) for r2 in r1]) for r1 in records]
    counts = map(lambda x: len(x), common)
    return sum(counts)


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        # put given test cases here
        (test_data, 6),
    ),
)
def test_compute(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    exit(main())
