from ..days.day9 import RectFinder


def test_part1_2():
    l = ["7,1", "11,1", "11,7", "9,7", "9,5", "2,5", "2,3", "7,3"]
    rf = RectFinder(l)
    assert rf.p1() == 50
    assert rf.p2() == 24
