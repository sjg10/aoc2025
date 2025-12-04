from ..days.day4 import PaperMap


def test_part1_2():
    l = [
        "..@@.@@@@.",
        "@@@.@.@.@@",
        "@@@@@.@.@@",
        "@.@@@@..@.",
        "@@.@@@@.@@",
        ".@@@@@@@.@",
        ".@.@.@.@@@",
        "@.@@@.@@@@",
        ".@@@@@@@@.",
        "@.@.@@@.@.",
    ]
    pm = PaperMap(l)
    assert pm.get_4_nbors() == 13
    assert pm.get_total_removed() == 43
