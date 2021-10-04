# coding=utf-8

import os
import math

DATA_PATH = './data/imdb1/'
STOPWORD_FILENAME = './data/english.stop'

def read_stopwords(filename):
    """
    ulaz:
    -filename: datoteka

    izlaz:
    -skup stop riječi iz datoteke
    """
    return set()

def read_document(filename, stopwords = set()):
    """
    ulaz:
    -filename: datoteka dokumenta
    -stopwords: skup stop riječi

    izlaz:
    -skup riječi iz datoteke koje nisu u stopwords
    """
    return []

def make_datasets(data_path, numfolds = 10):
    """
    ulaz:
    -data_path: putanja do datoteka
    izlaz:
    -lista oblika
    0: train: pos: [filename, filename, ...]
              neg: [filename, filename, ...]
       test: pos:  [filename, filename, ...]
             neg:  [filename, filename, ...]
    1: train: pos: [filename, filename, ...]
              neg: [filename, filename, ...]
       test: pos:  [filename, filename, ...]
             neg:  [filename, filename, ...]
    ...
    ...
    Svaki element liste je rječnik sa dva ključa "train" i "test"
    čije su vrijednosti rječnik s dva ključa "pos" i "neg" čije su
    vrijednosti lista datoteka koje su "pos" ili "neg" kritike
    """
    klasses = [klass for klass in os.listdir(data_path) if not klass.startswith('.')]
    datasets = []
    filenames = {klass: sorted(os.listdir(data_path + klass + '/')) for klass in klasses}
    for fold in range(numfolds):
        trains = {klass: [] for klass in klasses}
        tests = {klass: [] for klass in klasses}
        for klass in klasses:
            for filename in filenames[klass]:
                if filename[2] == str(fold):
                    tests[klass].append(data_path + klass + '/' + filename)
                else:
                    trains[klass].append(data_path + klass + '/' + filename)
        datasets.append({'train': trains, 'test': tests})
    return datasets

class NBClassifier(object):
    """
    Naivni Bayesov klasifikator
    """

    def __init__(self, klasses, stopwords = set()):
        """
        ulaz:
        -klasses: kolekcija klasa
        -stopwords: skup stop riječi

        Pojašnjenje atributa:
        - self.stopwords je skup riječi
        - self.klasses je skup klasa
        - self.documents je brojač dokumenata za svaku klasu
        - self.likelihood je brojač riječi svake klase,
          npr. ako je self.likelihood['pos']['lovely'] = 3
          znaći da se u svim dokumentima klase 'pos' 3 puta pojavljuje
          riječ 'lovely'
        - self.vocabulary je skup riječi iz svih dokumata od svih klasa
        """
        self.stopwords = stopwords
        self.klasses = set(klasses)
        self.documents = {klass: 0 for klass in klasses}
        self.likelihood = {klass: {} for klass in klasses}
        self.vocabulary = set()


    def add_train_doc(self, klass, filename):
        """
        ulaz:
        -klass: klasa dokumenta
        -filename: datoteka dokumenta

        koraci
        1. inkrementirati rječnik self.documents dane klase
        2. pročitati datoteku dokumenta koristeći read_document()
        3. za svaku riječ iz dokumenta:
             3.1. inkrementirati self.likelihood dane klase i dane riječi
             3.2. dodati riječ u self.vocabulary
        """
        pass

    def train(self):
        """
        Uvjetna vjerojatnost po dodaj-1 izglađivanju glasi:

        P(c|w) = (br(w,c) + 1) / (br(c) + |V|)

        br(w,c) - broj pojavljivanja riječi w u dokumentima klase c
        br(c) - broj svih riječi u dokumentima klase c
        |V| - broj riječi u rječniku

        Nazivnik (denominator) ove formule je

        br(c) + |V|

        koji je konstantan za svaku klasu c i neče ga biti potrebno ponovno
        izračunavati prilikom klasifikacije

        Koraci
        1. u self.prior izračunati prior vjerojatnost svake klase po formuli
            P'(c) = Nc/N

            c- klasa
            Nc - broj dokumenata klase c
            N - broj svih dokumenata

        2. u self.denominator izračunati vrijednost nazivika br(c) + |V|

           br(c) - broj svih riječi u dokumentima klase c (dobiva se iz self.likelihood)
           |V| - broj riječi u rječniku (dobiva se pomoću self.vocabulary)

           self.denominator je također rječnik čiji su ključevi klase

        """
        self.prior = {}
        self.denominator = {}

    def classify(self, filename):
        """
        ulaz:
        -filename: datoteka dokumenta koji se klasificira
        izlaz:
        -klass: predviđena klasa dokumenta

        Posterior vjerojatnost da dokument d pripada klasi c je

        P(c|d) = P(c) * (umnožak svih P(c|w) za svaku riječ w iz d)

        Napomena: koristiti logaritamski prostor jer su uvjetne vjerojatnosti mali realni brojevi
        Stoga se formula od P(c|d) svodi na

        log(P(c)) + (zbroj svih log(P(c|w)) za svaku riječ w iz d)

        Za izračuna P(c|w) vidi dokumentaciju od funkcije train()

        Na kraju se vraća ona klasa c čiji je P(c|d) maksimalan
        """
        return

def cross_validate(has_stopwords, counts):
    """
    ulaz:
    -has_stopwords: ima ili nema stop riječi
    -counts: lista očekivanog broja točno klasificiranih dokumenata za
             svaku unakrsnu podjelu podataka

    Koraci:
    1. Pripremi unakrsnu validaciju
    2. Ako ima stop riječi onda ih učitaj
    3. Za svaku unakrsnu podjelu podataka:
       3.1. Treniraj klasifikator na podacima za trening
       3.2. Klasificiraj na podacima za testiranje
       3.3. Izračunaj točnost klasifikatora za unakrsnu podjelu
    4. Izračunaj ukupnu točnost klasifikatora
    """
    print('[INFO] Preparing datasets...')
    datasets = make_datasets(DATA_PATH)
    if has_stopwords:
        print('[INFO] Reading stopwords...')
        stopwords = read_stopwords(STOPWORD_FILENAME)
    else:
        stopwords = set()
    print('[INFO] Training and classifying...')

    total_good, total_all = 0, 0
    for fold, dataset in enumerate(datasets):
        train, test = dataset['train'], dataset['test']
        classifier = NBClassifier(train.keys(), stopwords)

        # training
        for klass, filenames in train.items():
            for filename in filenames:
                classifier.add_train_doc(klass, filename)
        classifier.train()

        # evaluating
        count_good, count_all = 0, 0
        for klass, filenames in test.items():
            for filename in filenames:
                predicted_klass = classifier.classify(filename)
                count_good += 1 if predicted_klass == klass else 0
                count_all += 1
        total_good += count_good
        total_all += count_all

        success = count_good == counts[fold]
        success_txt = ' OK ' if success else ' X  '

        print('[%s] Fold %d: %d/%d\t%.1f%%' % (success_txt, fold, count_good, count_all, count_good/count_all * 100))

    print('[INFO] Accuracy %d/%d\t%.1f%%' % (total_good, total_all, total_good/total_all*100))

################################################################################
###                       FUNKCIJE ZA TESTIRANJE                             ###
################################################################################

def testname(func):
    print()

    print(func.__name__.upper())
    print('#'*60)

def reformat(data):
        maxlen = 80
        maxdict = 10
        maxlist = 10
        if type(data) is str:
            if len(data) > maxlen:
                return data[:maxlen] + '...'
        if isinstance(data, (tuple, list, set, frozenset)):
            if len(data) > maxlist:
                temp = [reformat(el) for el in list(data)[:maxlist]] + ['...']
                return type(data)(temp)
            else:
                return type(data)(reformat(el) for el in list(data))
        if isinstance(data, dict):
            return type(data)((k, reformat(data[k])) for k in sorted(data)[:maxdict])
        return data

def test(func, input, output = None):
    import copy
    input_copy = copy.deepcopy(input)
    result = func(*input)

    success = 'OK' if result == output else 'X'
    success_rel = '=' if result == output else '!'
    print('%s\t%s%s \n\t=> %s\n\t%s= %s\n' % (success, func.__name__, reformat(str(reformat(input_copy))), reformat(output), success_rel , reformat(result)))
    return result

