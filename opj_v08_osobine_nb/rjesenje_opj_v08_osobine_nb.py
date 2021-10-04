# coding=utf-8

import random
import math
import os


###########################################################################################
### PREPROCESING ###
###########################################################################################

def read_file(filename):
    """
    ulaz:
     filename: datoteka
    izlaz:
     lista riječi u datoteci (data)
    """
    return [line.strip() for line in open(filename, 'r').read().strip().split()]

def get_labeled_data(data_path):
    """
    ulaz:
     data_path: putanja do datoteka s podacima
    izlaz:
     lista označenih podataka (labeled_data) gdje je označeni podatak oblika (word, label)

    data_path je direktorij koji sadrži dvije datoteke
    ./names/
      female.txt # datoteka s ženskim imenima
      male.txt   # datoteka s muškim imenima

    1. oznake će biti female i male
    2. svakoj riječi iz datoteke female.txt će se pridružiti oznaka female
       svakoj riječi iz datoteke male.txt će se pridružiti oznaka male
    3. sve označene riječi iz female.txt i male.txt će se spojiti u jedinstvenu listu
    """
    labels = [filename.rstrip('.txt') for filename in os.listdir(data_path) if filename.endswith('.txt')]
    return [(word, label) for label in labels for word in read_file(data_path + label + '.txt')]

def split_train_test_data(labeled_data):
    """
    ulaz:
     labeled_data: lista označenih podataka
    izlaz:
     lista označenih podataka za treniranje
     lista označenih podataka za testiranje

    1. lista sa označenim ženskim i muškim imenima se prvo promiješa
    2. prvih 3/4 pomiješane označene liste su podaci za treniranje
       ostalih 1/4 pomiješane označene liste su podaci za testiranje
    """
    random.seed(0)
    random.shuffle(labeled_data)
    n = 3 * len(labeled_data) // 4
    return labeled_data[:n], labeled_data[n:]


def make_rich_features(word):
    features = {}
    features["first_letter"] = word[0].lower()
    features["last_letter"] = word[-1].lower()
    for letter in 'ale':
        #features["count({})".format(letter)] = word.lower().count(letter)
        features["has({})".format(letter)] = (letter in word.lower())
    return features

###########################################################################################
### CLASSIFIER ###
###########################################################################################

