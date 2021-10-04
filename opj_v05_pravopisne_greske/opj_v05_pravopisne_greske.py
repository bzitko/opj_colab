# coding=utf-8

"""
1. DATOTEKA NGRAM MODELA
read_model i write_model su metode koje služe za rad s datotekom ngram modela.
U ovom slučaju radi se o datoteci "hr_unigram.txt" koja sadrži unigram modela,
odnosno redak u datoteci je riječ i njena frekvencija (broj pojavljivanja)

2. MINIMALNA UDALJENOST 1
gen_deletes, gen_inserts, gen_replaces i gen_transposes su funkcija koje za zadanu riječ
i abecedu generiraju skup riječi koje su za 1 udaljene od zadane riječi temeljem
brisanja, ubacivanja, zamjene i transpozicije (zamjene dva susjedna znaka) u zadanoj riječi.
Na primjer, neka je zadana riječ: "pas" i abeceda "ABC"
gen_deletes daje: "as", "ps", "pa"
gen_inserts daje: "Apas", "Bpas", "Cpas", "pAas", "pBas", "pCas", "paAs", "paBs", "paCs", "pasA", "pasB", "pasC"
gen_replaces daje: "Aas", "Bas", "Cas", "pAs", "pBs", "pCs", "paA", "paB", "paC"
gen_transposes daje: "aps", "psa"

gen_edits1 daje sve riječi koje su za jedan udaljene od zadane riječi temeljem zadane abecede.
Zapravo gen_edits1 vraća uniju skupova riječi dobivenih od gen_deletes, gen_inserts, gen_replaces i gen_transposes

3. KANDIDATI ZA PRAVOPISNU GREŠKU
Za dobivanje kandidata pravopisne greške koristi se unigram model iz datoteke "hr_unigram.txt".
Unigram model je već učitan i koristi se kao ulazni argument za funkciju spell_candidates.

spell_candidates je funkcija koja za zadanu riječ, abecedu i unigram model vraća listu kandidata koji su za
1 udaljeni od zadane riječi i koje se nalaze u unigram modelu. Kandidati su sortirani silazno po broju pojavljivanja
u unigram modelu.
"""

def read_model(filename):
    """
    ulaz:
    -filename: putanja datoteke
    izlaz:
    -model jezika
    """
    print('*** loading model ' + filename, end=' ')
    txt = open(filename, 'r', encoding='utf8').read().strip()

    model = {}
    for line in txt.split('\n'):
        if not line.startswith('#'):
            line = line.split('\t')
            ngram, freq = tuple(line[:-1]), int(line[-1])
            model[ngram] = freq
    print('FINISHED')
    return model

def write_model(filename, model, comment = None):
    """
    ulaz:
    -filename: putanja datoteke
    -model: model jezika
    -comment: opcioni komentar na početku datoteke
    izlaz:
    zapiše model jezika u datoteku
    svaki red datoteke je oblika
    w1\tw2\tw3\t...\twn\tfreq
    gdje su w1, ..., wn riječi ngrama, a freq frekvencija
    """
    f = open(filename, 'w', encoding='utf8')
    if comment: f.write('# ' + str(comment) + '\n')
    for freq, ngram in sorted(((freq, ngram) for ngram, freq in model.items()), reverse=True):
        f.write('\t'.join(ngram) + '\t' + str(freq) + '\n')
    f.close()

def gen_deletes(word):
    """
    ulaz:
    -word: riječ
    izlaz:
    -skup svih riječi nastalih brisanjem jednog znaka iz zadane riječi

    Primjer: za riječ "pas" dobiva se {"as", "ps", "pa"}
    """
    return set()

def gen_inserts(word, alphabet):
    """
    ulaz:
    -word: riječ
    -alphabet: znakovi abecede (kao string)
    izlaz:
    -skup svih riječi nastalih dodavanjem svakog znaka iz abecede na sva moguća mjesta u riječi

    Primjer: za riječ "pas" i abecedu "abc" dobiva se
    {"apas", "bpas", "cpas", "paas", "pbas", "pcas", "pabs", "pacs", "pasa", "pasb", "pasc"}
    """
    return set()

def gen_replaces(word, alphabet):
    """
    ulaz:
    -word: riječ
    -alphabet: znakovi abecede (kao string)
    izlaz:
    -skup svih riječi nastalih zamjenom svakog znaka iz riječi sa svakim znakom iz abecede

    Primjer: za riječ "pas" i abecedu "abc" dobiva se
    {"aas", "bas", "cas", "pas", "pbs", "pcs", "paa", "pab", "pac"}
    """
    return set()

