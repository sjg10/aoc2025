def find_password(lines):
    """
    Calcukate both password modes from an iterable of lines
    """
    current_ctr = 50
    pw1 = 0
    pw2 = 0
    for l in lines:
        mul = 1 if l[0] == "R" else -1
        current_ctr += mul * int(l[1:].strip())
        pw2 += abs(current_ctr // 100)
        current_ctr %= 100
        if current_ctr == 0:
            pw1 += 1
    return pw1, pw2


def run(fs):
    return find_password(fs)