class NBClassifier(object):

    def __init__(self, features_factory):
        """
        ulaz:
         features_factory - funkcija koja gradi osobine od zadane riječi
                            U ovom zadatku su definirane dvije funkcije
                            make_letter_features, make_suffix_features

        funkcija za gradnju osobina će se pamtiti u self.features_factory atributu
        """
        self.features_factory = features_factory

    def train(self, labeled_data):
        """
        ulaz:
         labeled_data - lista označenih podataka
         oblika [('Jonn', 'male'), ('Jane', 'female'), ...]
         gdje je svaki par oblika (word, label)

        FEATURES_DATA
        ************************************************************
        iz labeled_data stvoriti features_data
        oblika [({'last_letter': 'n'}, 'male'), ({'last_letter': 'e'}, 'female'), ...]
        gdje je svaki par oblika (features(word), label)

        Potrebno je za svaku riječ word pozvati funkciju postavljenu u self.features_factory
        koja će stvoriti features(word)

        features(word) je rječnik čiji su ključevi nazivi osobina fname,
        a vrijednosti su vrijednosti osobina fval.

        PRIOR
        ************************************************************

                        N(label)
        prior(label) = ----------
                           N

        gdje je
         N(label) broj svih riječi iz labeled_data označenih s label
         N ukupan broj svih riječi iz labeled_data

        Primjer:
        Za labeled_data = [('Jonn', 'male'), ('Jane', 'female'), ('Allison', 'female')]
        dobiva se:
         prior('male') = 1/3
         prior('female') = 2/3

        LIKELIHOOD
        ************************************************************

        likelihood(label, fname, fval) = N(label, fname, fval)

        gdje je N(label, fname, fval) broj pojavljivanja osobine
        s nazivom fname i vrijednošću fval za oznaku label

        Primjer:
        Za labeled_data =
        [('Jonn', 'male'), ('Jane', 'female'), ('Allison', 'female')]
        prvo se pretvori u featured_data =
        [({'last_letter': 'n'}, 'male'), ({'last_letter': 'e'}, 'female'), ({'last_letter': 'n'}, 'female')]
        i dobiva se:
         likelihood('male', 'last_letter', 'n') = 1
         likelihood('female', 'last_letter', 'e') = 1
         likelihood('female', 'last_letter', 'n') = 1


        FEATURES VOCABULARY
        ************************************************************

        vocabulary(fname) = {fval1, fval2, fval3, ...}

        vocavulary je rječnik s ključevima fname a vrijednosti su sve moguće fval

        Primjer:
        Za featured_data = [({'last_letter': 'n'}, 'male'), ({'last_letter': 'e'}, 'female'), ({'last_letter': 'n'}, 'female')]
        dobiva se:
         vocabulary('last_letter') = {'n', 'e'}
        """

        self.labels = set()
        self.prior = {}
        self.likelihood = {}
        self.featurevalues = {}

        for word, label in labeled_data:
            self.prior[label] = self.prior.get(label, 0) + 1
            self.labels.add(label)
            featureset = self.features_factory(word)
            for fname, fval in featureset.items():
                self.likelihood.setdefault((label, fname), {})
                self.likelihood[label, fname][fval] = self.likelihood[label, fname].get(fval, 0) + 1
                self.featurevalues.setdefault(fname, set()).add(fval)

        self.prior = {label: count / len(labeled_data) for label, count in self.prior.items()}


    def classify(self, word):
        """
        ulaz:
         word: riječ koja će se označiti
        izlaz:
         label: predviđena oznaka ulazne riječi

        neka je features(word) rječnik osobina i vrijednosti za word

        Na primjer:
        ako je word = "John"
        onda je features(word) = {'last_letter': 'n'}

        POSTERIOR
        ************************************************************

        posterior(label|word) = log(prior(label))
                              + [ suma(log(likelihood(label, fname, fval) + 1) - log(|vocabulary(fname)| + |vocabulary|) ]
                                [ za sve fname, fval iz features(word)                                                   ]

        gdje je |vocabulary| = suma svih |vocabulary(fname)| za sve nazive osobina fname

        MAX POSTERIOR
        *************************************************************

        label* = argmax( posterior(label|word) )

        vratiti onu oznaku label* koja maksimizira posterior
        """
        featureset = self.features_factory(word)
        posterior = {}
        vocabulary_size = sum(len(values) for values in self.featurevalues.values())
        for label in self.labels:
            posterior[label] = math.log(self.prior[label])
            for fname, fval in featureset.items():
                posterior[label] += math.log(self.likelihood[label, fname].get(fval, 0) + 1)
                posterior[label] -= math.log(len(self.featurevalues[fname]) + vocabulary_size)
        return max(posterior, key=posterior.get)

    def accuracy(self, labeled_data):
        """
        Za označene podatke labeled_data prebrojava koliko ih je točno klasificirao
        """
        count_good, count_all = 0, 0
        for word, label in labeled_data:
            predict_label = self.classify(word)
            if predict_label == label:
                count_good += 1
            count_all += 1

        #print(count_good, count_all, count_good / count_all)
        return count_good, count_all

    def show_informative_features(self, slice_size = 10):
        """
        Ispisuje najinformativnije osobine
        """
        maxprob = {}
        minprob = {}
        for (label, fname), prob_dist in self.likelihood.items():
            for fval, count in prob_dist.items():
                feature = (fname, fval)
                maxprob[feature] = max(count, maxprob.get(feature, float('-inf')))
                minprob[feature] = min(count, minprob.get(feature, float('inf')))

        prob = {feature: maxprob[feature] / minprob[feature] for feature in minprob}
        prob = [(feature, prob[feature]) for feature in sorted(prob, key = prob.get, reverse = True)[:slice_size]]
        for (fname, fval), ratio in prob:
            maxim = {label: self.likelihood[label, fname].get(fval, 0) for label in self.prior}
            maxim = sorted(maxim, key=maxim.get, reverse=True)
            print('\t%10s = %-10r\t%6s : %-6s = %.1f : 1.0' % (fname, fval, maxim[0], maxim[1], ratio))

    def show_errors(self, labeled_data, slice_size = 100):
        """
        Za označene podatke labeled_data vraća pogrešno klasificirane
        """
        errors = []
        for word, label in labeled_data:
            predict_label = self.classify(word)
            if predict_label != label:
                errors.append((label, predict_label, word))
        errors.sort()

        errors = errors[:slice_size]
        if errors:
            print('\tCorrect    Predicted  Word')
            print('\t--------------------------')
            for er in errors:
                print('\t%-10s %-10s %s' % er)
        return errors

