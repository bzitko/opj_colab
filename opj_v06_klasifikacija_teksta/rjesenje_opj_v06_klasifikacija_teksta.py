# coding=utf-8
import re
import math

def read_file(filename):
    """
    ulaz:
    -filename: datoteka

    izlaz:
    -sadržaj datoteke
    """
    return open(filename, 'r', encoding='utf-8').read()

def file_to_doc_model(filename):
    """
    ulaz:
    -filename: datoteka

    izlaz:
    -model dokumenta kao unigram stvoren temeljem sadržaja datoteke; riječi u datoteci su odvojene razmakom
    i potrebno ih je pretvoriti u mala slova

    Npr: ako je sadržaj datoteke "Češka Obala Bjelokosti Češka Republika" onda će unigram biti
    {'česka': 2, 'obala': 1, 'bjelokosti': 1, 'republika': 1}
    """
    doc_model = {}
    for word in read_file(filename).lower().split():
        doc_model[word] = doc_model.get(word, 0) + 1
    return doc_model

def build_train_model(path):
    """
    ulaz:
    -path: putanja do direktorija koji sadrži podatke za treniranje oblika
      train/
        AFRIKA/
          afrika01.txt
          afrika02.txt
          ...
        AZIJA/
          azija01.txt
          azija02.txt
          ...
        ...
    AFRIKA, AZIJA i ostali kontinenti su klase, a afrika01.txt, afrika02.txt, ... su dokumenti koji se pretvaraju u unigrame
    koristeći funkciju file_to_doc_model()

    izlaz:
    -trenirani model kao rječnik čiji su ključevi klase, a vrijednosti lista dokumenata iz te klase pretvorenih u unigrame
    """
    import os

    train_model = {}
    for folder in os.listdir(path):
        train_model[folder] = []
        for filename in os.listdir(path + folder + '/'):
            train_model[folder].append(file_to_doc_model(path + folder + '/' + filename))
    return train_model

def get_prior(train_model):
    """
    ulaz:
    -train_model: trenirani model kojeg vraća funkcija build_train_model()

    izlaz:
    -prior: je rječnik čiji su ključevi klase, a vrijednosti prior vjerojatnosti za svaku klasu
    prior vjerojatnost neke klase je omjer broja dokumenata u toj klasi i ukupnog broja dokumenata u svim klasama

    P'(c) = Nc/N

      c- klasa
      Nc - broj dokumenata klase c
      N - broj svih dokumenata
    """
    total = sum(len(docs) for docs in train_model.values())
    return {cls: len(docs) / total for cls, docs in train_model.items()}

def get_megadoc_model(train_model):
    """
    ulaz:
    -train_model: trenirani model kojeg vraća funkcija build_train_model()

    izlaz:
    -megadoc_model: je rječnik čiji su ključevi klase, a vrijednosti megadokumenti kao unigrami
    nastali "spajanjem" svih unigrama iz treniranog modela za određenu klasu
    """
    megadoc_model = {}
    for cls, docs in train_model.items():
        megadoc_model[cls] = {}
        for doc in docs:
            for word, freq in doc.items():
                megadoc_model[cls][word] = megadoc_model[cls].get(word, 0) + freq
    return megadoc_model

def get_vocabulary(megadoc_model):
    """
    ulaz:
    -megadoc_model: model megadokumenta

    izlaz:
    -rječnik: skup svih riječi iz svih megadokumenata u modelu megadokumenata
    """
    vocabulary = set()
    for megadoc in megadoc_model.values():
        vocabulary |= set(megadoc)
    return vocabulary

def get_likelihood(megadoc_model, test_model):
    """
    ulaz:
    -megadoc_model: model megadokumenata
    -test_model: model dokumenta za testiranje (predstavljen kao unigram)

    izlaz:
    -uvjetna vjerojatnost P(w|c) pojavljivanja riječi w iz testnog modela za svaku klasu c

    Uvjetna vjerojatnost po dodaj-1 izglađivanju:

    P(w|c) = (br(w,c) + 1) / (br(c) + |V|)

      br(w,c) - broj pojavljivanja riječi w u dokumentima klase c
      br(c) - broj svih riječi u dokumentima klase c
      |V| - broj riječi u rječniku
    """
    vocabulary = get_vocabulary(megadoc_model)
    likelihood = {}
    for word in test_model:
        for cls, megadoc in megadoc_model.items():
            likelihood[(word, cls)] = (megadoc.get(word, 0) + 1) /  (sum(megadoc.values()) + len(vocabulary))
    return likelihood

def get_posterior(prior, likelihood, test_model):
    """
    ulaz:
    -prior: prior vjerojatnosti P(c)
    -likelihood: uvjetne vjerojatnosti P(w|c)
    -test_model: model dokumenta za testiranje (predstavljen kao unigram)

    izlaz:
    -uvjetne vjerojatnosti P(c|d) da se dokument d (testni model) nalazi u klasi c
     uvjetna vjerojatnost je rječnik čiji su ključevi klase c, a vrijednosti P(c|d)

    P(c|d) = P(c) * (umnožak svih P(c|w) za svaku riječ w iz d)

    Napomena: koristiti logaritamski prostor jer su uvjetne vjerojatnosti mali realni brojevi
    Stoga se formula od P(c|d) svodi na

    log(P(c)) + (zbroj svih log(P(c|w)) za svaku riječ w iz d)
    """
    posterior = {}
    for cls in prior:
        posterior[cls] = math.log(prior[cls])
        for word, freq in test_model.items():
            posterior[cls] += freq * math.log(likelihood[(word, cls)])
        posterior[cls] = round(posterior[cls], 5)
    return posterior


