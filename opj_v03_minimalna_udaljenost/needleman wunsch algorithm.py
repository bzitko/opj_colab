# coding=utf-8

def print_mx(S, T, D):
    """
    ulaz:
    -S: string
    -T: string
    -D: matrica udaljenosti
    izlaz:
    -ispis na konzoli stringova S, T i matrice udaljenosti D
    """
    res = ''

    T = ' #' + T
    res += '\t'.join(T) + "\n"

    S = '#' + S
    for i in range(0, len(S)):
        res += S[i] + '\t' + '\t'.join(map(str, D[i])) + '\n'



    print(res)


def edit_dist_mx(S, T):
    """
    ulaz:
    -S: string
    -T: string
    izlaz:
    -matrica udaljenosti između S i T koristeći Levenshteinovu udaljenost
    """
    n, m = len(S), len(T)
    D = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    change = -1

    for i in range(n + 1):
        D[i][0] = i * change
    for j in range(m + 1):
        D[0][j] = j * change

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = max(D[i - 1][j] + change,
                          D[i][j - 1] + change,
                          D[i - 1][j - 1] + (change if S[i - 1] != T[j - 1] else -change))

    return D

def edit_dist(S, T):
    """
    ulaz:
    -S: string
    -T: string
    izlaz:
    -minimalna udaljenost između S i T
    Napomena: koristiti edit_dist_mx da se dobije matrica udaljenosti
    """
    return edit_dist_mx(S, T)[-1][-1]

def align(S, T):
    """
    ulaz:
    -S: string
    -T: string
    izlaz:
    -NS: string - poravnanje od S
    -NT: string - poravnanje od T

    Napomena: kod poravnanja koristiti znak "-".
    """
    D = edit_dist_mx(S, T)
    NS, NT = '', ''
    state = n, m = len(S), len(T)
    i, j = n-1, m-1
    while state != (0, 0):
        n, m = state
        next_states = {D[x][y]: (x, y) for x, y in [(n-1, m), (n, m-1), (n-1, m-1)] if x >= 0 and y >= 0}
        next_state = next_states[max(next_states)]
        nn, mm = next_state

        if nn < n:
            NS = S[i] + NS
            i -= 1
        else:
            NS = '-' + NS

        if mm < m:
            NT = T[j] + NT
            j -= 1
        else:
            NT = '-' + NT

        state = next_state

    return NS, NT

# ********************************************************************
# TEST FUNKCIJE
# ********************************************************************

def testname(func):
    print()
    print(func.__name__.upper())
    print('-'*60)

def test_dist(input, output, align = False):
    S, T = input

    D = edit_dist_mx(S, T)
    d = edit_dist(S, T)
    print('%s\tudaljenost između %r i %r je %s' % ('OK' if output == (D, d) else 'X', S, T, d))
    print_mx(S, T, D)
    print()


def test_alignment(input, output):
    S, T = input
    result = align(S, T)
    NS, NT = result
    print('%s\tporavnanje od %r i %r:\n%s\n%s' % ('OK' if output == result else 'X', S, T, NS, NT))
    print()

# ********************************************************************
# TESTOVI
# ********************************************************************


testname(edit_dist)
test_dist(('GATTACA','GCATGCU'), ([[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 2]], 2))
test_alignment(('GATTACA','GCATGCU'), ('nos', 'noj'))
# test_dist(('osa','bosa'), ([[0, 1, 2, 3, 4], [1, 2, 1, 2, 3], [2, 3, 2, 1, 2], [3, 4, 3, 2, 1]], 1))
# test_dist(('bosa','osa'), ([[0, 1, 2, 3], [1, 2, 3, 4], [2, 1, 2, 3], [3, 2, 1, 2], [4, 3, 2, 1]], 1))
# test_dist(('paliti','piti'), ([[0, 1, 2, 3, 4], [1, 0, 1, 2, 3], [2, 1, 2, 3, 4], [3, 2, 3, 4, 5], [4, 3, 2, 3, 4], [5, 4, 3, 2, 3], [6, 5, 4, 3, 2]], 2))
# test_dist(('paliti','pisati'), ([[0, 1, 2, 3, 4, 5, 6], [1, 0, 1, 2, 3, 4, 5], [2, 1, 2, 3, 2, 3, 4], [3, 2, 3, 4, 3, 4, 5], [4, 3, 2, 3, 4, 5, 4], [5, 4, 3, 4, 5, 4, 5], [6, 5, 4, 5, 6, 5, 4]], 4))

# testname(align)
# test_alignment(('nos','noj'), ('nos', 'noj'))
# test_alignment(('osa','bosa'), ('-osa', 'bosa'))
# test_alignment(('bosa','osa'), ('bosa', '-osa'))
# test_alignment(('paliti','piti'), ('paliti', 'p--iti'))
# test_alignment(('paliti','pisati'), ('pali--ti', 'p--isati'))
# test_alignment(('blindiram', 'navigiram'), ('blin-di--ram', '---navigiram'))
