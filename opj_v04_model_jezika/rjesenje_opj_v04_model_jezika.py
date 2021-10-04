# coding=utf-8

import re

def read_file(filename):
    """
    ulaz:
    -filename: putanja datoteke
    izlaz:
    -tekst iz datoteke
    """
    return open(filename, 'r', encoding = 'utf8').read()

def segment_sentence(txt):
    """
    ulaz:
    -txt: tekst
    izlaz:
    -lista rečenica dobivenih iz teksta razbijanjem po regularnom izrazu
    koji traži sve interpunkcijske znakove i nove redove.
    Također se izbacuju sve vrste zagrada na početku i/ili kraju svake rečenice.
    """
    sentences = re.split(r'[\n.\!\?]+', txt.strip())
    sentences = [sent.strip(' [](){}') for sent in sentences if sent.strip()]
    return sentences

def segment_word(txt):
    """
    ulaz:
    -txt: tekst
    izlaz:
    -lista riječi u tekstu nastalih razbijanjem po regularnom izrazu
    koji traži sve razmake, interpunkcijske znakove i zareze.
    Također se izbacuju sve vrste zagrada i navodika na početku
    i/ili kraju svake riječi.
    """
    words = re.split(r'[ \,\.\!\?\n]', txt)
    words = [word.strip(' [](){}') for word in words if word.strip()]
    return words

def segment_sentences_words(txt):
    return [segment_word(sent) for sent in segment_sentence(txt)]

def build_ngram(sentence, ngram_size):
    """
    ulaz:
    -sentence: tekst rečenice
    -ngram_size: broj koji određuje veličinu n-grama
    izlaz:
    -lista n-grama zadane rečenice. n-gram je uređena n-torka (tuple) riječi
    Bitni su početak i kraj rečenice. Početak i kraj rečenice označiti sa "<sent>" i "</sent>".
    Napomena: kod unigrama odnosno kad je ngram_size = 1 n-torka je i dalje tuple,
    odnosno ima oblik (riječ, ).
    """
    ngram = []
    sent_words = ['<sent>'] + segment_word(sentence) + ['</sent>']
    for i in range(len(sent_words) - ngram_size + 1):
        ngram.append(tuple(sent_words[i:i+ngram_size]))
    return ngram


def build_model(txt, ngram_size):
    """
    ulaz:
    -txt: tekst
    -ngram_size: broj koji određuje veličinu n-grama
    izlaz:
    -rječnik čiji su ključevi ngrami (kao tuple riječi) a vrijednosti broj pojavljivanja u tekstu
    Napomena: bitni su početak i kraj rečenice. Početak i kraj rečenice označiti sa "<sent>" i "</sent>"
    Npr. Za tekst "A gdje je ured? Ne znam gdje je." i za ngram_size = 2 dobiveni ngrami su
    ("<sent>", "A"), ("A", "gdje"), ("gdje", "je"), ("je", "ured"), ("ured", "</sent>")
    ("<sent>", "Ne"), ("Ne", "znam"), ("znam", "gdje"), ("gdje", "je"), ("je", "</sent>")
    a, model jezika je
    {("<sent>", "A"): 1,
     ("A", "gdje"): 1,
     ("gdje", "je"): 2,
     ("je", "ured"): 1,
     ("ured", "</sent>"): 1,
     ("<sent>", "Ne"): 1,
     ("Ne", "znam"): 1,
     ("znam", "gdje"): 1,
     ("je", "</sent>": 1)
     }
    """
    model = {}
    for sent in segment_sentence(txt):
        for ngram in build_ngram(sent, ngram_size):
            model[ngram] = model.get(ngram, 0) + 1
    return model

def digram_probability(sentence, model2, model1):
    """
    ulaz:
    -sentence: tekst rečenice
    -model2: digram
    -model1: unigram
    izlaz:
    -vjeroratnost rečenice po digram modelu normaliziranog uz pomoć unigram modela
    Napomena: vjerojatnost pojedinog digrama (A, B) je jednaka broju
    pojavljivanja digrama (A, B) podijeljenog s brojem pojavljivanja unigrama (A, )
    P(A, B) = broj((A, B)) / broj(A, )
    """
    prob = 1
    for ngram in build_ngram(sentence, 2):
        cnt2 = model2.get(ngram, 0)
        cnt1 = model1.get(ngram[:1], 0)
        prob *= cnt2 / cnt1
    return prob

def digram_probability_laplace(sentence, model2, model1):
    """
    ulaz:
    -sentence: tekst rečenice
    -model2: digram
    -model1: unigram
    izlaz:
    -vjeroratnost rečenice po digram modelu normaliziranog uz pomoć unigram modela s
    dodaj-1 izglađivanjem.
    P(A, B) = (broj((A, B)) + 1) / (broj(A) + |V|)
    gdje je V broj različitih riječi u unigramu
    """
    prob = 1
    v = len(model1)
    for ngram in build_ngram(sentence, 2):
        cnt2 = model2.get(ngram, 0) + 1
        cnt1 = model1.get(ngram[:1], 0) + v
        prob *= cnt2 / cnt1
    return prob


def random_chain(model):
    word = '<sent>'
    sentence = []
    while word != '</sent>':
        next_grams = {gram for gram in model if gram[0] == word}
        if next_grams:
            next_gram = max(next_grams, key = lambda x: model[x])
            sentence.append(next_gram)
            word = next_gram[-1]
            if word == '<sent>':
                break
        else:
            break
    print(sentence)
    sentence = ' '.join(' '.join(gram[1:]) for gram in sentence).strip('</sent>')
    print(sentence)


