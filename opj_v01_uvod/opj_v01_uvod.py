# coding=utf8

def read_file(filename):
    """
    ulaz:
    -filename: putanja datoteke
    izlaz:
    -tekst iz datoteke
    """
    return open(filename, 'r', encoding = 'utf8').read()

def len_file(filename):
    """
    ulaz:
    -filename: putanja datoteke
    izlaz:
    -broj znakova u datoteci
    """
    return

def count_chars(txt, chars):
    """
    ulaz:
    -txt: tekst
    -chars: lista znakova
    izlaz:
    -ukupan broj pojavljivanja znakova iz liste znakova u tekstu

    Primjer: u tekstu "Upravo sada kad sam konačno našao mušteriju!"
    znakovi "a", "k" i "t" se ukupno javljaju 11 puta.
    """
    return


def pos_subtext(txt, subtxt):
    """
    ulaz:
    -txt: tekst
    -subtxt: podtekst
    izlaz:
    -sortirana lista pozicija podteksta u tekstu

    Primjer: U tekstu "Upravo sada kad sam konačno našao mušteriju!"
    podtekst "na" se nalazi na pozicijama 22 i 28
    """
    return

def sep_text(txt, sep):
    """
    ulaz:
    -txt: tekst
    -sep: znak separatora
    izlaz:
    -lista svih podtekstova iz teksta koji se nalaze između 2 separatora

    Primjer: za tekst "aaaXbbXcccXdXX" i znak separatora "X" rezultirajuća 
    lista je ['bb', 'ccc', 'd', '']
    """
    return

def split_text(txt, sep):
    """
    ulaz:
    -txt: tekst
    -sep: znak separatora
    izlaz:
    -lista svih podtekstova iz teksta koji se nalaze između 2 separatora 
    ili između separatora i početka ili kraja teksta

    Primjer: za tekst "aaaXbbXcccXdXX" i znak separatora "X" rezultirajuća 
    lista je ['aaa', 'bb', 'ccc', 'd', '', '']
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

testname(len_file)
test(len_file, (FILENAME, ), 19301)

testname(count_chars)
test(count_chars, input=('Upravo sada kad sam konačno našao mušteriju!', ['a','k','t']), output=11)
test(count_chars, input=('Upravo sada kad sam konačno našao mušteriju!', ['u','U']), output=3)
test(count_chars, input=(read_file(FILENAME), ['a','k','t']), output=2939)

testname(pos_subtext)
test(pos_subtext, input=('Upravo sada kad sam konačno našao mušteriju!', 'na'), output=[22, 28])
test(pos_subtext, input=('Bananarama je svakog dana sama', 'ana'), output=[1, 3, 22])
test(pos_subtext, input=(read_file(FILENAME), 'New York'), output= [29, 12946, 16002])

testname(sep_text)
test(sep_text, input=('aaaXbbXcccXdXX', 'X'), output = ['bb', 'ccc', 'd', ''])
test(sep_text, input=('Da čujemo što mladac zna! Prokleta lopužo! Ili sviraj ili vrati novac!', ' '), output = ['čujemo', 'što', 'mladac', 'zna!', 'Prokleta', 'lopužo!', 'Ili', 'sviraj', 'ili', 'vrati'])

testname(split_text)
test(split_text, input=('aaaXbbXcccXdXX', 'X'), output = ['aaa', 'bb', 'ccc', 'd', '', ''])
test(split_text, input=('Da čujemo što mladac zna! Prokleta lopužo! Ili sviraj ili vrati novac!', ' '), output = ['Da', 'čujemo', 'što', 'mladac', 'zna!', 'Prokleta', 'lopužo!', 'Ili', 'sviraj', 'ili', 'vrati', 'novac!'])