def testclass(obj, method, input, outputs = {}):
    import copy
    input_copy = copy.deepcopy(input)
    method(*input)
    lines = []
    passed = True
    for attr in sorted(outputs):
        output = outputs[attr]

        if not hasattr(obj, attr):
            result = '???'
            passed = False
        else:
            result = getattr(obj, attr)
        passed = result == output
        success = 'OK' if result == output else 'X'
        success_rel = '=' if result == output else '!'
        lines.append('\t%s\t%s' % (success, attr))
        lines.append('\t=> %s\n\t%s= %s\n' % (reformat(output), success_rel , reformat(result)))
        #print('%s\t%s%s \n\t=> %s\n\t%s= %s\n' % (success, method.__name__, reformat(str(reformat(input_copy))), reformat(output), success_rel , reformat(result)))

    passed == 'OK' if passed else 'X'
    lines.insert(0, '%s\t%s%s' % (success, method.__name__, reformat(str(reformat(input_copy)))))
    for line in lines:
        print(line)

################################################################################
###                           TESTOVI                                        ###
################################################################################
datasets = make_datasets(DATA_PATH)

testname(read_stopwords)
stopwords = test(read_stopwords, (STOPWORD_FILENAME,), {'nine', 'willing', 'inc', 'because', 'edu', 'whenever', 'well', 'hence', 'may', 'seven', 'sometime', 'becomes', 'among', 'had', 'lest', 'containing', 'yourself', 'of', 'theirs', "i'll", 'said', 'down', 'p', 'hereby', 'sub', 'then', 'there', 'qv', 'nothing', 'is', 'tries', 'new', 'x', 'everywhere', 'otherwise', 'com', 'presumably', 'amongst', 'become', 'were', 'they', 'her', 'also', 'hers', 'second', 'tried', 'gone', 'two', 'wants', 'above', 'although', 'much', 'rd', 'f', 'was', 'have', 'has', 'just', 'thorough', 'took', 'particular', 'together', 'up', 'became', 'mean', 'anybody', "they're", 'former', 'only', 'follows', 'right', 'think', 'especially', 'we', 'not', 'concerning', 'which', 'despite', 'tends', 'course', "aren't", 'used', 'cant', 'formerly', 'anyways', 'usually', 'your', 'goes', 'having', 'here', 'nor', "what's", "c's", 'reasonably', 'a', 'see', 'theres', 'meanwhile', "we'll", 'how', "you'd", 'third', 'contain', 'brief', 'becoming', 'asking', 'r', 'liked', 'novel', 'me', 'for', 'its', 'unfortunately', 'elsewhere', 'uses', 'are', 'whereupon', 'overall', 'know', 'consider', 'help', 'uucp', 'furthermore', 'enough', 'according', 'anyway', 'latter', 'far', 'truly', "we've", 'definitely', 'keep', 'yet', 'mostly', 'behind', 'un', 'serious', 'doing', 'probably', 'though', 'what', 'must', 'our', 'say', 'contains', 'upon', 'provides', 'more', "don't", 'per', "t's", 'thereupon', 'unlikely', 'going', 'always', 'anything', 'currently', 'still', 'associated', 'obviously', 'and', 'very', 'described', 'better', 'do', "you'll", 'him', 'looks', 'hardly', "haven't", 'k', "they've", 'seriously', 'thereafter', 'nd', 'particularly', 'be', 'whom', 'out', 'like', 'welcome', 'able', 'go', 'gives', 'seeming', 'trying', 'anyone', 'each', 'inner', 'namely', 'he', 'to', 'thank', 'beyond', 'herein', 'm', 'useful', 'various', 'wherever', 'thus', 'l', 'ask', 'within', 'merely', "shouldn't", "that's", 'sometimes', "they'll", 'wherein', "where's", "ain't", 'gotten', 'somehow', 'ignored', 'therein', 'ever', 'yours', 'other', 'let', 'certain', 'changes', 'whereby', 'hither', 'allow', 'could', 'respectively', 'inward', 'wonder', 'under', 'someone', 'therefore', 'necessary', 'etc', 'in', 'least', 'awfully', 'relatively', 'shall', 'corresponding', 'should', 'appear', 'need', 'whither', 'non', 'looking', 'get', 'v', 'sorry', "wouldn't", 'whereas', 'lately', 'n', 'says', 'wish', 'soon', 'six', 'himself', 'entirely', 'got', "i'd", 'even', 'example', 'e', 'self', 'vs', 'several', 'considering', 'however', 'such', 'why', 'getting', 'happens', 'okay', 'some', "there's", 'towards', "hasn't", 'sent', 'th', "we're", 'few', 'seemed', 'believe', 'four', 'b', 'whereafter', 'three', 'who', 'aside', 'does', 'or', 'actually', 'placed', "doesn't", 'further', 'latterly', 'once', 'maybe', 'one', 'herself', 'indicate', 'normally', 'regardless', 'ones', 'already', 'name', 'eight', 'so', 'their', 'ex', 'after', 'while', 'u', "you've", 'available', 'g', 'keeps', 'unto', 'afterwards', 'near', 'later', 'those', 'certainly', 'j', 'o', 'went', 'since', 'plus', 'whole', 'less', 'consequently', 'now', 'd', 'known', 'thanx', 'w', 'yes', 'oh', 'alone', 'my', 'us', 'neither', 'below', 'taken', 'hereafter', 'nowhere', 'whence', 'off', 'where', 'ourselves', 'regarding', 'given', 'by', 'except', 'immediate', "isn't", 'forth', 'over', 'else', 'try', 'everything', 'via', 'inasmuch', 'ours', 'toward', 'often', 'y', 'until', 'using', 'perhaps', 'them', 'about', 'seems', 'gets', 'specified', 'knows', 'seen', 'without', 'cannot', 'appropriate', 'every', 'clearly', 'both', 'downwards', "a's", 'everybody', 'accordingly', 'cause', 'old', 'with', 'tell', 'i', 'anyhow', 'besides', "who's", 'that', 'following', 'can', 'itself', 'q', 'thru', 'these', 'little', 'the', 'viz', 'hi', 'first', 'against', 'somewhat', "weren't", 'next', 'kept', 'thanks', 'sup', 'themselves', "wasn't", 'sure', "he's", 'done', 'allows', 'fifth', 'twice', 'across', 'apart', 'own', 'before', 'at', 'nearly', 'during', 'ltd', 'noone', 'causes', 'from', 'followed', 'away', "couldn't", 'best', 'last', 'most', 'nobody', 'almost', "won't", 'either', 'you', "let's", 'many', 'thence', 'hereupon', 'exactly', 'somewhere', 'please', 'anywhere', 'another', 'insofar', 'quite', 'way', 'appreciate', 'ok', 'regards', 'outside', 'five', 'between', 'ought', 'whoever', 'specify', 'would', 'throughout', 'instead', "here's", 'no', 'z', 'through', 'c', 'secondly', "c'mon", 'she', 'really', "hadn't", 'into', 'if', 'ie', 'want', 'same', 'whether', 'all', 'any', 'indicated', "i'm", 'zero', 's', 'will', 'thats', 'myself', 'possible', 'sensible', 'co', 'on', 'but', 'an', 'again', 'take', 'value', 'et', 'h', 'mainly', 'specifying', 'beforehand', 'as', 'around', 'thoroughly', 'beside', 'been', 'moreover', 'different', 'somebody', 'might', "we'd", 'likely', 'indeed', 'eg', "they'd", 'rather', 'nevertheless', 'others', "can't", "you're", 'selves', 'howbeit', 'hopefully', 'did', 'whose', 'when', 'came', 'his', 'never', 'whatever', 'along', "it'll", 'seeing', 'this', 'it', "it'd", 'am', 'come', 'unless', 'everyone', "i've", 'something', 'than', 'use', 're', 'hello', 'que', 'thereby', 'indicates', 'none', 't', 'seem', 'needs', 'yourselves', "didn't", 'onto', 'greetings', 'saying', 'comes', "it's", 'being', 'saw', 'look', 'too'})

