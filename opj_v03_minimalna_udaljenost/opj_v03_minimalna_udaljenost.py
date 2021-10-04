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
    if not D: return
    
    res = ''
    
    S = '#' + S
    for i in range(len(S) - 1, -1, -1):
        res += S[i] + '\t' + '\t'.join(map(str, D[i])) + '\n'

    T = ' #' + T
    res += '\t'.join(T)

    print(res)


def edit_dist_mx(S, T):
    """
    ulaz:
    -S: string
    -T: string
    izlaz:
    -matrica udaljenosti između S i T koristeći Levenshteinovu udaljenost
    """
    return

def edit_dist(S, T):
    """
    ulaz:
    -S: string
    -T: string
    izlaz:
    -minimalna udaljenost između S i T
    Napomena: koristiti edit_dist_mx da se dobije matrica udaljenosti
    """
    return 

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
    return None, None

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
test_dist(('nos','noj'), ([[0, 1, 2, 3], [1, 0, 1, 2], [2, 1, 0, 1], [3, 2, 1, 2]], 2))
test_dist(('osa','bosa'), ([[0, 1, 2, 3, 4], [1, 2, 1, 2, 3], [2, 3, 2, 1, 2], [3, 4, 3, 2, 1]], 1))
test_dist(('bosa','osa'), ([[0, 1, 2, 3], [1, 2, 3, 4], [2, 1, 2, 3], [3, 2, 1, 2], [4, 3, 2, 1]], 1))
test_dist(('paliti','piti'), ([[0, 1, 2, 3, 4], [1, 0, 1, 2, 3], [2, 1, 2, 3, 4], [3, 2, 3, 4, 5], [4, 3, 2, 3, 4], [5, 4, 3, 2, 3], [6, 5, 4, 3, 2]], 2))
test_dist(('paliti','pisati'), ([[0, 1, 2, 3, 4, 5, 6], [1, 0, 1, 2, 3, 4, 5], [2, 1, 2, 3, 2, 3, 4], [3, 2, 3, 4, 3, 4, 5], [4, 3, 2, 3, 4, 5, 4], [5, 4, 3, 4, 5, 4, 5], [6, 5, 4, 5, 6, 5, 4]], 4))

testname(align)
test_alignment(('nos','noj'), ('nos', 'noj'))
test_alignment(('osa','bosa'), ('-osa', 'bosa'))
test_alignment(('bosa','osa'), ('bosa', '-osa'))
test_alignment(('paliti','piti'), ('paliti', 'p--iti'))
test_alignment(('paliti','pisati'), ('pali--ti', 'p--isati'))
test_alignment(('blindiram', 'navigiram'), ('blin-di--ram', '---navigiram'))