def classify(train_model, test_model):
    """
    ulaz:
    -train_model: trenirani model
    -test_model: model dokumenta za testiranje (predstavljen kao unigram)
    izlaz:
    -klasa: klasa kojoj pripada testni model

    Koraci:
    1. stvoriti model megadokumenta - koristiti funkciju get_megadoc_model()
    2. stvoriti prior vjerojatnosti - koristiti funkciju get_prior()
    3. stvoriti uvjetne vjerojatnosti za testni model - koristiti funkciju get_likelihood()
    4. stvoriti posterior vjerojatnosti za testni model - koristiti funkciju get_posterior()
    5. iz posterior vjerojatnosti izabrati i vratiti onu s najvećom vjerojatnošću
    """
    megadoc_model = get_megadoc_model(train_model)

    prior = get_prior(train_model)
    likelihood = get_likelihood(megadoc_model, test_model)
    posterior = get_posterior(prior, likelihood, test_model)

    choices = sorted(posterior, key = lambda x: posterior[x], reverse = True)
    return choices[0]


################################################################################
###                       FUNKCIJE ZA TESTIRANJE                             ###
################################################################################

def testname(func):
    print()
    print(func.__name__.upper())
    print('#'*60)

def test(func, input, output = None):
    def reformat(data):
        maxlen = 80
        maxdict = 10
        maxlist = 10
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            return type(data)(reformat(el) for el in list(data)[:maxlist])
        if isinstance(data, dict):
            return type(data)((k, reformat(data[k])) for k in sorted(data)[:maxdict])
        return data

    import copy
    input_copy = copy.deepcopy(input)
    result = func(*input)

    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    print('%s\t%s%s \n\t=> %s\n\t%s= %s\n' % (success, func.__name__, reformat(str(reformat(input_copy))), reformat(output), success_rel , reformat(result)))
    return result

################################################################################
###                           TESTOVI                                        ###
################################################################################

TRAIN_PATH = 'train/'
TEST_PATH = 'test/'

testname(file_to_doc_model)
test(file_to_doc_model, (TRAIN_PATH + 'afrika/afrika12.txt', ), {'argentina': 1, 'burundi': 1, 'faso': 1, 'brazil': 1, 'gana': 2, 'južnoafrička': 1, 'kongo': 2, 'zimbabve': 1, 'egipat': 1, 'republika': 2, 'burkina': 1, 'kolumbija': 1})
test(file_to_doc_model, (TRAIN_PATH + 'australija/australija03.txt', ), {'palau': 1, 'panama': 2, 'vanuatu': 2, 'sudan': 1, 'novi': 1, 'zeland': 1, 'libanon': 1, 'belize': 1, 'slovačka': 1, 'tuvalu': 1, 'etiopija': 1, 'kiribati': 1, 'sveta': 1, 'maršalovi': 2, 'papua': 1, 'nizozemska': 2, 'nauru': 6, 'samoa': 2, 'tonga': 1, 'nova': 1, 'lanka': 1, 'tajvan': 1, 'gvatemala': 2, 'haiti': 1, 'gvineja': 1, 'otoci': 5, 'šri': 1, 'turska': 1, 'lesoto': 1, 'kanada': 1, 'honduras': 1, 'liberija': 1, 'solomonski': 3, 'savezne': 3, 'vijetnam': 1, 'azerbejdžan': 1, 'lucija': 1, 'australija': 1, 'države': 3, 'butan': 1, 'kazahstan': 1, 'mikronezije': 3})
test(file_to_doc_model, (TRAIN_PATH + 'južna_amerika/južna_amerika13.txt', ), {'paragvaj': 1, 'vanuatu': 1, 'solomonski': 1, 'brazil': 1, 'kolumbija': 1, 'čile': 3, 'venezuela': 1, 'otoci': 1, 'fidži': 2, 'australija': 1, 'surinam': 1, 'urugvaj': 1, 'gvajana': 2, 'peru': 3})

train_model = build_train_model(TRAIN_PATH)

testname(get_prior)
prior = test(get_prior, (train_model, ), {'AFRIKA': 0.22580645161290322, 'AUSTRALIJA': 0.18548387096774194, 'SJEVERNA_AMERIKA': 0.20967741935483872, 'AZIJA': 0.1774193548387097, 'JUŽNA_AMERIKA': 0.11290322580645161, 'EUROPA': 0.08870967741935484})

