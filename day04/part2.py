# Initial template from asottile
import argparse
import re
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

invalid_data = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

valid_data = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
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


def safe_int(x: str) -> int: return 0 if x is None else int(x)


validations = {
    "byr": lambda x: re.fullmatch(r'[0-9]{4}', x) is not None
    and 2002 >= safe_int(x) >= 1920,
    "iyr": lambda x: re.fullmatch(r'[0-9]{4}', x) is not None
    and 2020 >= safe_int(x) >= 2010,
    "eyr": lambda x: re.fullmatch(r'[0-9]{4}', x) is not None
    and 2030 >= safe_int(x) >= 2020,
    "hgt": lambda x:
        re.fullmatch(r'(([0-9]{2})in|([0-9]{3})cm)', x) is not None and
        (
            (59 <= safe_int(re.fullmatch(
                r'(([0-9]{2})in|([0-9]{3})cm)', x)[2]) <= 76)  # type: ignore
            or
            (150 <= safe_int(re.fullmatch(
                r'(([0-9]{2})in|([0-9]{3})cm)', x)[3]) <= 193)  # type: ignore
    ),
    "hcl": lambda x: re.fullmatch(r'#[0-9a-f]{6}', x) is not None,
    "ecl": lambda x:
        re.fullmatch(r'(amb|blu|brn|gry|grn|hzl|oth)', x) is not None,
    "pid": lambda x: re.fullmatch(r'[0-9]{9}', x) is not None,
    "cid": lambda x: True,
}


@pytest.mark.parametrize(
    ("k", "v", "expected"),
    (
        ("byr", "1920", True),
        ("byr", "1919", False),
        ("byr", "2002", True),
        ("byr", "2003", False),
        ("byr", "foo", False),
        ("iyr", "2010", True),
        ("iyr", "2009", False),
        ("iyr", "2020", True),
        ("iyr", "2021", False),
        ("iyr", "foo", False),
        ("eyr", "2020", True),
        ("eyr", "2013", False),
        ("eyr", "2030", True),
        ("eyr", "2031", False),
        ("eyr", "foo", False),
        ("hgt", "150cm", True),
        ("hgt", "149cm", False),
        ("hgt", "193cm", True),
        ("hgt", "194cm", False),
        ("hgt", "22foo", False),
        ("hcl", "#123abc", True),
        ("hcl", "#123zyx", False),
        ("hcl", "123abc", False),
        ("ecl", "brn", True),
        ("ecl", "wat", False),
        ("pid", "000000001", True),
        ("pid", "0123456789", False),
    )
)
def test_validations(k: str, v: str, expected: bool) -> None:
    assert validations[k](v) == expected


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
    for raw_passport in parse_records(s):
        passport = parse_field(raw_passport)
        missing = set(fields) - set(passport.keys())
        if len(missing) > 0:
            if {"cid"} != missing:
                continue
        if all(validations[k](v) for (k, v) in passport.items()):
            result += 1
    return result


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (valid_data, 4),
        (invalid_data, 0),
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