testname(read_document)
test(read_document, (datasets[0]['train']['pos'][0], ), set(['james', 'l', '.', 'brooks', ',', 'one', 'of', 'the', 'developers', 'of', 'the', 'simpsons', 'and', 'director', 'of', 'broadcast', 'news', ',', 'returns', 'to', 'the', 'big', 'screen', 'with', 'this', 'entertaining', ',', 'if', 'slightly', 'flawed', 'comedy', '.', 'nicholson', 'plays', 'melvin', 'udall', ',', 'probably', 'the', 'most', 'horrible', 'person', 'ever', 'on', 'the', 'screen', '.', "he's", 'racist', ',', 'homophobic', ',', 'and', 'never', 'has', 'a', 'good', 'word', 'to', 'say', 'to', 'anyone', '.', 'so', ',', 'nobody', 'talks', 'to', 'him', ',', 'except', 'waitress', 'carol', 'conelly', '(', 't', '.', 'v', 'sitcom', 'star', 'hunt', ',', 'who', 'was', 'last', 'seen', 'in', 'twister', ',', '1996', ')', '.', 'naturally', ',', 'udall', ',', 'conelly', 'and', 'gay', 'neighbor', 'simon', 'bishop', '(', 'kinnear', ')', 'who', 'nicholson', 'hates', ',', 'all', 'hit', 'it', 'off', 'in', 'the', 'end', '.', 'like', 'good', 'will', 'hunting', '(', '1997', ')', 'and', 'titanic', '(', '1997', ')', ',', 'even', 'though', 'the', 'outcome', 'is', 'completely', 'obvious', ',', 'as', 'good', 'as', 'it', 'gets', 'is', 'an', 'enjoyable', ',', 'funny', 'and', 'warm', 'comedy', '.', 'nicholson', 'is', 'hilarious', 'as', 'melvin', ',', 'churning', 'out', 'insults', 'with', 'superb', 'relish', '.', 'only', 'nicholson', 'could', 'get', 'away', 'with', 'the', 'lines', 'that', 'melvin', 'delivers', '.', 'hunt', 'is', 'also', 'good', 'as', 'waitress', 'carol', ',', 'and', 'easily', 'rises', 'to', 'the', 'challenge', 'of', 'nicholson', '.', "there's", 'also', '(', 'thankfully', ')', 'a', 'bit', 'of', 'chemistry', 'between', 'them', '.', 'kinnear', ',', 'as', 'the', 'gay', 'neighbor', ',', 'seems', 'to', 'have', 'a', 'slightly', 'underwritten', 'role', ',', "he's", 'more', 'of', 'a', 'plot', 'convience', 'than', 'a', 'character', '.', 'although', 'his', 'performance', 'is', 'good', ',', 'his', 'character', 'just', 'seems', 'to', 'exist', 'to', 'help', 'melvin', 'and', 'carol', 'come', 'together', '.', 'in', 'fact', ',', 'the', 'scene', 'stealer', 'is', "simon's", 'dog', ',', 'who', 'is', 'funnier', 'than', 'nicholson', '.', 'but', 'then', 'again', ',', 'pets', 'are', 'always', 'cute', 'on', 'screen', '.', 'providing', 'solid', 'support', 'is', 'cuba', 'gooding', ',', 'jnr', '(', 'jerry', 'maguire', ',', '1996', ')', 'and', 'yeardly', 'smith', '(', 'who', 'is', 'the', 'voice', 'of', 'lisa', 'simpsons', 'in', 'the', 'simpsons', ')', 'although', 'gooding', "isn't", 'as', 'good', 'as', 'is', 'character', 'in', 'maguire', ',', 'he', 'is', 'still', 'fun', '.', 'he', 'overacts', 'a', 'little', ',', 'but', 'not', 'so', 'much', 'as', 'to', 'be', 'annoying', '.', 'smith', 'is', 'also', 'good', ',', 'although', 'she', 'has', 'a', 'fairly', 'small', 'role', '.', 'even', 'director', 'lawrence', 'kasdan', '(', 'body', 'heat', ',', '1981', ')', 'makes', 'an', 'appearance', 'as', 'a', 'doctor', '.', 'but', 'this', 'is', 'primarily', 'nicholsons', 'film', ',', 'and', 'every', 'scene', "he's", 'in', ',', "he's", 'steals', 'it', '.', "he's", 'character', 'is', 'so', 'hateful', ',', 'though', ',', "it's", 'amazing', 'that', 'anyone', 'talks', 'to', 'him', 'at', 'all', ',', 'especially', 'carol', '.', 'and', 'this', 'is', 'the', 'films', 'main', 'problem', '.', "it's", 'totally', 'unbelievable', 'that', 'carol', 'would', 'ever', 'consider', 'liking', 'melvin', '.', 'she', "doesn't", 'fall', 'in', 'love', 'with', 'him', 'naturally', ',', 'the', 'film', 'forces', 'her', 'to', 'fall', 'in', 'love', 'with', 'him', '.', 'also', ',', 'melvins', 'character', 'seems', 'to', 'go', 'too', 'nice', ',', 'too', 'quickly', '.', 'i', 'would', 'doubt', 'anyone', 'with', 'a', 'character', 'like', 'melvins', 'would', 'be', 'able', 'to', 'turn', 'back', 'to', 'a', 'nice', ',', 'loving', 'person', '.', 'it', 'would', 'take', 'a', 'helluva', 'long', 'time', ',', 'much', 'longer', 'than', 'this', 'film', 'would', 'like', 'to', 'make', 'out', '.', 'brooks', 'direction', 'is', 'good', ',', 'though', ',', 'if', 'a', 'bit', 'average', ',', 'but', 'he', 'usually', 'manages', 'to', 'get', 'an', 'emotion', 'out', 'of', 'the', 'audience', '.', 'he', 'handles', 'the', 'comedy', 'scenes', 'better', 'than', 'the', 'sentimental', 'ones', '(', 'he', 'tends', 'to', 'pile', 'on', 'to', 'much', 'schmaltz', ')', 'but', 'generally', "he's", 'good', '.', "there's", 'also', 'a', 'nice', 'soundtrack', 'by', 'veteran', 'composer', 'hans', 'zimmer', '.', 'but', ',', 'generally', ',', 'as', 'good', 'as', 'it', 'gets', 'achieves', 'what', 'it', 'sets', 'out', 'to', 'do', ',', 'which', 'is', 'to', 'make', 'the', 'audience', 'feel', 'good', 'by', 'the', 'end', 'of', 'the', 'movie', '.', 'the', 'movie', 'is', 'a', 'bit', 'overlong', ',', 'but', 'nicholson', 'is', 'such', 'good', 'fun', 'that', 'the', 'running', 'time', 'passes', 'by', 'pretty', 'quickly', '.', 'overall', ',', 'as', 'good', 'as', 'it', 'gets', 'is', 'a', 'fun', 'movie', ',', 'even', 'though', 'it', 'may', 'be', 'unbelivable', ',', 'and', 'certainly', 'worth', 'seeing', '(', 'if', 'just', 'for', 'jack', 'nicholsons', 'performance', '.', ')', 'not', 'quite', 'as', 'good', 'as', 'it', 'gets', '(', 'pardon', 'the', 'bad', 'joke', ')', ',', 'but', 'still', 'good', 'fun', '.']))
test(read_document, (datasets[0]['train']['pos'][0], stopwords), set(['james', '.', 'brooks', ',', 'developers', 'simpsons', 'director', 'broadcast', 'news', ',', 'returns', 'big', 'screen', 'entertaining', ',', 'slightly', 'flawed', 'comedy', '.', 'nicholson', 'plays', 'melvin', 'udall', ',', 'horrible', 'person', 'screen', '.', 'racist', ',', 'homophobic', ',', 'good', 'word', '.', ',', 'talks', ',', 'waitress', 'carol', 'conelly', '(', '.', 'sitcom', 'star', 'hunt', ',', 'twister', ',', '1996', ')', '.', 'naturally', ',', 'udall', ',', 'conelly', 'gay', 'neighbor', 'simon', 'bishop', '(', 'kinnear', ')', 'nicholson', 'hates', ',', 'hit', 'end', '.', 'good', 'hunting', '(', '1997', ')', 'titanic', '(', '1997', ')', ',', 'outcome', 'completely', 'obvious', ',', 'good', 'enjoyable', ',', 'funny', 'warm', 'comedy', '.', 'nicholson', 'hilarious', 'melvin', ',', 'churning', 'insults', 'superb', 'relish', '.', 'nicholson', 'lines', 'melvin', 'delivers', '.', 'hunt', 'good', 'waitress', 'carol', ',', 'easily', 'rises', 'challenge', 'nicholson', '.', '(', 'thankfully', ')', 'bit', 'chemistry', '.', 'kinnear', ',', 'gay', 'neighbor', ',', 'slightly', 'underwritten', 'role', ',', 'plot', 'convience', 'character', '.', 'performance', 'good', ',', 'character', 'exist', 'melvin', 'carol', '.', 'fact', ',', 'scene', 'stealer', "simon's", 'dog', ',', 'funnier', 'nicholson', '.', ',', 'pets', 'cute', 'screen', '.', 'providing', 'solid', 'support', 'cuba', 'gooding', ',', 'jnr', '(', 'jerry', 'maguire', ',', '1996', ')', 'yeardly', 'smith', '(', 'voice', 'lisa', 'simpsons', 'simpsons', ')', 'gooding', 'good', 'character', 'maguire', ',', 'fun', '.', 'overacts', ',', 'annoying', '.', 'smith', 'good', ',', 'fairly', 'small', 'role', '.', 'director', 'lawrence', 'kasdan', '(', 'body', 'heat', ',', '1981', ')', 'makes', 'appearance', 'doctor', '.', 'primarily', 'nicholsons', 'film', ',', 'scene', ',', 'steals', '.', 'character', 'hateful', ',', ',', 'amazing', 'talks', ',', 'carol', '.', 'films', 'main', 'problem', '.', 'totally', 'unbelievable', 'carol', 'liking', 'melvin', '.', 'fall', 'love', 'naturally', ',', 'film', 'forces', 'fall', 'love', '.', ',', 'melvins', 'character', 'nice', ',', 'quickly', '.', 'doubt', 'character', 'melvins', 'turn', 'back', 'nice', ',', 'loving', 'person', '.', 'helluva', 'long', 'time', ',', 'longer', 'film', 'make', '.', 'brooks', 'direction', 'good', ',', ',', 'bit', 'average', ',', 'manages', 'emotion', 'audience', '.', 'handles', 'comedy', 'scenes', 'sentimental', '(', 'pile', 'schmaltz', ')', 'generally', 'good', '.', 'nice', 'soundtrack', 'veteran', 'composer', 'hans', 'zimmer', '.', ',', 'generally', ',', 'good', 'achieves', 'sets', ',', 'make', 'audience', 'feel', 'good', 'end', 'movie', '.', 'movie', 'bit', 'overlong', ',', 'nicholson', 'good', 'fun', 'running', 'time', 'passes', 'pretty', 'quickly', '.', ',', 'good', 'fun', 'movie', ',', 'unbelivable', ',', 'worth', '(', 'jack', 'nicholsons', 'performance', '.', ')', 'good', '(', 'pardon', 'bad', 'joke', ')', ',', 'good', 'fun', '.']))