testname(get_megadoc_model)
megadoc_model = test(get_megadoc_model, (train_model, ), {'AZIJA': {'kazahstan': 23, 'tanzanija': 4, 'azerbejdžan': 24, 'andora': 1, 'šri': 20, 'kostarika': 2, 'japan': 24, 'kolumbija': 6, 'maroko': 5, 'uzbekistan': 9, 'finska': 2, 'vijetnam': 11, 'irska': 1, 'island': 3, 'ekvador': 3, 'češka': 1, 'kamerun': 3, 'kirgistan': 25, 'ukrajina': 3, 'arapski': 15, 'gambija': 5, 'monako': 1, 'kuvajt': 23, 'tunis': 1, 'malta': 1, 'mianmar': 16, 'bosna': 2, 'kongo': 7, 'tuvalu': 2, 'estonija': 2, 'senegal': 4, 'somalija': 2, 'sirija': 16, 'zapadna': 1, 'albanija': 3, 'gruzija': 18, 'sahara': 1, 'surinam': 7, 'lihtenštajn': 4, 'tajvan': 16, 'panama': 8, 'mađarska': 4, 'sejšeli': 3, 'emirati': 15, 'kraljevstvo': 3, 'argentina': 2, 'tonga': 7, 'kambodža': 30, 'egipat': 4, 'sveti': 13, 'indija': 22, 'kristofor': 3, 'čile': 3, 'zambija': 4, 'armenija': 14, 'kenija': 5, 'burma': 14, 'sveta': 5, 'bahrein': 17, 'nigerija': 1, 'lucija': 5, 'sijera': 2, 'turska': 18, 'belize': 4, 'kiribati': 2, 'slovačka': 1, 'obala': 1, 'ujedinjeno': 3, 'filipini': 11, 'novi': 6, 'dominikanska': 5, 'makedonija': 1, 'mali': 4, 'italija': 1, 'demokratska': 3, 'tajland': 22, 'samoa': 6, 'luksemburg': 1, 'meksiko': 1, 'trinidad': 1, 'faso': 2, 'dominika': 4, 'fidži': 6, 'princip': 5, 'malavi': 3, 'cipar': 1, 'gvajana': 3, 'mauricijus': 3, 'toma': 5, 'angola': 5, 'libija': 3, 'srednjoafrička': 3, 'liberija': 4, 'švedska': 4, 'otoci': 5, 'bolivija': 6, 'mongolija': 24, 'hercegovina': 2, 'zeland': 6, 'grenada': 3, 'portugal': 2, 'litva': 3, 'burkina': 2, 'afganistan': 25, 'haiti': 4, 'rusija': 1, 'ruanda': 3, 'južni': 2, 'iran': 25, 'američke': 5, 'barbuda': 4, 'libanon': 17, 'togo': 2, 'leone': 2, 'mikronezije': 3, 'ujedinjeni': 15, 'brunej': 16, 'bangladeš': 18, 'namibija': 3, 'ekvatorska': 4, 'džibuti': 1, 'madagaskar': 3, 'singapur': 23, 'mauritanija': 1, 'sjedinjene': 5, 'republika': 14, 'nepal': 26, 'bjelokosti': 1, 'nova': 4, 'australija': 7, 'države': 8, 'antigva': 4, 'maldivi': 15, 'lanka': 20, 'južna': 19, 'oman': 18, 'gvineja': 14, 'bahami': 2, 'arabija': 18, 'irak': 17, 'papua': 4, 'tadžikistan': 13, 'gora': 1, 'laos': 17, 'čad': 5, 'san': 2, 'saudijska': 18, 'nizozemska': 3, 'svazi': 3, 'kina': 18, 'etiopija': 4, 'vincent': 5, 'lesoto': 1, 'urugvaj': 4, 'marino': 2, 'poljska': 1, 'gvatemala': 5, 'francuska': 6, 'grenadini': 5, 'koreja': 51, 'burundi': 3, 'peru': 2, 'jemen': 29, 'komori': 3, 'crna': 1, 'maršalovi': 3, 'vanuatu': 5, 'srbija': 1, 'katar': 20, 'španjolska': 1, 'brazil': 7, 'barbados': 7, 'malezija': 15, 'jordan': 21, 'kuba': 8, 'solomonski': 2, 'alžir': 3, 'nikaragva': 3, 'rumunjska': 3, 'južnoafrička': 2, 'palau': 2, 'kanada': 4, 'salvador': 4, 'uganda': 4, 'venezuela': 4, 'slovenija': 4, 'honduras': 8, 'i': 20, 'nauru': 8, 'niger': 3, 'paragvaj': 2, 'sjeverna': 14, 'jamajka': 7, 'pakistan': 17, 'sudan': 5, 'timor': 23, 'eritreja': 1, 'norveška': 3, 'latvija': 4, 'indonezija': 21, 'hrvatska': 3, 'kosovo': 4, 'švicarska': 3, 'gabon': 1, 'turkmenistan': 20, 'bisau': 4, 'izrael': 16, 'tobago': 1, 'benin': 2, 'gana': 3, 'istočni': 23, 'butan': 20, 'savezne': 3, 'nevis': 3, 'mozambik': 2, 'bocvana': 5}, 'JUŽNA_AMERIKA': {'američke': 2, 'barbuda': 1, 'tuvalu': 2, 'azerbejdžan': 1, 'tunis': 1, 'kostarika': 2, 'ekvatorska': 1, 'džibuti': 1, 'kolumbija': 20, 'togo': 2, 'madagaskar': 1, 'singapur': 2, 'eritreja': 2, 'sjedinjene': 2, 'island': 1, 'republika': 2, 'ekvador': 18, 'austrija': 1, 'kamerun': 1, 'nova': 2, 'ukrajina': 1, 'australija': 2, 'gambija': 3, 'vanuatu': 2, 'peru': 21, 'danska': 1, 'antigva': 1, 'zimbabve': 2, 'gvineja': 7, 'kongo': 2, 'arabija': 1, 'estonija': 1, 'papua': 2, 'fidži': 4, 'laos': 1, 'čad': 1, 'gruzija': 1, 'san': 3, 'saudijska': 1, 'surinam': 17, 'lihtenštajn': 1, 'panama': 2, 'mađarska': 1, 'sejšeli': 1, 'etiopija': 2, 'lesoto': 1, 'urugvaj': 20, 'argentina': 21, 'tonga': 1, 'marino': 3, 'cipar': 3, 'egipat': 1, 'gvatemala': 3, 'francuska': 1, 'države': 2, 'čile': 16, 'brazil': 28, 'komori': 1, 'burma': 1, 'maršalovi': 1, 'bahrein': 2, 'belize': 3, 'kiribati': 1, 'slovačka': 1, 'barbados': 4, 'bjelorusija': 1, 'nauru': 1, 'novi': 3, 'solomonski': 1, 'njemačka': 2, 'nikaragva': 2, 'kuba': 2, 'finska': 1, 'palau': 1, 'toma': 1, 'kanada': 1, 'salvador': 1, 'dominika': 3, 'zapadna': 1, 'venezuela': 24, 'princip': 1, 'kambodža': 1, 'gvajana': 18, 'i': 2, 'mauricijus': 1, 'niger': 2, 'paragvaj': 19, 'angola': 1, 'otoci': 2, 'sudan': 1, 'sveti': 1, 'nepal': 1, 'ruanda': 1, 'latvija': 1, 'indonezija': 1, 'bolivija': 15, 'zeland': 3, 'kosovo': 1, 'maldivi': 1, 'portugal': 1, 'bisau': 2, 'jemen': 1, 'haiti': 1, 'bocvana': 1, 'iran': 1, 'sahara': 1}, 'AFRIKA': {'kazahstan': 6, 'maroko': 19, 'azerbejdžan': 1, 'tunis': 36, 'libanon': 5, 'kostarika': 6, 'japan': 6, 'kolumbija': 10, 'tanzanija': 26, 'uzbekistan': 6, 'finska': 3, 'vijetnam': 3, 'irska': 6, 'island': 7, 'ekvador': 10, 'češka': 4, 'austrija': 4, 'kamerun': 46, 'somalija': 23, 'ukrajina': 2, 'arapski': 4, 'gambija': 26, 'monako': 3, 'leone': 24, 'danska': 3, 'kuvajt': 2, 'zimbabve': 31, 'malta': 1, 'mianmar': 6, 'bosna': 3, 'kongo': 84, 'tuvalu': 3, 'andora': 6, 'estonija': 4, 'senegal': 25, 'sirija': 6, 'zapadna': 24, 'albanija': 4, 'gruzija': 4, 'sahara': 24, 'surinam': 10, 'lihtenštajn': 5, 'tajvan': 5, 'panama': 6, 'mađarska': 6, 'sejšeli': 33, 'emirati': 4, 'kraljevstvo': 4, 'belgija': 4, 'argentina': 7, 'tonga': 6, 'kambodža': 6, 'egipat': 29, 'sveti': 32, 'indija': 4, 'kristofor': 5, 'čile': 5, 'zambija': 25, 'armenija': 5, 'kenija': 35, 'burma': 7, 'sveta': 5, 'bahrein': 7, 'lucija': 5, 'sijera': 24, 'nigerija': 25, 'belize': 5, 'kiribati': 5, 'slovačka': 4, 'obala': 34, 'ujedinjeno': 4, 'filipini': 3, 'novi': 4, 'dominikanska': 6, 'makedonija': 7, 'mali': 29, 'italija': 8, 'demokratska': 22, 'tajland': 2, 'singapur': 6, 'meksiko': 7, 'trinidad': 4, 'faso': 23, 'dominika': 2, 'fidži': 2, 'princip': 22, 'malavi': 23, 'cipar': 3, 'gvajana': 9, 'mauricijus': 26, 'toma': 22, 'angola': 32, 'gvatemala': 4, 'srednjoafrička': 36, 'liberija': 27, 'nepal': 6, 'pakistan': 8, 'bolivija': 10, 'mongolija': 3, 'hercegovina': 3, 'zeland': 4, 'grenada': 9, 'sudan': 60, 'litva': 9, 'koreja': 16, 'burkina': 23, 'afganistan': 2, 'bugarska': 1, 'haiti': 3, 'rusija': 7, 'ruanda': 27, 'iran': 6, 'gabon': 33, 'američke': 3, 'barbuda': 3, 'šri': 5, 'togo': 30, 'kirgistan': 6, 'mikronezije': 3, 'ujedinjeni': 4, 'brunej': 5, 'bangladeš': 3, 'namibija': 30, 'ekvatorska': 36, 'džibuti': 26, 'madagaskar': 20, 'vatikan': 4, 'mauritanija': 28, 'sjedinjene': 3, 'republika': 139, 'švedska': 5, 'bjelokosti': 34, 'nova': 5, 'kina': 3, 'države': 6, 'antigva': 3, 'maldivi': 5, 'lanka': 5, 'oman': 7, 'gvineja': 109, 'bahami': 8, 'arabija': 5, 'irak': 4, 'papua': 5, 'tadžikistan': 6, 'laos': 1, 'čad': 20, 'san': 4, 'saudijska': 5, 'nizozemska': 5, 'svazi': 31, 'turska': 8, 'etiopija': 32, 'vincent': 5, 'lesoto': 31, 'urugvaj': 5, 'marino': 4, 'poljska': 6, 'libija': 29, 'francuska': 5, 'grenadini': 5, 'južna': 7, 'burundi': 32, 'peru': 10, 'jemen': 6, 'komori': 31, 'maršalovi': 6, 'vanuatu': 2, 'srbija': 6, 'katar': 5, 'španjolska': 2, 'brazil': 13, 'barbados': 2, 'bjelorusija': 4, 'malezija': 3, 'jordan': 5, 'moldova': 3, 'južni': 29, 'alžir': 21, 'nikaragva': 6, 'rumunjska': 1, 'kuba': 5, 'južnoafrička': 34, 'palau': 4, 'butan': 6, 'solomonski': 5, 'kanada': 5, 'njemačka': 3, 'salvador': 8, 'uganda': 31, 'venezuela': 7, 'slovenija': 3, 'honduras': 8, 'i': 42, 'nauru': 6, 'niger': 22, 'paragvaj': 9, 'sjeverna': 5, 'jamajka': 4, 'otoci': 11, 'portugal': 5, 'timor': 6, 'eritreja': 30, 'norveška': 8, 'latvija': 7, 'indonezija': 5, 'hrvatska': 10, 'kosovo': 5, 'švicarska': 9, 'luksemburg': 3, 'turkmenistan': 4, 'bisau': 28, 'izrael': 4, 'tobago': 4, 'benin': 28, 'gana': 36, 'istočni': 6, 'australija': 6, 'savezne': 3, 'samoa': 6, 'nevis': 5, 'mozambik': 24, 'bocvana': 29}, 'AUSTRALIJA': {'američke': 1, 'barbuda': 1, 'kazahstan': 1, 'tuvalu': 20, 'azerbejdžan': 2, 'kirgistan': 1, 'sveta': 2, 'mikronezije': 24, 'brunej': 2, 'iran': 1, 'šri': 2, 'ekvatorska': 2, 'oman': 1, 'kolumbija': 5, 'tanzanija': 1, 'uzbekistan': 1, 'kina': 1, 'singapur': 1, 'vijetnam': 2, 'sjedinjene': 1, 'demokratska': 1, 'ekvador': 3, 'maroko': 1, 'bjelokosti': 1, 'češka': 2, 'australija': 25, 'somalija': 2, 'nova': 20, 'ukrajina': 2, 'republika': 6, 'gambija': 1, 'države': 25, 'venezuela': 1, 'monako': 2, 'nizozemska': 3, 'maldivi': 2, 'lanka': 2, 'zimbabve': 2, 'južna': 4, 'mianmar': 1, 'gvineja': 24, 'kongo': 1, 'andora': 1, 'papua': 20, 'grčka': 1, 'zapadna': 2, 'albanija': 4, 'čad': 2, 'gruzija': 1, 'sahara': 2, 'surinam': 5, 'lihtenštajn': 2, 'antigva': 1, 'panama': 3, 'nigerija': 1, 'etiopija': 3, 'bosna': 1, 'vincent': 3, 'lesoto': 2, 'urugvaj': 2, 'belgija': 1, 'argentina': 5, 'tonga': 33, 'marino': 1, 'cipar': 1, 'gvatemala': 4, 'sveti': 5, 'grenadini': 3, 'koreja': 5, 'burundi': 2, 'čile': 3, 'brazil': 3, 'zambija': 1, 'kenija': 1, 'barbados': 1, 'burma': 1, 'maršalovi': 30, 'vanuatu': 24, 'lucija': 2, 'srbija': 1, 'katar': 1, 'turska': 2, 'belize': 1, 'kiribati': 21, 'slovačka': 4, 'obala': 1, 'bjelorusija': 2, 'mauricijus': 1, 'jordan': 1, 'novi': 17, 'dominikanska': 2, 'makedonija': 4, 'nikaragva': 2, 'rumunjska': 2, 'južnoafrička': 2, 'samoa': 22, 'crna': 1, 'palau': 22, 'solomonski': 25, 'paragvaj': 2, 'meksiko': 2, 'kanada': 3, 'vatikan': 1, 'njemačka': 2, 'salvador': 1, 'dominika': 1, 'fidži': 21, 'komori': 2, 'tajvan': 2, 'slovenija': 1, 'toma': 1, 'princip': 1, 'malavi': 1, 'honduras': 1, 'i': 7, 'nauru': 35, 'niger': 1, 'malta': 1, 'libanon': 1, 'angola': 1, 'gora': 1, 'otoci': 55, 'srednjoafrička': 1, 'sudan': 3, 'liberija': 1, 'švedska': 1, 'ruanda': 2, 'latvija': 1, 'togo': 1, 'bolivija': 3, 'hrvatska': 3, 'hercegovina': 1, 'zeland': 17, 'kosovo': 1, 'švicarska': 3, 'portugal': 1, 'litva': 1, 'gvajana': 4, 'izrael': 1, 'savezne': 24, 'kristofor': 1, 'butan': 1, 'haiti': 2, 'rusija': 1, 'san': 1, 'nevis': 1, 'južni': 2, 'peru': 6, 'finska': 2, 'bocvana': 2}, 'SJEVERNA_AMERIKA': {'kazahstan': 1, 'tanzanija': 1, 'azerbejdžan': 3, 'tunis': 1, 'libanon': 1, 'kostarika': 22, 'surinam': 3, 'kolumbija': 2, 'togo': 1, 'uzbekistan': 1, 'finska': 2, 'vijetnam': 2, 'island': 1, 'ekvador': 4, 'češka': 1, 'austrija': 1, 'kamerun': 1, 'kirgistan': 3, 'ukrajina': 4, 'gambija': 2, 'monako': 2, 'kuvajt': 6, 'zimbabve': 2, 'bosna': 1, 'kongo': 5, 'estonija': 2, 'senegal': 1, 'sirija': 2, 'zapadna': 1, 'albanija': 1, 'gruzija': 3, 'sahara': 1, 'japan': 1, 'lihtenštajn': 1, 'venezuela': 3, 'panama': 34, 'mađarska': 2, 'sejšeli': 2, 'kraljevstvo': 3, 'belgija': 1, 'srednjoafrička': 3, 'argentina': 6, 'tonga': 1, 'cipar': 2, 'egipat': 1, 'sveti': 56, 'indija': 4, 'kristofor': 31, 'čile': 8, 'zambija': 2, 'armenija': 1, 'kenija': 1, 'burma': 1, 'sveta': 35, 'vanuatu': 6, 'lucija': 35, 'sijera': 3, 'nigerija': 1, 'belize': 27, 'kiribati': 3, 'slovačka': 1, 'obala': 1, 'filipini': 4, 'novi': 1, 'dominikanska': 42, 'makedonija': 1, 'mali': 1, 'italija': 2, 'samoa': 2, 'meksiko': 27, 'trinidad': 27, 'faso': 1, 'dominika': 22, 'fidži': 3, 'princip': 1, 'malavi': 2, 'kambodža': 5, 'gvajana': 1, 'ujedinjeno': 3, 'toma': 1, 'angola': 3, 'libija': 1, 'jamajka': 28, 'liberija': 2, 'otoci': 6, 'bolivija': 6, 'mongolija': 2, 'hercegovina': 1, 'republika': 47, 'grenada': 26, 'sudan': 2, 'litva': 1, 'burkina': 1, 'bugarska': 1, 'haiti': 24, 'rusija': 2, 'iran': 3, 'američke': 24, 'barbuda': 20, 'šri': 2, 'tuvalu': 6, 'leone': 3, 'mikronezije': 2, 'bangladeš': 1, 'ekvatorska': 3, 'madagaskar': 3, 'vatikan': 4, 'mauritanija': 2, 'sjedinjene': 24, 'zeland': 1, 'bjelokosti': 1, 'nova': 6, 'australija': 1, 'države': 26, 'antigva': 20, 'maldivi': 3, 'lanka': 2, 'oman': 1, 'gvineja': 13, 'bahami': 33, 'arabija': 1, 'irak': 1, 'papua': 6, 'grčka': 5, 'tadžikistan': 3, 'gabon': 1, 'bahrein': 1, 'san': 3, 'saudijska': 1, 'nizozemska': 1, 'turkmenistan': 5, 'turska': 6, 'etiopija': 5, 'vincent': 24, 'urugvaj': 5, 'marino': 3, 'poljska': 4, 'gvatemala': 32, 'grenadini': 24, 'koreja': 4, 'peru': 5, 'benin': 2, 'komori': 1, 'crna': 2, 'maršalovi': 2, 'srbija': 2, 'katar': 1, 'brazil': 4, 'barbados': 38, 'bjelorusija': 2, 'malezija': 2, 'kuba': 29, 'solomonski': 4, 'nikaragva': 21, 'rumunjska': 4, 'moldova': 1, 'južnoafrička': 1, 'palau': 2, 'kanada': 21, 'njemačka': 2, 'salvador': 32, 'uganda': 1, 'tajvan': 2, 'slovenija': 8, 'honduras': 39, 'i': 104, 'nauru': 4, 'paragvaj': 4, 'sjeverna': 3, 'gora': 2, 'pakistan': 4, 'portugal': 5, 'timor': 2, 'eritreja': 2, 'norveška': 1, 'latvija': 3, 'indonezija': 1, 'kosovo': 1, 'švicarska': 5, 'luksemburg': 5, 'svazi': 4, 'bisau': 3, 'tobago': 27, 'mozambik': 3, 'istočni': 2, 'savezne': 2, 'nevis': 31}, 'EUROPA': {'kazahstan': 2, 'maroko': 4, 'azerbejdžan': 1, 'tunis': 1, 'libanon': 1, 'kostarika': 3, 'japan': 5, 'kolumbija': 3, 'tanzanija': 2, 'uzbekistan': 4, 'finska': 7, 'vijetnam': 4, 'irska': 20, 'island': 15, 'ekvador': 2, 'češka': 11, 'austrija': 15, 'kamerun': 2, 'somalija': 2, 'ukrajina': 17, 'gambija': 4, 'monako': 12, 'danska': 8, 'kuvajt': 5, 'zimbabve': 4, 'malta': 10, 'mianmar': 2, 'bosna': 16, 'kongo': 9, 'estonija': 11, 'senegal': 6, 'sirija': 2, 'zapadna': 4, 'albanija': 18, 'sahara': 4, 'surinam': 7, 'lihtenštajn': 8, 'venezuela': 5, 'panama': 3, 'mađarska': 13, 'sejšeli': 1, 'kraljevstvo': 14, 'belgija': 18, 'argentina': 3, 'tonga': 4, 'cipar': 8, 'egipat': 4, 'sveti': 4, 'indija': 2, 'čile': 4, 'zambija': 2, 'armenija': 1, 'kenija': 6, 'burma': 1, 'vanuatu': 3, 'sijera': 5, 'nigerija': 5, 'kiribati': 1, 'slovačka': 6, 'crna': 13, 'mauricijus': 4, 'filipini': 2, 'novi': 3, 'dominikanska': 1, 'njemačka': 17, 'mali': 3, 'italija': 14, 'demokratska': 5, 'tajland': 4, 'samoa': 2, 'luksemburg': 14, 'meksiko': 2, 'trinidad': 1, 'faso': 1, 'dominika': 3, 'fidži': 7, 'princip': 2, 'malavi': 4, 'kambodža': 2, 'gvajana': 8, 'ujedinjeno': 14, 'toma': 2, 'angola': 5, 'libija': 2, 'gora': 13, 'liberija': 4, 'nepal': 1, 'pakistan': 2, 'bolivija': 6, 'mongolija': 2, 'srednjoafrička': 2, 'zeland': 3, 'grenada': 1, 'sudan': 3, 'litva': 8, 'burkina': 1, 'bugarska': 15, 'rusija': 18, 'ruanda': 2, 'južni': 1, 'američke': 1, 'barbuda': 3, 'šri': 1, 'tuvalu': 6, 'jemen': 2, 'leone': 5, 'mikronezije': 4, 'brunej': 4, 'bangladeš': 2, 'namibija': 2, 'ekvatorska': 4, 'džibuti': 2, 'madagaskar': 4, 'vatikan': 13, 'sjedinjene': 1, 'republika': 12, 'švedska': 13, 'bjelokosti': 1, 'čad': 4, 'nova': 1, 'kina': 2, 'države': 5, 'nizozemska': 20, 'maldivi': 1, 'lanka': 1, 'južna': 3, 'oman': 4, 'gvineja': 10, 'arabija': 5, 'irak': 1, 'papua': 1, 'grčka': 17, 'tadžikistan': 5, 'laos': 2, 'andora': 9, 'bahrein': 2, 'san': 11, 'saudijska': 5, 'singapur': 1, 'antigva': 3, 'svazi': 2, 'turska': 16, 'etiopija': 1, 'vincent': 2, 'lesoto': 5, 'urugvaj': 3, 'marino': 11, 'poljska': 11, 'gvatemala': 1, 'francuska': 12, 'grenadini': 2, 'koreja': 9, 'burundi': 1, 'peru': 3, 'mozambik': 3, 'komori': 3, 'obala': 1, 'maršalovi': 4, 'kirgistan': 2, 'srbija': 11, 'katar': 2, 'togo': 1, 'gana': 2, 'brazil': 9, 'barbados': 1, 'bjelorusija': 13, 'malezija': 3, 'jordan': 2, 'moldova': 13, 'solomonski': 6, 'alžir': 3, 'nikaragva': 2, 'rumunjska': 16, 'kuba': 1, 'južnoafrička': 1, 'palau': 5, 'butan': 2, 'kanada': 3, 'makedonija': 13, 'uganda': 2, 'tajvan': 3, 'slovenija': 15, 'honduras': 3, 'i': 24, 'nauru': 2, 'niger': 1, 'hercegovina': 16, 'paragvaj': 6, 'sjeverna': 3, 'jamajka': 2, 'otoci': 10, 'portugal': 17, 'timor': 3, 'eritreja': 3, 'norveška': 16, 'latvija': 11, 'indonezija': 3, 'hrvatska': 16, 'kosovo': 15, 'švicarska': 19, 'gabon': 3, 'turkmenistan': 4, 'bisau': 2, 'izrael': 2, 'tobago': 1, 'benin': 3, 'španjolska': 12, 'istočni': 3, 'australija': 3, 'savezne': 4, 'bocvana': 2}})

