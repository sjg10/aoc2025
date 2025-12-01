from ..days.day1 import find_password


def test_part1_2():
    l = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]
    res = find_password(l)
    assert res[0] == 3
    assert res[1] == 6