def gen_transposes(word):
    """
    ulaz:
    -word: riječ
    izlaz:
    -skup riječi nastalih zamjenom dva susjedna znaka zadane riječi

    Primjer: za riječ "pas" dobiva se
    {"aps", "psa"}
    """
    return set()

def gen_edits1(word, alphabet):
    """
    ulaz:
    -word: riječ
    -alphabet: abeceda
    izlaz:
    -skup riječi koji su za 1 udaljeni od dane riječi
    ovisnost:
    -gen_deletes, gen_inserts, gen_replaces, gen_transposes

    Napomena: Rezultat je unija skupova dobivenim brisanjem, ubacivanjem, zamjenom i transpozicijom
    """
    return set()

def spell_candidates(word, alphabet, model):
    """
    ulaz:
    -word: riječ
    -alphabet: abeceda
    -model: unigram model jezika
    izlaz:
    -lista kandidata nastalih presjekom skupa riječi koje su za 1 udaljene od zadane riječi i
    skupa svih riječi iz unigrama sortiranih po frekvenciji riječi od najveće prema najmanjom
    ovisnost:
    -gen_edits1
    """
    return


def testname(func):
    print()
    print(func.__name__.upper())
    print('-'*60)

def test(func, input, output = None):
    def reformat(data):
        maxlen = 80
        maxdict = 5
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(reformat(el) for el in data)
        if isinstance(data, dict):
            return type(data)((k, reformat(data[k])) for k in sorted(data)[:maxdict])
        return data

    import copy
    input_copy = copy.deepcopy(input)
    result = func(*input)

    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    print('%s\t%s%s \n=> %s\n%s= %s\n' % (success, func.__name__, reformat(input_copy), reformat(output), success_rel ,result))

testname(gen_deletes)
test(gen_deletes, ('pas', ), {'as', 'ps', 'pa'})
test(gen_deletes, ('kuća', ), {'uća', 'kća', 'kua', 'kuć'})

testname(gen_inserts)
test(gen_inserts, ('pas', 'abc'), {'apas', 'bpas', 'cpas', 'paas', 'pbas', 'pcas', 'pabs', 'pacs', 'pasa', 'pasb', 'pasc'})
test(gen_inserts, ('kuća', 'ABC'), {'Akuća', 'Bkuća', 'Ckuća', 'kAuća', 'kBuća', 'kCuća', 'kuAća', 'kuBća', 'kuCća', 'kućAa', 'kućBa', 'kućCa', 'kućaA', 'kućaB', 'kućaC'})

testname(gen_replaces)
test(gen_replaces, ('pas', 'abc'), {'aas', 'bas', 'cas', 'pas', 'pbs', 'pcs', 'paa', 'pab', 'pac'})
test(gen_replaces, ('kuća', 'ABC'), {'Auća', 'Buća', 'Cuća', 'kAća', 'kBća', 'kCća', 'kuAa', 'kuBa', 'kuCa', 'kućA', 'kućB', 'kućC'})

testname(gen_transposes)
test(gen_transposes, ('pas', ), {'aps', 'psa'})
test(gen_transposes, ('kuća', ), {'ukća', 'kćua', 'kuać'})

testname(gen_edits1)
test(gen_edits1, ('pas', 'abc'), {'pabs', 'pa', 'pasa', 'pasc', 'paa', 'pab', 'pas', 'bpas', 'apas', 'aps', 'pcs', 'pbas', 'cas', 'pac', 'ps', 'psa', 'cpas', 'pcas', 'aas', 'pbs', 'paas', 'as', 'bas', 'pasb', 'pacs'})

unigram = read_model('hr_unigram.txt')
testname(spell_candidates)
test(spell_candidates, ('moelkula', 'abcčćdđefghijklmnoprsštuvzž', unigram), ['molekula'])
test(spell_candidates, ('atmo', 'abcčćdđefghijklmnoprsštuvzž', unigram), ['tamo', 'amo', 'ajmo', 'atom', 'ato'])
test(spell_candidates, ('pivt', 'abcčćdđefghijklmnoprsštuvzž', unigram), ['piva', 'pivo', 'pivu', 'pive', 'pit', 'pivot', 'pivat'])