def test_randomness():
    random.seed(0)
    temp = list(range(100))
    random.shuffle(temp)
    success = temp == [23, 8, 11, 7, 48, 13, 1, 91, 94, 54, 16, 63, 52, 41, 80, 2, 47, 87, 78, 66, 19, 6, 24, 10, 59, 30, 22, 29, 83, 37, 93, 81, 43, 99, 86, 28, 34, 88, 44, 14, 84, 70, 4, 20, 15, 21, 31, 76, 57, 67, 73, 50, 69, 25, 98, 46, 96, 0, 72, 35, 58, 92, 3, 95, 56, 90, 26, 40, 55, 89, 75, 71, 60, 42, 9, 82, 39, 18, 77, 68, 32, 79, 12, 85, 36, 17, 64, 27, 74, 45, 61, 38, 51, 62, 65, 33, 5, 53, 97, 49]
    if success:
        print('[INFO] Random seed OK')
    else:
        print('[WARNING] Random seed is WRONG! Test results may not be the same!')

def evaluate_classifier(train_data, test_data, features_factory, slice_features, slice_errors, output = None):
    print('*' * 60)
    print("[INFO] Classifier with %s" % features_factory.__name__.upper())
    classifier = NBClassifier(features_factory)

    print("[INFO] Training size: %d" % len(train_data))
    classifier.train(train_data)

    count_good, count_all = classifier.accuracy(test_data)
    if output is not None:
        if (count_good, count_all) == output:
            success = " OK  "
        else:
            success = "WRONG"
        print("[%s]\tAccuracy: %d/%d = %.3f%%\n\t\tExpected: %d/%d = %.3f%%" %
            (success, count_good, count_all, count_good/count_all*100, output[0], output[1], output[0]/output[1]*100))
    else:
        print("[INFO]\tAccuracy: %d/%d = %.3f%%" % (count_good, count_all, count_good/count_all*100))

    print("[INFO] Informative features...")
    classifier.show_informative_features(slice_features)

    print("[INFO] Errors...")
    classifier.show_errors(test_data, slice_errors)


# PREPARING DATA
test_randomness()
NAMES_PATH = './names/'

labeled_data = get_labeled_data(NAMES_PATH)
train_data, test_data = split_train_test_data(labeled_data)

# EVALUATING 1
def make_letter_features(word):
    """
    ulaz:
     word - riječ
    izlaz:
     rječnik čiji je ključ 'last_letter', a vrijednost zadnje slovo riječi

    Na primjer:
    Ako je riječ 'John', vratit će se rječnik {'last_letter': 'n'}
    """
    return {'last_letter': word[-1]}
evaluate_classifier(train_data, test_data, make_letter_features, 0, 0, (1475,1987))

# EVALUATING 2
def make_suffix_features(word):
    """
    ulaz:
     word - riječ
    izlaz:
     rječnik čiji su ključevi i vrijednosti oblika:
       'suffix1' - zadnje slovo riječi
       'suffix2' - zadnja 2 slova riječi

    Na primjer:
    Ako je riječ 'John', vratit će se rječnik {'suffix1': 'n', 'suffix2': 'hn'}
    """
    return {'suffix1': word[-1], 'suffix2': word[-2:]}

evaluate_classifier(train_data, test_data, make_suffix_features, 0, 0, (1552,1987))

# CUSTOM EVALUATING
def make_custom_features(word):

    return {
        'suffix1': word[-1:],
        'suffix2': word[-2:],
        'suffix3': word[-3:],
        'suffix4': word[-4:],
        'prefix1': word[0]
        #'ali': 'ali' in word
        #'lenset': tuple(sorted(set(word[-3:])))

    }

evaluate_classifier(train_data, test_data, make_custom_features, 10, 0)