testname(get_vocabulary)
vocabulary = test(get_vocabulary, (megadoc_model, ), {'kambodža', 'salvador', 'sirija', 'andora', 'ekvatorska', 'nevis', 'libija', 'kraljevstvo', 'tajland', 'ukrajina', 'norveška', 'malezija', 'gora', 'malta', 'zapadna', 'makedonija', 'mađarska', 'kuba', 'irska', 'albanija', 'ruanda', 'litva', 'nepal', 'sveta', 'mozambik', 'demokratska', 'brazil', 'surinam', 'čile', 'barbados', 'otoci', 'tajvan', 'bahami', 'ujedinjeni', 'irak', 'rusija', 'namibija', 'grčka', 'luksemburg', 'gana', 'oman', 'sveti', 'panama', 'armenija', 'šri', 'malavi', 'madagaskar', 'švedska', 'republika', 'njemačka', 'gvajana', 'niger', 'burkina', 'dominikanska', 'meksiko', 'maldivi', 'hrvatska', 'maroko', 'crna', 'gvatemala', 'kanada', 'timor', 'indija', 'lihtenštajn', 'monako', 'zeland', 'italija', 'novi', 'vanuatu', 'faso', 'bjelorusija', 'nauru', 'zimbabve', 'maršalovi', 'danska', 'vincent', 'marino', 'bolivija', 'turkmenistan', 'jordan', 'češka', 'argentina', 'rumunjska', 'australija', 'japan', 'nikaragva', 'saudijska', 'benin', 'urugvaj', 'slovenija', 'hercegovina', 'kostarika', 'sejšeli', 'španjolska', 'antigva', 'lesoto', 'latvija', 'libanon', 'kamerun', 'emirati', 'savezne', 'venezuela', 'tadžikistan', 'katar', 'trinidad', 'estonija', 'filipini', 'kazahstan', 'vatikan', 'kiribati', 'cipar', 'nigerija', 'bjelokosti', 'dominika', 'ekvador', 'i', 'mianmar', 'gvineja', 'kina', 'srbija', 'indonezija', 'turska', 'belize', 'burma', 'vijetnam', 'južnoafrička', 'kuvajt', 'nova', 'haiti', 'džibuti', 'portugal', 'sudan', 'sijera', 'palau', 'srednjoafrička', 'kolumbija', 'togo', 'sahara', 'fidži', 'leone', 'arabija', 'afganistan', 'grenada', 'obala', 'belgija', 'bugarska', 'peru', 'iran', 'kristofor', 'tobago', 'burundi', 'bocvana', 'slovačka', 'francuska', 'azerbejdžan', 'čad', 'liberija', 'mongolija', 'solomonski', 'butan', 'samoa', 'zambija', 'brunej', 'lucija', 'austrija', 'tonga', 'papua', 'jemen', 'egipat', 'alžir', 'američke', 'bosna', 'istočni', 'države', 'svazi', 'gruzija', 'koreja', 'toma', 'barbuda', 'kongo', 'island', 'izrael', 'san', 'arapski', 'nizozemska', 'mali', 'ujedinjeno', 'tunis', 'etiopija', 'moldova', 'uganda', 'bangladeš', 'švicarska', 'grenadini', 'jamajka', 'bisau', 'mauricijus', 'laos', 'uzbekistan', 'lanka', 'poljska', 'tuvalu', 'pakistan', 'singapur', 'angola', 'finska', 'sjedinjene', 'paragvaj', 'južni', 'honduras', 'gabon', 'mauritanija', 'kenija', 'somalija', 'kirgistan', 'princip', 'bahrein', 'komori', 'sjeverna', 'senegal', 'tanzanija', 'mikronezije', 'gambija', 'eritreja', 'južna', 'kosovo'})

