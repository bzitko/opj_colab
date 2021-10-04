# coding=utf-8
import re

def read_file(filename):
    """
    ulaz:
    -filename: putanja datoteke
    izlaz:
    -tekst iz datoteke
    """
    return

def count_pattern(txt, pattern):
    """
    ulaz:
    -txt: tekst
    -pattern: regularni izraz
    izlaz:
    -broj odgovarajućih dijelova teksta po regularnom izrazu
    Npr. Za tekst "4 plus 31 jednako 5" i regularni izraz r"\d+" vraća 3
    """
    return

def match_pattern(txt, pattern):
    """
    ulaz:
    -txt: tekst
    -pattern: regularni izraz
    izlaz:
    -lista odgovarajućih djelova teksta po regularnom izrazu
    Npr. Za tekst "4 plus 31 jednako 5" i regularni izraz r"\d+" vraća
    listu svih nizova brojčanih znakova ['4', '31', '5'] kako se pojavljuju
    u tekstu
    """
    return

def split_pattern(txt, pattern):
    """
    ulaz:
    -txt: tekst
    -pattern: regularni izraz
    izlaz:
    -lista odgovarajućih djelova teksta po regularnom izrazu
    Npr. Za tekst "4 plus 31 jednako 5" i regularni izraz r"\d+" vraća
    listu svih nizova koji ne odgovaraju regularnom izrazu odnosno
    [' plus ', ' jednako ']
    """
    return

def cnt_newline(txt):
    """
    ulaz:
    -txt: tekst
    izlaz:
    -ukupan broj pojavljivanja novog reda u tekstu
    """
    return

def mtch_upper_word(txt):
    """
    ulaz:
    -txt: tekst
    izlaz:
    -lista riječi koje počinju s velikim slovom
    """
    return

def mtch_infix(txt, infix):
    """
    ulaz:
    -txt: tekst
    -infix: tekst
    izlaz:
    -lista riječi koje sadrže infix
    """
    return


# TEST FUNKCIJE ********************************************************************

def testname(func):
    print()
    print(func.__name__.upper())
    print('-'*60)

def test(func, input, output = None):
    def reformat(data):
        maxlen = 80
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(reformat(el) for el in data)
        if isinstance(data, dict):
            return type(data)((k, reformat(v)) for k, v in data.items())
        return data

    import copy
    input_copy = copy.deepcopy(input)
    result = func(*input)

    success = 'OK' if result == output else 'X'
    print('%s\t%s%s ==> %s == %s' % (success, func.__name__, reformat(input_copy), reformat(output), (result)))

# TESTOVI **************************************************************************

FILENAME = 'alan_ford_001_grupa_tnt.txt'
TXT = """
Čujmo malo muzike! Tišina me odviše podsjeća na groblje! Hm... Beethoven! Mora da je to neki popkauntor. Da čujemo što mladac zna! Prokleta lopužo! Ili sviraj ili vrati novac! Ta moderna muzika zaista je ispunjena elektricitetom.

Gotovo, mister. Želite li još nešto? Malo masaže ne bi štetilo. I ovako se sviđam ženama, ali nikad nije na odmet... Sklopite oči! Naočale pomažu, ali svjetlost će biti snažna pa je bolje da žmirite... Hm! Namjestio sam automat na 45 sekunda! A sad... Hm... Čini se da treba nešto izmijeniti na automatu! Učinit ću to još danas!
""".strip()

testname(count_pattern)
test(count_pattern, (TXT, r'a'), 53)
test(count_pattern, (TXT, r'[^a]'), 506)
test(count_pattern, (TXT, r'\S+'), 94)
test(count_pattern, (TXT, r'\w+'), 94)
test(count_pattern, (TXT, r'oš'), 2)
test(count_pattern, (TXT, r'al'), 5)
test(count_pattern, (TXT, r'oš|al'), 7)

testname(match_pattern)
test(match_pattern, (TXT, r'oš|al'), ['al', 'oš', 'al', 'al', 'al', 'al', 'oš'])
test(match_pattern, (TXT, r'\bo\w+'), ['odviše', 'ovako', 'odmet', 'oči'])
test(match_pattern, ('b**2-49ac', '\d'), ['2','4','9'])
test(match_pattern, ('b**2-49ac', '\d*'), ['', '', '', '2', '', '49', '', '', ''])
test(match_pattern, ('b**2-49ac', '\d+'), ['2', '49'])

testname(split_pattern)
test(split_pattern, ('b**2-49ac', '\d+'), ['b**', '-', 'ac'])
test(split_pattern, ('b**2-49ac', '\D+'), ['', '2', '49', ''])

testname(cnt_newline)
test(cnt_newline, (TXT, ), 2)
test(cnt_newline, (read_file(FILENAME), ), 44)

testname(mtch_upper_word)
test(mtch_upper_word, ('A AA bba, Bcd, cDD Šđđ Žeđ',), ['A', 'AA', 'Bcd', 'Šđđ', 'Žeđ'])
test(mtch_upper_word, (TXT, ), ['Čujmo', 'Tišina', 'Hm', 'Beethoven', 'Mora', 'Da', 'Prokleta', 'Ili', 'Ta', 'Gotovo', 'Želite', 'Malo', 'I', 'Sklopite', 'Naočale', 'Hm', 'Namjestio', 'A', 'Hm', 'Čini', 'Učinit'])

testname(mtch_infix)
test(mtch_infix, (TXT, 'ma'), ['malo', 'masaže', 'ženama', 'pomažu', 'automat', 'automatu'])
test(mtch_infix, (read_file(FILENAME), 'oba'), ['isprobati', 'dobar', 'neobavljena', 'soba', 'osoba', 'obavijest', 'sposoban', 'dobar'])


