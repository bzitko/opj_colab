# coding=utf-8

import random
import math
import os


###########################################################################################
### PREPROCESING ###
###########################################################################################

def read_file(filename):
    return [line.strip() for line in open(filename, 'r').read().strip().split()]

def get_labeled_data(data_path):
    labels = [filename.rstrip('.txt') for filename in os.listdir(data_path) if filename.endswith('.txt')]
    return [(word, label) for label in labels for word in read_file(data_path + label + '.txt')]

def split_train_test_data(labeled_data):
    random.seed(0)
    random.shuffle(labeled_data)
    n = 3 * len(labeled_data) // 4
    return labeled_data[:n], labeled_data[n:]

def make_letter_features(word):
    return {'last_letter': word[-1]}

def make_suffix_features(word):
    return {'suffix1': word[-1], 'suffix2': word[-2:]}

def make_rich_features(word):
    features = {}
    features["first_letter"] = word[0].lower()
    features["last_letter"] = word[-1].lower()
    for letter in 'ale':
        #features["count({})".format(letter)] = word.lower().count(letter)
        features["has({})".format(letter)] = (letter in word.lower())
    return features    

class NBClassifier(object):

    def __init__(self, features_factory):
        self.features_factory = features_factory

    def train(self, labeled_data):
        #labeled_festuresets = self.get_labeled_featuresets(labeled_data)

        #self.fnames = set()
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
                #self.fnames.add(fname)

        self.prior = {label: count / len(labeled_data) for label, count in self.prior.items()}


    def classify(self, word):
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
        count_good, count_all = 0, 0
        for word, label in labeled_data:
            predict_label = self.classify(word)
            if predict_label == label:
                count_good += 1
            count_all += 1

        print(count_good, count_all, count_good / count_all)

    def show_informative_features(self, slice_size = 10):
        maxprob = {}
        minprob = {}
        for (label, fname), prob_dist in self.likelihood.items():
            for fval, count in prob_dist.items():
                feature = (fname, fval)
                maxprob[feature] = max(count, maxprob.get(feature, float('-inf')))
                minprob[feature] = min(count, minprob.get(feature, float('inf')))

        prob = {feature: maxprob[feature] / minprob[feature] for feature in minprob}
        prob = [(feature, prob[feature]) for feature in sorted(prob, key = prob.get, reverse = True)[:slice_size]]
        print(prob)

    def show_errors(self, labeled_data, slice_size = 100):
        errors = []
        for word, label in labeled_data:
            predict_label = self.classify(word)
            if predict_label != label:
                errors.append((label, predict_label, word))
        errors.sort()

        for er in errors[:slice_size]:
            print('Correct: %s\tPredicted: %s\tfor %r' % er)
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


test_randomness()
NAMES_PATH = './names/'

labeled_data = get_labeled_data(NAMES_PATH)
train_data, test_data = split_train_test_data(labeled_data)

classifier = NBClassifier(make_letter_features)
classifier.train(train_data)
classifier.classify('Neo')
classifier.classify('Rocky')
classifier.accuracy(test_data)
classifier.show_informative_features()
#classifier.show_errors(test_data)

#print(make_bin_feature('abcda','male', 0.3))
#print(classifier.featurevalues)