test_model_01 = file_to_doc_model(TEST_PATH + 'test01.txt')
test_model_02 = file_to_doc_model(TEST_PATH + 'test02.txt')

testname(get_likelihood)
likelihood_01 = test(get_likelihood, (megadoc_model, test_model_01), {('kina', 'AFRIKA'): 0.0012907389480477573, ('indija', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('japan', 'AZIJA'): 0.01337613697164259, ('indija', 'AFRIKA'): 0.0016134236850596966, ('japan', 'EUROPA'): 0.004195804195804196, ('kina', 'AZIJA'): 0.010165864098448368, ('japan', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('japan', 'AUSTRALIJA'): 0.0010235414534288639, ('indija', 'EUROPA'): 0.002097902097902098, ('indija', 'AUSTRALIJA'): 0.0010235414534288639, ('indija', 'AZIJA'): 0.012306046013911182, ('japan', 'SJEVERNA_AMERIKA'): 0.0011976047904191617, ('japan', 'AFRIKA'): 0.002258793159083575, ('kina', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('indija', 'SJEVERNA_AMERIKA'): 0.0029940119760479044, ('kina', 'AUSTRALIJA'): 0.0020470829068577278, ('kina', 'EUROPA'): 0.002097902097902098, ('kina', 'SJEVERNA_AMERIKA'): 0.0005988023952095808})
likelihood_02 = test(get_likelihood, (megadoc_model, test_model_02), {('koreja', 'EUROPA'): 0.006993006993006993, ('čile', 'AFRIKA'): 0.001936108422071636, ('češka', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('koreja', 'AZIJA'): 0.027822364901016586, ('njemačka', 'EUROPA'): 0.012587412587412588, ('hrvatska', 'SJEVERNA_AMERIKA'): 0.0005988023952095808, ('hrvatska', 'EUROPA'): 0.011888111888111888, ('hrvatska', 'AFRIKA'): 0.0035495321071313327, ('koreja', 'AFRIKA'): 0.005485640529202969, ('njemačka', 'AZIJA'): 0.0005350454788657035, ('čile', 'SJEVERNA_AMERIKA'): 0.005389221556886228, ('bosna', 'SJEVERNA_AMERIKA'): 0.0011976047904191617, ('kina', 'SJEVERNA_AMERIKA'): 0.0005988023952095808, ('češka', 'AFRIKA'): 0.0016134236850596966, ('bosna', 'AUSTRALIJA'): 0.0020470829068577278, ('italija', 'SJEVERNA_AMERIKA'): 0.0017964071856287425, ('njemačka', 'JUŽNA_AMERIKA'): 0.004901960784313725, ('njemačka', 'AUSTRALIJA'): 0.0030706243602865915, ('italija', 'AUSTRALIJA'): 0.0010235414534288639, ('hrvatska', 'AUSTRALIJA'): 0.0040941658137154556, ('češka', 'SJEVERNA_AMERIKA'): 0.0011976047904191617, ('češka', 'EUROPA'): 0.008391608391608392, ('češka', 'AUSTRALIJA'): 0.0030706243602865915, ('bosna', 'AZIJA'): 0.0016051364365971107, ('čile', 'JUŽNA_AMERIKA'): 0.027777777777777776, ('čile', 'EUROPA'): 0.0034965034965034965, ('bosna', 'AFRIKA'): 0.0012907389480477573, ('njemačka', 'AFRIKA'): 0.0012907389480477573, ('italija', 'AFRIKA'): 0.002904162633107454, ('italija', 'EUROPA'): 0.01048951048951049, ('kina', 'AZIJA'): 0.010165864098448368, ('bosna', 'EUROPA'): 0.011888111888111888, ('češka', 'AZIJA'): 0.001070090957731407, ('kina', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('koreja', 'SJEVERNA_AMERIKA'): 0.0029940119760479044, ('kina', 'AUSTRALIJA'): 0.0020470829068577278, ('kina', 'EUROPA'): 0.002097902097902098, ('kina', 'AFRIKA'): 0.0012907389480477573, ('italija', 'AZIJA'): 0.001070090957731407, ('hrvatska', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('bosna', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('čile', 'AZIJA'): 0.002140181915462814, ('italija', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('hrvatska', 'AZIJA'): 0.002140181915462814, ('njemačka', 'SJEVERNA_AMERIKA'): 0.0017964071856287425, ('koreja', 'AUSTRALIJA'): 0.006141248720573183, ('koreja', 'JUŽNA_AMERIKA'): 0.0016339869281045752, ('čile', 'AUSTRALIJA'): 0.0040941658137154556})

testname(get_posterior)
test(get_posterior, (prior, likelihood_01, test_model_01), {'AFRIKA': -20.66294, 'EUROPA': -20.22969, 'SJEVERNA_AMERIKA': -21.52134, 'AZIJA': -15.02991, 'JUŽNA_AMERIKA': -21.43142, 'AUSTRALIJA': -21.6451})
test(get_posterior, (prior, likelihood_02, test_model_02), {'AFRIKA': -50.81034, 'AZIJA': -49.84133, 'SJEVERNA_AMERIKA': -53.53663, 'EUROPA': -41.78543, 'JUŽNA_AMERIKA': -49.58326, 'AUSTRALIJA': -48.61281})

testname(classify)
test(classify, (train_model, test_model_01), 'AZIJA')
test(classify, (train_model, test_model_02), 'EUROPA')