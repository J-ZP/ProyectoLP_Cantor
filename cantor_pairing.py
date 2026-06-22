import math


def pi(x, y):
    return (x + y) * (x + y + 1) // 2 + y


def unpi(z):
    w = (math.isqrt(8*z + 1) - 1) // 2
    t = w * (w + 1) // 2
    y = z - t
    x = w - y
    return x, y


def encode_list(lst):
    if not lst:
        return 0

    if len(lst) == 1:
        return lst[0]

    return pi(lst[0], encode_list(lst[1:]))
