# coding=utf-8

import os
import random
import math

from pprint import pprint


def read_file(filename):
    return [line.strip() for line in open(filename, 'r').read().strip().split()]


def get_labels(data_path):
    return [filename.rstrip('.txt') for filename in os.listdir(data_path) if filename.endswith('.txt')]


def get_labeled_data(data_path):
    klasses = get_labels(data_path)
    return [(doc, klass) for klass in klasses for doc in read_file(data_path + klass + '.txt')]


def split_train_test_data(labeled_data):
    random.seed(0)
    random.shuffle(labeled_data)
    n = 3 * len(labeled_data) // 4
    return labeled_data[:n], labeled_data[n:]


def generate_feature(letter, klass):
    def feature(d, c):
        return 1 if c == klass and d[-1] == letter else 0
    return feature

def make_features(klasses):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    features = [generate_feature(letter, klass) for klass in klasses for letter in alphabet]
    return features


NAMES_PATH = './names/'


C = labels = get_labels(NAMES_PATH)
labeled_data = get_labeled_data(NAMES_PATH)
train_data, test_data = split_train_test_data(labeled_data)
F = features = make_features(labels)


ProbDist = {}
for d, c in train_data:
    if (d, c) in ProbDist:
        ProbDist[d, c] += 1
    else:
        ProbDist[d, c] = 1
ProbDist = {(d, c): num / len(train_data) for (d, c), num in ProbDist.items()}

K = len(features) # broj osobina
L = [0 for _ in features] #lambda vektor
D = documents = [d for d, _ in train_data]

MAXITERATIONS = 2
M = sum(F[j](d, c) for j in range(K) for c in C for d in D)
for iteration in range(MAXITERATIONS):
    pL = {}
    Z = {}
    for d in D:
        Z[d] = sum(math.exp(sum(L[i] * F[i](d, c) for i in range(K))) for c in C)
        for c in C:
            pL[c, d] = math.exp(sum(L[i] * F[i](d, c) for i in range(K))) / Z[d]


    delta = [0 for i in range(K)]


    for i in range(K):
        nominator = sum(ProbDist[d, c] * F[i](d, c) for d, c in train_data)
        if nominator == 0: continue
        denominator = sum(pL[c, d] * F[i](d, c) for c in C for d in D)

        delta[i] = math.log(nominator / denominator) / M
        L[i] += delta[i]



    count, total = 0, 0
    for d, k in test_data:
        z = sum(math.exp(sum(L[i] * F[i](d, c) for i in range(K))) for c in C)
        p = {c:math.exp(sum(L[i] * F[i](d, c) for i in range(K)))/z for c in C}
        c = max(p, key = p.get)
        if c == k:
            count += 1
        total += 1

    print("%d. %d/%d = %d%%" % (iteration, count, total, count/total * 100))



d = "Zoe"

for c in C:
    nominator = math.exp(sum(L[i] * F[i](d, c) for i in range(K)))
    denominator = sum(math.exp(sum(L[i] * F[i](d, k) for i in range(K))) for k in C)


    n = nominator / denominator
    print(c, n)






