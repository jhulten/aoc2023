# Initial template from asottile
from __future__ import annotations

import argparse

import pytest

# only 12 red cubes, 13 green cubes, and 14 blue cubes
MAX_RGB = (12, 13, 14)

# f any(x > y for x, y in zip(rgb, MAX_RGB)):


def compute(s: str) -> int:
    total = 0
    for line in s.strip().splitlines():
        ok = True
        game_str, samples = line.split(':')
        game_id = int(game_str.split()[1])
        print(f'Game {game_id}')
        for sample in samples.split(';'):
            r, g, b = 0, 0, 0
            print(sample)
            for color in sample.split(','):
                qty, color = color.strip().split()
                if color == 'red':
                    r = int(qty)
                elif color == 'green':
                    g = int(qty)
                elif color == 'blue':
                    b = int(qty)
                else:
                    raise ValueError(f'Unknown color: {color}')
            rgb = (r, g, b)
            print(rgb)
            if any(x > y for x, y in zip(rgb, MAX_RGB)):
                ok = False
                break  # no need to check other samples
        if ok:
            total += game_id

    return total


TEST_INPUT = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
        (TEST_INPUT, 8),
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
