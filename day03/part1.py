# Initial template from asottile
import argparse
from typing import Tuple

import pytest

slope = (3, 1)  # right, down
start = (0, 0)

test_data = """..##.......\n#...#...#..\n.#....#..#.\n..#.#...#.#\n.#...##..#.\n..#.##.....\n.#.#.#....#\n.#........#\n#.##...#...\n#...##....#\n.#..#...#.#"""  # noqa: E501


def move(start: Tuple[int, int], map_s: str) -> Tuple[int, int]:
    width = len(map_s.splitlines()[0])
    end = tuple(map(lambda i, j: i + j, start, slope))
    end = (end[0] % width, end[1])
    return end


@ pytest.mark.parametrize(
    ("start", "map_s", "expected"),
    [
        (tuple([0, 0]), test_data, tuple([3, 1])),
        (tuple([3, 1]), test_data, tuple([6, 2])),
        (tuple([6, 2]), test_data, tuple([9, 3])),
        (tuple([9, 3]), test_data, tuple([1, 4])),
        (tuple([12, 4]), test_data, tuple([4, 5])),
    ]
)
def test_move(start: Tuple[int, int], map_s: str,
              expected: Tuple[int, int]) -> None:

    assert move(start, map_s) == expected


def is_tree(loc: Tuple[int, int], map_s: str) -> bool:
    grid = list(map(lambda x: list(x), map_s.splitlines()))
    return grid[loc[1]][loc[0]] == '#'


@ pytest.mark.parametrize(
    ("loc", "map_s", "expected"),
    [
        (tuple([0, 0]), test_data, False),
        (tuple([2, 0]), test_data, True),
    ],
)
def test_is_tree(loc: Tuple[int, int], map_s: str, expected: bool) -> None:
    assert is_tree(loc, map_s) == expected


def compute(s: str) -> int:
    path = []
    loc = start

    try:
        while True:
            path.append(is_tree(loc, s))
            loc = move(loc, s)
    except IndexError:
        pass

    return len(list(filter(lambda x: x, path)))


@ pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        # put given test cases here
        (test_data, 7),
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
