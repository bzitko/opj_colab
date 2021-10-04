# coding=utf-8

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
    return len(read_file(filename))

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
    return sum(txt.count(ch) for ch in chars)

def count_subtext(txt, subtxt):
    """
    ulaz:
    -txt: tekst
    -subtxt: podteks
    izlaz:
    -ukupan broj pojavljivanje podteksta u tekstu

    Primjer: u tekstu "Upravo sada kad sam konačno našao mušteriju!"
    podtekst "na" se javlja 3 puta.
    """
    return txt.count(subtxt)

def pos_subtext(txt, subtxt):
    """
    ulaz:
    -txt: tekst
    -subtxt: podtekst
    izlaz:
    -sortirana lista pozicija podteksta u tekstu

    Primjer: U tekstu "Upravo sada kad sam konačno našao mušteriju!"
    podtekst "na" se nalazi na pozicijama
    """
    pos_list = []
    for i in range(0, len(txt) - len(subtxt) + 1):
        if txt[i: i+len(subtxt)] == subtxt:
            pos_list.append(i)
    return pos_list

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
    result = []
    i = 0
    while i < len(txt):
        if txt[i] == sep:
            j = i + 1
            while j < len(txt):
                if txt[j] == sep:
                    result.append(txt[i+1:j])
                    i = j - 1
                    break
                j += 1
        i += 1
    return result

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
    return txt.split(sep)


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