classifier1 = NBClassifier(['pos', 'neg'])
classifier2 = NBClassifier(['pos', 'neg'], stopwords)

testname(NBClassifier.add_train_doc)
testclass(classifier1, classifier1.add_train_doc, ("pos", datasets[0]['train']['pos'][0],), {
    'documents': {'pos': 1, 'neg': 0},
    'likelihood': {'neg': {}, 'pos': {'films': 1, 'consider': 1, 'may': 1, 'bad': 1, 'on': 1, 'fun': 1, 'melvins': 1, 'of': 1, 'ever': 1, 'v': 1, 'jerry': 1, 'seeing': 1, 'for': 1, 'seen': 1, 'it': 1, 'plot': 1, 'thankfully': 1, 'fact': 1, 'audience': 1, 'slightly': 1, 'gets': 1, 'liking': 1, 'all': 1, 'except': 1, 'veteran': 1, 'direction': 1, 'composer': 1, 'lisa': 1, 'her': 1, 'gay': 1, 'jack': 1, 'to': 1, 'twister': 1, 'broadcast': 1, 'schmaltz': 1, 'hateful': 1, 'out': 1, 'running': 1, 'insults': 1, 'still': 1, 'person': 1, '.': 1, '1996': 1, 'easily': 1, 'do': 1, 'off': 1, 'heat': 1, '1981': 1, 'scenes': 1, 'by': 1, 'churning': 1, 'little': 1, 'too': 1, 'movie': 1, 'handles': 1, 'pretty': 1, 'longer': 1, 'loving': 1, 'long': 1, 'totally': 1, 'small': 1, 'ones': 1, 'she': 1, 'who': 1, 'achieves': 1, 'flawed': 1, 'big': 1, 'entertaining': 1, 'stealer': 1, 'able': 1, 'feel': 1, 'but': 1, 'that': 1, 'love': 1, 'relish': 1, 'doctor': 1, 'an': 1, 'smith': 1, 'only': 1, 'screen': 1, 'support': 1, 'generally': 1, 'most': 1, 'outcome': 1, 'overlong': 1, 'would': 1, 'always': 1, 'brooks': 1, 'has': 1, 'back': 1, 'i': 1, 'primarily': 1, 'will': 1, "he's": 1, 'pile': 1, 'nicholsons': 1, 'simpsons': 1, 'completely': 1, 'one': 1, ',': 1, 'unbelievable': 1, 'forces': 1, 'he': 1, 'unbelivable': 1, 'helluva': 1, 'passes': 1, 'director': 1, 'go': 1, 'could': 1, 'better': 1, 'this': 1, 'doubt': 1, 'so': 1, 'last': 1, 'chemistry': 1, 'certainly': 1, 'not': 1, 'conelly': 1, 'funny': 1, 'anyone': 1, 'worth': 1, 'fall': 1, 'joke': 1, 'gooding': 1, 'though': 1, 'come': 1, 'emotion': 1, 'turn': 1, 'are': 1, 'udall': 1, 'hates': 1, 'manages': 1, 'word': 1, 'talks': 1, "simon's": 1, 'him': 1, 'kasdan': 1, 'carol': 1, 'delivers': 1, 'titanic': 1, 'time': 1, "doesn't": 1, 'fairly': 1, 'than': 1, 'steals': 1, 'if': 1, 'take': 1, 'problem': 1, 'homophobic': 1, 'get': 1, 'help': 1, 'even': 1, 'lawrence': 1, 'convience': 1, "there's": 1, 'comedy': 1, 'zimmer': 1, 'star': 1, 'character': 1, 'bit': 1, "it's": 1, 'although': 1, "isn't": 1, 'makes': 1, ')': 1, 'waitress': 1, 'usually': 1, 'together': 1, 'hilarious': 1, 'hit': 1, 'solid': 1, 'more': 1, 'exist': 1, 'enjoyable': 1, 'providing': 1, 'soundtrack': 1, 'hunt': 1, 'especially': 1, 'such': 1, 'average': 1, 'say': 1, 'much': 1, 'is': 1, 'cute': 1, 'good': 1, 'sets': 1, 'the': 1, 'was': 1, 'pardon': 1, 'hunting': 1, 'racist': 1, 'plays': 1, 'between': 1, 'them': 1, 'dog': 1, 'appearance': 1, 'lines': 1, 'end': 1, 'news': 1, 'l': 1, 'at': 1, 'just': 1, 'seems': 1, 'have': 1, 't': 1, 'cuba': 1, 'as': 1, 'returns': 1, 'be': 1, 'in': 1, 'which': 1, 'amazing': 1, 'and': 1, 'sitcom': 1, 'performance': 1, '(': 1, 'like': 1, 'every': 1, 'funnier': 1, 'overacts': 1, 'tends': 1, 'simon': 1, 'maguire': 1, 'pets': 1, 'annoying': 1, '1997': 1, 'melvin': 1, 'developers': 1, 'quickly': 1, 'underwritten': 1, 'yeardly': 1, 'what': 1, 'away': 1, 'with': 1, 'nice': 1, 'naturally': 1, 'never': 1, 'probably': 1, 'obvious': 1, 'body': 1, 'hans': 1, 'rises': 1, 'main': 1, 'jnr': 1, 'make': 1, 'challenge': 1, 'james': 1, 'film': 1, 'superb': 1, 'his': 1, 'neighbor': 1, 'horrible': 1, 'sentimental': 1, 'nobody': 1, 'quite': 1, 'scene': 1, 'kinnear': 1, 'then': 1, 'also': 1, 'role': 1, 'again': 1, 'bishop': 1, 'voice': 1, 'warm': 1, 'nicholson': 1, 'overall': 1, 'a': 1}},
    'vocabulary': {'annoying', 'also', 'of', 'main', 'for', 'seeing', 'such', 'although', 'certainly', 'too', 'liking', 'nicholson', '.', 'titanic', 'lines', 'passes', 'are', 'l', 'seems', 'average', 'turn', 'director', 'better', 'sitcom', 'on', 'overlong', 'dog', 'plays', 'chemistry', 'schmaltz', 'go', 'good', 'by', 'comedy', 'do', 'more', 'hans', 'overacts', 'this', 'as', 'between', 'would', 'horrible', 'jnr', 'v', 'unbelievable', 'relish', 'seen', 'i', 'so', 'may', 'jack', 'pets', 'melvin', 'hunt', 'all', 'homophobic', 'churning', 'delivers', 'little', 'heat', 'a', 'solid', 'which', 'again', 'returns', 'probably', 'rises', 'them', 'most', 'him', 'providing', 'stealer', 'than', 'he', 'one', 'consider', 'doubt', 'tends', 'veteran', 'off', 'feel', 'unbelivable', 'gooding', 'carol', 'hunting', 'though', 'voice', 'is', 'bad', 'always', 'quickly', 'funnier', 'warm', 'thankfully', 'cuba', 'challenge', 'still', 'nobody', 'doctor', 'racist', "there's", 'get', 'anyone', 'appearance', 'news', 'handles', 'generally', 'but', 'love', 'say', 'take', 'come', 'films', 'in', '1981', 'bishop', 'sentimental', 'twister', 'role', 'exist', 'quite', 'character', 'body', 'naturally', 'completely', 'at', 'direction', 'big', 'pardon', 'his', 'waitress', 'then', 'soundtrack', 'convience', 'scene', 'help', 'screen', "he's", 'scenes', 't', 'plot', 'she', 'be', 'maguire', 'make', 'problem', 'insults', 'gay', 'outcome', '1996', 'lawrence', 'totally', "simon's", 'was', ')', 'longer', 'running', 'melvins', 'have', 'pretty', 'cute', 'amazing', 'kasdan', 'long', 'who', ',', 'ever', 'superb', 'simon', 'joke', 'much', 'ones', 'will', 'simpsons', 'audience', 'small', 'underwritten', 'slightly', 'fun', 'movie', 'broadcast', 'emotion', 'hateful', 'only', 'bit', 'kinnear', 'her', 'smith', 'talks', 'conelly', 'with', 'entertaining', "isn't", 'and', 'hilarious', 'fact', 'nicholsons', 'fall', 'pile', 'neighbor', 'never', 'overall', 'hates', 'not', '1997', 'especially', 'forces', 'obvious', 'makes', 'except', 'back', 'to', 'the', 'zimmer', 'steals', 'usually', 'brooks', 'performance', 'james', 'support', 'able', 'out', 'easily', 'flawed', 'jerry', 'achieves', 'if', 'has', 'enjoyable', 'nice', 'primarily', 'loving', 'helluva', 'funny', 'fairly', 'udall', 'person', 'even', 'yeardly', 'hit', "it's", 'developers', 'like', 'sets', 'what', 'just', 'away', 'composer', 'word', 'gets', 'together', 'last', '(', 'end', 'star', 'manages', 'film', 'worth', 'time', 'an', 'that', 'every', 'could', 'it', 'lisa', "doesn't"}
    })
