import numpy as np

def print_mx(S, T, D):
    res = ''

    S = '#' + S
    for i in range(len(S) - 1, -1, -1):
        res += S[i] + '\t' + '\t'.join(map(str, D[i])) + '\n'

    T = ' #' + T
    res += '\t'.join(T)

    print(res)


def testname(func):
    print()
    print(func.__name__.upper())
    print('-' * 60)


def test_dist(func_mx, func_dist, input, output):
    S, T = input

    D = func_mx(S, T)
    if D is None:
        print("X")
        return

    d = func_dist(S, T)

    DO, do = output
    OK_text = "OK" if np.array_equal(D, DO) and d == do else "X"

    print('%s\tudaljenost između %r i %r je %s' % (OK_text, S, T, d))
    print_mx(S, T, D)
    print()


def test_alignment(func_align, input, output):
    S, T = input
    result = func_align(S, T)
    if result is None:
        print("X")
        return
    NS, NT = result
    print('%s\tporavnanje od %r i %r:\n%s\n%s' % ('OK' if output == result else 'X', S, T, NS, NT))
    print()
