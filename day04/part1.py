# Initial template from asottile
import argparse
from typing import Any
from typing import Dict
from typing import List

import pytest

test_data = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

fields = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    "cid",
]


def parse_records(s: str) -> List[str]:
    return s.split("\n\n")


def test_parse_records() -> None:
    result = parse_records(test_data)
    assert len(result) == 4
    assert all(map(lambda x: "eyr" in x, result))


def parse_field(rec: str) -> Dict[str, Any]:
    return dict([tuple(i.split(':')) for i in rec.split()])  # type: ignore


def test_parse_fields() -> None:
    result = parse_field(parse_records(test_data)[0])
    assert isinstance(result, dict)
    assert len(result) == 8
    assert "eyr" in result


def compute(s: str) -> int:
    result = 0
    for passport in parse_records(s):
        missing = set(fields) - set(parse_field(passport).keys())
        if (len(missing) == 0):
            result += 1
        elif (len(missing) == 1 and 'cid' in missing):
            result += 1
    return result


@ pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        # put given test cases here
        (test_data, 2),
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