testclass(classifier1, classifier1.add_train_doc, ("neg", datasets[0]['train']['neg'][0],), {
    'documents': {'pos': 1, 'neg': 1},
    'likelihood': {'neg': {"didn't": 1, 'may': 1, 'survival': 1, 'soon': 1, 'poorly': 1, 'jason': 1, 'genre': 1, 'rated': 1, 'loves': 1, 'it': 1, "people's": 1, 'else': 1, 'slightly': 1, 'their': 1, 'doing': 1, 'land': 1, 'all': 1, 'does': 1, "leoni's": 1, 'shown': 1, 'my': 1, 'her': 1, 'stupid': 1, 'chock': 1, 'faces': 1, 'later': 1, 'to': 1, 'ridiculous': 1, 'upcoming': 1, 'general': 1, 'dark': 1, 'suffered': 1, 'creating': 1, 'while': 1, 'want': 1, 'please': 1, 'computer': 1, 'talented': 1, 'scenes': 1, 'sympathetic': 1, 'little': 1, 'too': 1, 'debut': 1, 'score': 1, 'cheap': 1, 'ele': 1, 'she': 1, 'who': 1, 'rittenhouse': 1, 'infinitely': 1, 'remarkable': 1, 'flick': 1, 'involving': 1, 'influences': 1, 'offer': 1, 'tolkin': 1, 'yar': 1, 'object': 1, 'denise': 1, 'use': 1, 'they': 1, 'film': 1, 'anyway': 1, 'drifting': 1, 'one': 1, 'surface': 1, 'has': 1, 'official': 1, 'back': 1, 'bruce': 1, 'car': 1, 'showing': 1, 'cgi': 1, 'he': 1, 'impacts': 1, 'shocker': 1, 'go': 1, 'generation': 1, 'this': 1, 'sky': 1, 'internet': 1, 'anyone': 1, 'meet': 1, 'laughable': 1, 'worse': 1, 'morgan': 1, 'horner': 1, 'stop': 1, 'title': 1, 'called': 1, 'subplot': 1, 'ninety': 1, 'highlights': 1, 'presence': 1, "doesn't": 1, 'fears': 1, 'duvall': 1, 'miss': 1, 'if': 1, 'me': 1, 'costing': 1, 'leo': 1, '!': 1, 'oppposed': 1, 'were': 1, 'would': 1, 'disastrously': 1, 'remember': 1, 'humans': 1, 'character': 1, 'woman': 1, 'leelee': 1, 'reckless': 1, 'determine': 1, 'ellicit': 1, 'goes': 1, 'tell': 1, 'joel': 1, 'is': 1, 'up': 1, 'grow': 1, 'off': 1, 'tasha': 1, 'shy': 1, 'mimi': 1, 'give': 1, 'included': 1, 'almost': 1, 'done': 1, 'came': 1, 'before': 1, 'as': 1, 'shallow': 1, 'cheapest': 1, 'unnamed': 1, 'x-files': 1, 'see': 1, 'do': 1, 'performance': 1, 'like': 1, 'performances': 1, 'water': 1, 'or': 1, 'deja': 1, 'destroy': 1, 'rubin': 1, 'final': 1, 'implausibilities': 1, 'with': 1, 'naturally': 1, 'pushing': 1, 'successful': 1, 'able': 1, 'directly': 1, 'rest': 1, 'push': 1, 'touching': 1, 'accident': 1, 'cover-up': 1, 'towards': 1, 'schell': 1, 'half': 1, 'his': 1, "actors'": 1, 'cave': 1, 'once': 1, 'unfortunately': 1, 'moment': 1, 'turns': 1, 'well': 1, 'again': 1, 'terror': 1, 'films': 1, 'apparently': 1, 'sci-fi': 1, 'nearly': 1, 'talking': 1, 'of': 1, 'virtually': 1, 'independence': 1, 'guessing': 1, 'press': 1, 'been': 1, 'fact': 1, 'viewers': 1, 'talks': 1, 'loved': 1, 'reporter': 1, 'months': 1, 'from': 1, 'spoilers': 1, 'us': 1, 'far': 1, '$75': 1, 'obvious': 1, 'knows': 1, 'roles': 1, 'out': 1, 'making': 1, 'mess': 1, 'contains': 1, 'biederman': 1, 'heartfelt': 1, 'blame': 1, 'discovers': 1, 'spelled': 1, 'announce': 1, 'ark': 1, 'watch': 1, 'major': 1, 'theater': 1, 'outside': 1, 'relationship': 1, 'above': 1, '1993': 1, 'pace': 1, 'personally': 1, 'ellie': 1, 'taking': 1, '"': 1, 'screen': 1, 'wants': 1, 'acknowledgeable': 1, 'most': 1, 'conference': 1, 'year': 1, 'vu': 1, 'standard': 1, 'continent': 1, 'right': 1, 'alan': 1, 'special': 1, 'starts': 1, 'the': 1, 'limited': 1, 'alone': 1, 'director': 1, 'peacemaker': 1, 'keep': 1, 'there': 1, 'introduced': 1, 'laughs': 1, 'human': 1, 'which': 1, 'trying': 1, 'characters': 1, 'stronger': 1, 'disaster': 1, 'him': 1, 'memories': 1, 'telescopes': 1, 'worst': 1, 'stuff': 1, 'titanic': 1, 'used': 1, 'its': 1, 'named': 1, 'front': 1, 'humor': 1, 'possible': 1, 'best': 1, 'another': 1, 'help': 1, '20%': 1, 'even': 1, 'work': 1, '2': 1, 'pathetic': 1, 'volcano': 1, 'doom': 1, 'entertaining': 1, 'effects': 1, 'improved': 1, 'tension': 1, 'situation': 1, 'am': 1, 'things': 1, 'days': 1, 'hits': 1, 'much': 1, 'boring': 1, 'good': 1, 'sets': 1, 'stood': 1, 'job': 1, 'think': 1, 'review': 1, 'heartless': 1, 'public': 1, 'better': 1, 'passes': 1, 'difference': 1, 'note': 1, 'feeling': 1, 'hours': 1, 'throughout': 1, 'at': 1, 'have': 1, 't': 1, 'full': 1, 'minutes': 1, 'leder': 1, 'put': 1, 'nice': 1, 'distant': 1, 'fire': 1, 'certain': 1, 'die': 1, 'vanessa': 1, 'only': 1, 'audience': 1, 'moments': 1, 'brings': 1, 'sobieski': 1, 'head': 1, 'horrible': 1, 'meatiest': 1, '48': 1, 'comes': 1, 'passed': 1, 'massive': 1, '?': 1, 'cast': 1, 'made': 1, 'hit': 1, 'succeeds': 1, 'concerning': 1, 'make': 1, 'walk': 1, 'competition': 1, 'bottom': 1, 'large': 1, 'trick': 1, 'teacher': 1, 'comet': 1, 'overall': 1, 'life': 1, 'these': 1, 'settle': 1, 'a': 1, 'nothing': 1, 'rushing': 1, 'path': 1, 'freeman': 1, 'baffles': 1, 'might': 1, 'fun': 1, 'wonder': 1, 'seeing': 1, 'recommend': 1, 'seen': 1, 'plot': 1, 'night': 1, 'turned': 1, 'when': 1, 'previews': 1, 'date': 1, 'visual': 1, "can't": 1, 'face': 1, "haven't": 1, 'hopefully': 1, 'given': 1, 'subtitles': 1, 'latter': 1, 'composed': 1, 'did': 1, 'drawn': 1, 'michael': 1, 'states': 1, 'frightening': 1, 'mine': 1, 'day': 1, 'truth': 1, 'races': 1, 'attempt': 1, 'luckily': 1, 'picks': 1, 'july': 1, 'pretty': 1, "tv's": 1, 'subplots': 1, 'situations': 1, 'rather': 1, 'ones': 1, 'because': 1, 'seconds': 1, 'plans': 1, 'supposed': 1, 'plan': 1, 'some': 1, 'armageddon': 1, 'lapsed': 1, 'ilm': 1, 'going': 1, 'literally': 1, 'photo': 1, 'flying': 1, 'affair': 1, 'distracting': 1, "hasn't": 1, 'elements': 1, 'know': 1, 'cheesy': 1, 'drama': 1, 'should': 1, 'i': 1, 'deadly': 1, 'will': 1, 'concept': 1, 'illustrious': 1, 'shrieks': 1, 'watching': 1, 'hope': 1, 'completely': 1, 'barely': 1, 'sarah': 1, 'instead': 1, 'sends': 1, 'promising': 1, 'story': 1, 'then': 1, 'not': 1, 'msnbc': 1, 'outdid': 1, 'interesting': 1, 'mostly': 1, 'boys': 1, 'via': 1, 'break': 1, 'ranking': 1, 'television': 1, 'worth': 1, 'unknown': 1, 'seat': 1, 'after': 1, 'million': 1, 'herself': 1, 'understand': 1, 'forgiveable': 1, 'majestic': 1, 'makes': 1, 'start': 1, 'weeks': 1, 'years': 1, 'longer--approximately': 1, 'related': 1, 'people': 1, 'liners': 1, 'very': 1, 'ms': 1, 'than': 1, 'entire': 1, 'hard': 1, 'omen': 1, 'take': 1, 'secret': 1, 'row': 1, 'language': 1, 'local': 1, 'reaction': 1, 'into': 1, 'realistic': 1, 'emotional': 1, 'compensated': 1, "isn't": 1, ';': 1, 'thing': 1, 'oscar-winner': 1, 'wish': 1, 'written': 1, 'stay': 1, 'be': 1, 'can': 1, 'robert': 1, 'show': 1, 'cliffhanger': 1, 'senator': 1, 'unknowingly': 1, 'was': 1, 'investigate': 1, 'handed': 1, 'mistake': 1, 'simply': 1, 'experience': 1, 'logic': 1, 'still': 1, 'successfully': 1, 'united': 1, 'just': 1, "leder's": 1, "it's": 1, 'jenny': 1, 'during': 1, 'february': 1, 'and': 1, 'chance': 1, '(': 1, 'strong': 1, 'forgettable': 1, 'brief': 1, 'released': 1, ':': 1, 'pick': 1, 'defied': 1, 'race': 1, 'leoni': 1, 'line': 1, 'suggestion': 1, '.': 1, 'how': 1, 'underground': 1, 'reminded': 1, ',': 1, 'earth': 1, 'course': 1, 'mail': 1, 'james': 1, 'sadist': 1, 'quite': 1, 'smart': 1, 'peak': 1, 'fooled': 1, 'enough': 1, 'collision': 1, 'exactly': 1, 'next': 1, "won't": 1, 'suggests': 1, 'remotely': 1, 'spacecraft': 1, 'renny': 1, 'wasted': 1, 'bad': 1, 'on': 1, '000': 1, 'hold': 1, 'naked': 1, 'send': 1, 'figure': 1, 'for': 1, 'exhilirating': 1, 'really': 1, 'tries': 1, 'hyped': 1, 'now': 1, 'away': 1, 'gets': 1, "that's": 1, 'deep': 1, 'spell': 1, 'among': 1, '1997': 1, 'direction': 1, 'no': 1, 'constructed': 1, 'killed': 1, 'feels': 1, 'redgrave': 1, 'likes': 1, 'witness': 1, 'summer': 1, 'stick': 1, 'minority': 1, 'wrong': 1, 'space': 1, 'select': 1, 'varies': 1, 'by': 1, 'few': 1, 'first': 1, 'any': 1, 'forms': 1, 'big': 1, 'movie': 1, 'ron': 1, 'girl': 1, 'students': 1, 'episodes': 1, 'absoltuely': 1, 'ya': 1, 'recommends': 1, 'decides': 1, 'utterly': 1, 'government': 1, 'but': 1, 'action': 1, 'fifteen': 1, 'warrant': 1, 'an': 1, 'honest': 1, 'incredibly': 1, 'wazoo': 1, 'wood': 1, "person's": 1, 'harlin': 1, 'random': 1, 'huge': 1, 'gives': 1, 'actually': 1, 'sex': 1, 'eldard': 1, "real-time--it's": 1, 'two': 1, 'trek': 1, 'are': 1, 'hotchner': 1, 'victims': 1, 'look': 1, 'could': 1, 'so': 1, 'last': 1, 'confirm': 1, 'beck': 1, 'placed': 1, 'cromwell': 1, 'in': 1, 'mentioning': 1, 'enhanced': 1, 'orbiting': 1, 'through': 1, 'come': 1, 'turn': 1, 'brilliant': 1, '70s': 1, 'impending': 1, 'shreds': 1, 'provide': 1, 'heard': 1, 'many': 1, 'time': 1, "dante's": 1, 'peering': 1, 'road': 1, 'you': 1, 'along': 1, 'get': 1, 'farther': 1, 'began': 1, 'your': 1, 'elijah': 1, 'shows': 1, 'star': 1, 'incohesive': 1, 'astronomer': 1, 'response': 1, 'dust': 1, 'place': 1, 'shame': 1, ')': 1, 'information': 1, 'least': 1, 'cry': 1, 'outrageous': 1, 'role': 1, 'astronaut': 1, 'beginning': 1, '800': 1, 'effective': 1, 'side': 1, 'flaunt': 1, 'energetic': 1, 'screenwriters': 1, 'mentions': 1, 'mind': 1, 'warning': 1, 'ways': 1, 'coming': 1, 'question': 1, 'lerner': 1, 'looking': 1, '80%': 1, 'begins': 1, 'school': 1, 'spectacular': 1, 'rope': 1, 'having': 1, 'seems': 1, 'expected': 1, 'more': 1, 'care': 1, 'darn': 1, 'crosby': 1, 'ship': 1, 'president': 1, 'future': 1, 'struck': 1, 'over': 1, 'reveal': 1, 'looks': 1, 'about': 1, 'arrive': 1, 'simplistic': 1, 'comet-disaster': 1, 'that': 1, 'procedures': 1, 'kill': 1, 'talent': 1, 'had': 1, 'what': 1, 'preposterous': 1, 'maximilian': 1, 'correct': 1, 'season': 1, 'unsatisfied': 1, 'those': 1, 'father': 1, 'crafted': 1, 'we': 1, 'yada': 1, 'ever': 1, 'technology': 1, 'pg-13': 1, 'also': 1, 'main': 1, 'actors': 1, 'er': 1, 'advanced': 1, 'impact': 1}, 'pos': {'films': 1, 'consider': 1, 'may': 1, 'bad': 1, 'on': 1, 'fun': 1, 'melvins': 1, 'of': 1, 'ever': 1, 'v': 1, 'jerry': 1, 'seeing': 1, 'for': 1, 'seen': 1, 'it': 1, 'plot': 1, 'thankfully': 1, 'fact': 1, 'audience': 1, 'slightly': 1, 'gets': 1, 'liking': 1, 'all': 1, 'except': 1, 'veteran': 1, 'direction': 1, 'composer': 1, 'lisa': 1, 'her': 1, 'gay': 1, 'jack': 1, 'to': 1, 'twister': 1, 'broadcast': 1, 'schmaltz': 1, 'hateful': 1, 'out': 1, 'running': 1, 'insults': 1, 'still': 1, 'person': 1, '.': 1, '1996': 1, 'easily': 1, 'do': 1, 'off': 1, 'heat': 1, '1981': 1, 'scenes': 1, 'by': 1, 'churning': 1, 'little': 1, 'too': 1, 'movie': 1, 'handles': 1, 'pretty': 1, 'longer': 1, 'loving': 1, 'long': 1, 'totally': 1, 'small': 1, 'ones': 1, 'she': 1, 'who': 1, 'achieves': 1, 'flawed': 1, 'big': 1, 'entertaining': 1, 'stealer': 1, 'able': 1, 'feel': 1, 'but': 1, 'that': 1, 'love': 1, 'relish': 1, 'doctor': 1, 'an': 1, 'smith': 1, 'only': 1, 'screen': 1, 'support': 1, 'generally': 1, 'most': 1, 'outcome': 1, 'overlong': 1, 'would': 1, 'always': 1, 'brooks': 1, 'has': 1, 'back': 1, 'i': 1, 'primarily': 1, 'will': 1, "he's": 1, 'pile': 1, 'nicholsons': 1, 'simpsons': 1, 'completely': 1, 'one': 1, ',': 1, 'unbelievable': 1, 'forces': 1, 'he': 1, 'unbelivable': 1, 'helluva': 1, 'passes': 1, 'director': 1, 'go': 1, 'could': 1, 'better': 1, 'this': 1, 'doubt': 1, 'so': 1, 'last': 1, 'chemistry': 1, 'certainly': 1, 'not': 1, 'conelly': 1, 'funny': 1, 'anyone': 1, 'worth': 1, 'fall': 1, 'joke': 1, 'gooding': 1, 'though': 1, 'come': 1, 'emotion': 1, 'turn': 1, 'are': 1, 'udall': 1, 'hates': 1, 'manages': 1, 'word': 1, 'talks': 1, "simon's": 1, 'him': 1, 'kasdan': 1, 'carol': 1, 'delivers': 1, 'titanic': 1, 'time': 1, "doesn't": 1, 'fairly': 1, 'than': 1, 'steals': 1, 'if': 1, 'take': 1, 'problem': 1, 'homophobic': 1, 'get': 1, 'help': 1, 'even': 1, 'lawrence': 1, 'convience': 1, "there's": 1, 'comedy': 1, 'zimmer': 1, 'star': 1, 'character': 1, 'bit': 1, "it's": 1, 'although': 1, "isn't": 1, 'makes': 1, ')': 1, 'waitress': 1, 'usually': 1, 'together': 1, 'hilarious': 1, 'hit': 1, 'solid': 1, 'more': 1, 'exist': 1, 'enjoyable': 1, 'providing': 1, 'soundtrack': 1, 'hunt': 1, 'especially': 1, 'such': 1, 'average': 1, 'say': 1, 'much': 1, 'is': 1, 'cute': 1, 'good': 1, 'sets': 1, 'the': 1, 'was': 1, 'pardon': 1, 'hunting': 1, 'racist': 1, 'plays': 1, 'between': 1, 'them': 1, 'dog': 1, 'appearance': 1, 'lines': 1, 'end': 1, 'news': 1, 'l': 1, 'at': 1, 'just': 1, 'seems': 1, 'have': 1, 't': 1, 'cuba': 1, 'as': 1, 'returns': 1, 'be': 1, 'in': 1, 'which': 1, 'amazing': 1, 'and': 1, 'sitcom': 1, 'performance': 1, '(': 1, 'like': 1, 'every': 1, 'funnier': 1, 'overacts': 1, 'tends': 1, 'simon': 1, 'maguire': 1, 'pets': 1, 'annoying': 1, '1997': 1, 'melvin': 1, 'developers': 1, 'quickly': 1, 'underwritten': 1, 'yeardly': 1, 'what': 1, 'away': 1, 'with': 1, 'nice': 1, 'naturally': 1, 'never': 1, 'probably': 1, 'obvious': 1, 'body': 1, 'hans': 1, 'rises': 1, 'main': 1, 'jnr': 1, 'make': 1, 'challenge': 1, 'james': 1, 'film': 1, 'superb': 1, 'his': 1, 'neighbor': 1, 'horrible': 1, 'sentimental': 1, 'nobody': 1, 'quite': 1, 'scene': 1, 'kinnear': 1, 'then': 1, 'also': 1, 'role': 1, 'again': 1, 'bishop': 1, 'voice': 1, 'warm': 1, 'nicholson': 1, 'overall': 1, 'a': 1}},
    'vocabulary': {'boys', 'start', 'of', 'months', 'although', 'certainly', 'meet', 'visual', "didn't", 'note', 'implausibilities', 'press', 'interesting', 'turn', 'confirm', 'look', 'naked', 'ship', 'score', 'crosby', 'on', 'acknowledgeable', 'comet', 'continent', 'schmaltz', 'information', 'mostly', 'comedy', 'successfully', 'hans', 'certain', 'loves', 'unnamed', 'horrible', 'jnr', 'v', 'can', 'grow', 'relish', 'used', 'may', 'people', 'stick', 'suffered', 'humans', 'delivers', 'churning', 'comes', 'struck', 'ways', 'roles', 'hours', 'remarkable', 'solid', 'feels', 'most', 'providing', 'stealer', 'running', 'year', 'one', 'might', 'veteran', 'flying', 'energetic', 'sympathetic', 'cheap', 'gooding', 'always', 'involving', 'majestic', 'nobody', 'watching', 'racist', 'included', 'leo', 'appearance', 'now', 'season', 'competition', 'passed', 'minority', 'experience', 'strong', 'see', 'soon', 'pick', 'shallow', 'loved', 'doom', 'orbiting', 'incredibly', 'deja', 'character', 'body', 'sky', 'naturally', 'direction', 'emotional', 'suggests', 'rated', 'compensated', 'shame', 'turned', 'influences', 'been', 'brief', 'mine', 'begins', 'virtually', 'screen', "he's", 'deadly', 'ranking', 'were', 'over', 'leder', 'crafted', 'woman', "simon's", 'father', 'blame', 'you', 'have', 'course', 'trick', '2', 'nothing', 'computer', 'wood', 'united', 'long', 'once', 'earth', 'came', 'hits', 'much', 'instead', 'ones', 'will', 'wasted', 'advanced', '20%', 'vu', 'eldard', 'underwritten', 'anyway', 'simply', 'baffles', 'fire', 'your', 'reporter', 'kinnear', '?', 'exhilirating', 'knows', 'talks', 'entertaining', 'shy', 'cromwell', 'relationship', 'title', 'heartfelt', 'upcoming', 'preposterous', 'pile', 'difference', 'armageddon', "won't", 'rushing', 'given', 'especially', '1993', 'because', 'oppposed', 'effects', 'affair', 'zimmer', 'human', 'place', 'concept', 'sadist', 'spelled', 'recommend', 'leelee', 'determine', 'successful', 'disastrously', 'heartless', 'astronomer', 'talking', 'figure', 'did', 'related', 'funny', 'sets', 'brings', 'terror', 'away', 'else', 'head', 'last', 'my', 'having', 'end', 'constructed', 'government', 'am', 'their', 'chock', 'worst', 'an', 'wazoo', 'space', 'almost', 'elijah', 'it', 'care', "doesn't", 'taking', 'annoying', 'main', 'for', 'such', 'cheesy', 'liking', 'killed', 'nicholson', 'titanic', 'sobieski', 'vanessa', 'lines', 'subtitles', 'are', 'literally', 'kill', 'wants', 'when', 'seems', 'average', 'chance', 'moment', 'or', "leder's", 'ridiculous', "can't", 'want', 'students', 'overlong', 'possible', 'reminded', 'chemistry', 'years', 'go', 'walk', 'thing', 'unfortunately', 'public', 'miss', 'unbelievable', 'seen', 'object', 'effective', 'debut', 'handed', 'weeks', 'ark', "person's", 'million', 'side', 'again', 'named', 'probably', 'tries', 'tends', 'he', 'quite', 'consider', 'feel', 'dark', 'doubt', '000', 'night', 'hopefully', 'flick', 'though', 'hunting', 'best', "dante's", 'bad', 'car', 'hold', 'fooled', 'among', 'rather', "there's", 'keep', 'news', 'sex', 'love', 'say', 'take', 'come', 'films', 'moments', 'sentimental', 'shown', 'ellie', 'mistake', 'duvall', 'pardon', 'water', 'leoni', 'forgiveable', 'after', 'alan', 'starts', 'reckless', 'large', 'remotely', 't', 'investigate', 'stuff', 'be', 'make', 'me', "leoni's", 'outcome', 'lawrence', 'was', ')', 'longer', 'previews', 'before', 'lapsed', 'distracting', 'pretty', 'major', 'ellicit', 'warning', 'composed', 'races', 'offer', 'procedures', ',', 'drawn', 'ever', 'superb', 'through', 'mind', 'tension', 'destroy', 'touching', 'plans', 'shocker', 'some', 'succeeds', 'into', ';', 'redgrave', 'internet', 'stood', 'luckily', 'surface', 'only', 'jenny', 'rittenhouse', 'smith', 'er', 'promising', 'nicholsons', 'personally', 'incohesive', 'minutes', 'showing', 'discovers', 'secret', 'neighbor', 'along', 'never', 'characters', "tv's", 'actually', 'unknown', 'the', 'steals', 'performance', 'days', 'support', 'mess', 'jerry', 'achieves', 'does', 'has', 'nice', 'shrieks', 'teacher', "that's", 'president', 'improved', 'hit', 'presence', 'correct', 'review', 'poorly', 'suggestion', 'push', 'ilm', 'cheapest', 'guessing', 'another', 'actors', 'film', 'highlights', 'time', 'exactly', 'that', 'could', 'looking', '80%', 'tell', 'meatiest', 'seeing', 'attempt', 'reaction', 'july', 'turns', 'too', 'first', 'really', '.', 'morgan', 'screenwriters', 'land', 'l', 'show', '$75', 'know', 'rest', 'truth', 'director', 'give', 'episodes', 'subplot', 'dog', 'how', 'plays', 'standard', 'wonder', 'by', 'we', 'life', 'about', 'overacts', 'as', 'between', 'disaster', 'barely', 'nearly', 'smart', 'lerner', 'coming', 'face', 'towards', 'stronger', 'i', 'question', 'going', 'laughs', 'pets', 'hunt', 'joel', 'homophobic', 'subplots', 'which', 'returns', 'rises', 'watch', 'them', 'latter', 'him', 'these', 'far', 'supposed', 'front', 'should', 'put', 'off', 'shreds', 'frightening', 'carol', 'peering', 'cliffhanger', 'thankfully', 'cuba', 'challenge', 'still', 'doctor', 'schell', 'harlin', 'expected', 'hyped', 'anyone', 'outdid', 'generally', 'witness', '70s', 'msnbc', 'drifting', '1981', 'bishop', 'had', 'job', 'twister', 'role', 'remember', 'unsatisfied', 'honest', 'at', 'throughout', 'big', 'date', 'his', 'waitress', 'ron', 'spectacular', 'two', 'impact', 'soundtrack', 'outrageous', 'wish', 'convience', 'scene', 'help', 'use', 'she', 'please', 'contains', '1996', 'illustrious', 'realistic', 'liners', 'sends', 'announce', 'performances', 'amazing', 'tolkin', 'summer', 'understand', 'pg-13', 'seat', 'simon', 'senator', 'wrong', 'oscar-winner', 'cave', 'joke', 'television', 'simplistic', "real-time--it's", 'talent', 'making', 'simpsons', 'general', 'ya', 'spacecraft', 'broadcast', 'began', 'farther', 'emotion', 'break', 'above', 'provide', 'bit', 'die', 'things', 'arrive', 'her', 'conelly', 'hilarious', 'forms', 'longer--approximately', 'trek', 'humor', 'not', 'settle', 'distant', 'genre', '1997', 'pushing', 'its', 'forces', 'action', 'except', 'huge', 'deep', 'utterly', '"', 'brooks', 'james', "haven't", 'out', 'flawed', 'if', 'rope', 'massive', 'placed', 'limited', 'later', 'denise', 'helluva', 'biederman', 'even', 'yeardly', "it's", 'written', 'developers', 'what', 'bottom', 'least', 'composer', 'word', 'no', 'think', 'together', 'astronaut', 'school', 'varies', 'bruce', 'likes', 'picks', 'defied', 'maximilian', 'every', 'lisa', 'enhanced', 'stay', 'also', 'brilliant', 'yada', 'renny', ':', 'elements', 'volcano', 'peacemaker', 'few', 'cgi', 'herself', 'hotchner', 'rubin', 'faces', 'passes', 'goes', 'official', 'robert', 'darn', 'situation', 'yar', 'theater', 'half', 'impacts', 'stop', 'sitcom', 'up', 'outside', 'generation', 'do', 'good', 'infinitely', 'cry', 'unknowingly', 'more', 'this', 'stupid', 'would', 'feeling', 'line', 'select', 'comet-disaster', 'freeman', 'many', 'sci-fi', 'trying', 'viewers', 'so', 'decides', 'jack', 'local', 'melvin', 'little', 'all', 'heat', 'sarah', 'a', 'better', 'forgettable', 'than', 'unbelivable', 'story', 'from', 'collision', 'concerning', 'well', 'road', 'voice', 'survival', 'is', 'heard', 'talented', 'quickly', 'funnier', 'warm', 'via', 'future', 'seconds', 'dust', 'made', 'released', "actors'", 'get', 'apparently', 'handles', 'language', 'drama', 'cover-up', 'but', 'directly', 'in', 'mentions', 'spell', 'underground', 'conference', 'exist', 'peak', 'impending', 'flaunt', 'completely', 'warrant', 'photo', 'hope', 'ms', 'next', 'then', 'ninety', 'response', 'jason', 'scenes', 'row', 'pathetic', 'cast', 'plot', 'worse', 'horner', 'maguire', 'looks', 'problem', 'insults', 'gay', 'any', 'enough', 'right', 'totally', 'doing', 'final', 'entire', 'creating', 'victims', 'melvins', 'there', 'recommends', "hasn't", 'cute', 'kasdan', '800', 'very', 'who', 'beginning', 'independence', 'boring', 'ele', 'fifteen', 'absoltuely', 'audience', 'mail', 'small', 'fun', 'slightly', 'movie', 'called', 'laughable', 'mentioning', 'shows', 'hateful', '!', 'technology', 'omen', 'they', 'accident', 'with', "isn't", 'fall', 'day', 'and', 'fact', 'work', 'situations', 'special', 'spoilers', 'logic', 'overall', 'hates', 'michael', 'path', 'back', 'obvious', 'makes', 'race', 'to', 'us', 'usually', '48', 'alone', 'while', 'able', 'tasha', 'easily', 'those', 'states', 'memories', 'done', 'enjoyable', 'introduced', 'beck', 'mimi', 'pace', 'primarily', 'loving', 'telescopes', 'send', 'random', 'fairly', 'udall', 'person', 'x-files', 'like', 'costing', 'just', "people's", 'gives', 'plan', 'gets', 'hard', 'february', '(', 'full', 'girl', 'star', 'manages', 'worth', 'fears', 'reveal', 'during'}
    })


testname(NBClassifier.train)
testclass(classifier1, classifier1.train, (), {
    'prior': {'pos': 0.5, 'neg': 0.5},
    'denominator': {'pos': 1129, 'neg': 1581}
    })

testname(NBClassifier.classify)
test(classifier1.classify, (datasets[0]['test']['pos'][0], ), 'pos')
test(classifier1.classify, (datasets[0]['test']['neg'][0], ), 'pos')

# Unakrsna validacija
testname(cross_validate)
cross_validate(False, [161,168,167,165,167,165,169,167,158,171])

testname(cross_validate)
cross_validate(True, [162,168,168,164,167,166,168,168,153,170])

