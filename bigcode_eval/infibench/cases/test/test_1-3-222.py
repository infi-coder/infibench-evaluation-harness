def f(n, k):
    return k if n == 1 else (k - 1) * (f(n - 1, k) + g(n - 1, k))

def g(n, k):
    return 0 if n == 1 else f(n - 1, k)

def h(n, k):
    return f(n, k) + g(n, k)


assert func(4, 3) == h(4, 3)
assert func(3, 3) == h(3, 3)
assert func(5, 3) == h(5, 3)
assert func(5, 4) == h(5, 4)
