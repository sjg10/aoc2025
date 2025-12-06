from ..days.day6 import do_homework


def test_part1_2():
    l = ["123 328  51 64 ", " 45 64  387 23 ", "  6 98  215 314", "*   +   *   +  "]
    res = do_homework(l)
    # assert res[0] == 4277556
    assert res[1] == 3263827