# TEST FUNKCIJE
# ********************************************************************

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
            return type(data)((k, reformat(data[k])) for k in list(data)[:3])
        return data

    import copy
    input_copy = copy.deepcopy(input)
    result = func(*input)

    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    print('%s\t%s%s \n=> %s\n%s= %s\n' % (success, func.__name__, reformat(input_copy), reformat(output), success_rel ,result))


def test_model(func, input, output):
    def reformat(data):
        maxlen = 80
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(reformat(el) for el in data)
        if isinstance(data, dict):
            return type(data)((k, reformat(data[k])) for k,v in data.items())
        return data
    def freq_model(model):
        freq = {}
        for count in model.values():
            freq[count] = freq.get(count, 0) + 1
        return freq

    model = build_model(*input)
    result = freq_model(model)
    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    #print('%s\t%s%s ==> %s == %s\n' % (success, func.__name__, reformat(input), reformat(output), (result)))
    print('%s\t%s%s \n=> %s\n%s= %s\n' % (success, func.__name__, reformat(input), reformat(output), success_rel ,result))
    return model

# TESTOVI
# ********************************************************************
testname(segment_sentence)
test(segment_sentence, ("A gdje je tvoj ured?", ), ['A gdje je tvoj ured'])
test(segment_sentence, ("A gdje je tvoj ured? Ne znam gdje je.", ), ['A gdje je tvoj ured', 'Ne znam gdje je'])
test(segment_sentence, ("""[Alan Ford 001 - Grupa TNT]
New York, najveći grad sjedinjenih država, kip slobode, neboderi, devet milijuna mrava što stanuju...
Čujmo malo muzike! Tišina me odviše podsjeća na groblje! """, ),
['Alan Ford 001 - Grupa TNT',
'New York, najveći grad sjedinjenih država, kip slobode, neboderi, devet milijuna mrava što stanuju',
'Čujmo malo muzike',
'Tišina me odviše podsjeća na groblje'])

testname(segment_word)
test(segment_word, ("A gdje je tvoj ured?", ), ['A', 'gdje', 'je', 'tvoj', 'ured'])
test(segment_word, ("A gdje je tvoj ured? Ne znam gdje je.", ), ['A', 'gdje', 'je', 'tvoj', 'ured', 'Ne', 'znam', 'gdje', 'je'])
test(segment_word, ("""[Alan Ford 001 - Grupa TNT]
New York, najveći grad sjedinjenih država, kip slobode, neboderi, devet milijuna mrava što stanuju...
Čujmo malo muzike! Tišina me odviše podsjeća na groblje! """, ),
['Alan', 'Ford', '001', '-', 'Grupa', 'TNT', 'New', 'York', 'najveći', 'grad', 'sjedinjenih', 'država', 'kip', 'slobode', 'neboderi', 'devet', 'milijuna', 'mrava', 'što', 'stanuju', 'Čujmo', 'malo', 'muzike', 'Tišina', 'me', 'odviše', 'podsjeća', 'na', 'groblje'])


testname(build_ngram)
test(build_ngram, ("A gdje je tvoj ured?", 1), [('<sent>',), ('A',), ('gdje',), ('je',), ('tvoj',), ('ured',), ('</sent>',)])
test(build_ngram, ("A gdje je tvoj ured?", 2), [('<sent>', 'A'), ('A', 'gdje'), ('gdje', 'je'), ('je', 'tvoj'), ('tvoj', 'ured'), ('ured', '</sent>')])
test(build_ngram, ("A gdje je tvoj ured?", 5), [('<sent>', 'A', 'gdje', 'je', 'tvoj'), ('A', 'gdje', 'je', 'tvoj', 'ured'), ('gdje', 'je', 'tvoj', 'ured', '</sent>')])

FILENAME = 'alan_ford_001_grupa_tnt.txt'
testname(build_model)
model1 = test_model(build_model, (read_file(FILENAME), 1), {1: 1185, 2: 182, 3: 73, 4: 44, 5: 20, 6: 9, 7: 14, 8: 13, 9: 5, 10: 2, 11: 2, 12: 3, 13: 1, 14: 3, 15: 4, 16: 2, 17: 1, 18: 1, 19: 4, 20: 1, 22: 1, 27: 1, 30: 1, 97: 1, 34: 1, 35: 1, 101: 1, 40: 1, 109: 1, 46: 1, 47: 1, 688: 2, 55: 1})
model2 = test_model(build_model, (read_file(FILENAME), 2), {1: 2910, 2: 220, 3: 61, 4: 30, 5: 10, 6: 6, 7: 9, 8: 6, 9: 3, 10: 4, 14: 2, 15: 3, 20: 1, 22: 1})
model3 = test_model(build_model, (read_file(FILENAME), 3), {1: 3055, 2: 78, 3: 19, 4: 7, 6: 3, 7: 2, 8: 2})



testname(digram_probability)
test(digram_probability, ("A gdje je tvoj ured?", model2, model1), 6.6673778536377226e-06)
test(digram_probability, ("U ovih nekoliko posljednjih sati, život se budio prolaznici su zaista dosadni!", model2, model1), 2.1678842892280916e-09)
test(digram_probability, ("Hm... uvijek kad zakočim ispadne kotač i ne čeka.", model2, model1), 8.777103696213908e-09)

testname(digram_probability_laplace)
#test(digram_probability_laplace, ("A gdje je tvoj ured?", model2, model1), 6.6673778536377226e-06)
test(digram_probability_laplace, ("xxx?", model2, model1), 2.781646584569149e-07)
test(digram_probability_laplace, ("xx xx xx xx?", model2, model1), 7.0122793090205e-17)

#random_chain(model2)
