from ..days.day5 import CafeteriaInventory


def test_part1_2():
    l = ["3-5", "10-14", "16-20", "12-18", "", "1", "5", "8", "11", "17", "32"]
    ci = CafeteriaInventory(l)
    assert ci.get_fresh() == 3
    assert ci.get_fresh_possible() == 14
