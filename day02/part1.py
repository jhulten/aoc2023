# Initial template from asottile
import argparse
from typing import Any
from typing import Dict
from typing import List

import pytest


def compute(s: str) -> int:
    entries = parse(s)
    return len(list(filter(validate, entries)))


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc\n", 2),
    ),
)
def test_compute(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def validate(passwords: Dict[str, Any]) -> bool:
    count = passwords['password'].count(passwords['letter'])
    return count >= passwords['min'] and count <= passwords['max']


@pytest.mark.parametrize(
    ("input_d", "expected"),
    (
        ({"min": 1, "max": 3, "letter": "a", "password": "abcde"}, True),
        ({"min": 1, "max": 3, "letter": "b", "password": "cdefg"}, False),
        ({"min": 2, "max": 9, "letter": "c", "password": "ccccccccc"}, True),
    )
)
def test_validate(input_d: Dict[str, Any], expected: bool) -> None:
    assert validate(input_d) == expected


def parse(input_s: str) -> List[Dict[str, Any]]:
    input = input_s.splitlines()
    out = []
    for i in input:
        (minmax, letter, password) = i.split(' ')
        (min, max) = minmax.split("-")
        letter = letter.replace(":", "")
        out.append({"min": int(min), "max": int(max),
                    "letter": letter, "password": password})
    return out


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc\n",
         [
             {"min": 1, "max": 3, "letter": "a", "password": "abcde"},
             {"min": 1, "max": 3, "letter": "b", "password": "cdefg"},
             {"min": 2, "max": 9, "letter": "c", "password": "ccccccccc"},
         ]
         ),
    ),
)
def test_parse(input_s: str, expected: List[Dict[str, Any]]) -> None:
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
