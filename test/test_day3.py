from ..days.day3 import find_batteries


def test_part1_2():
    l = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    res = find_batteries(l, 2)
    assert res == 357
    res = find_batteries(l, 12)
    assert res == 3121910778619
