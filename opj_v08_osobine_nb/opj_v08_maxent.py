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

def get_labeled_data(data_path, featureset=lambda x: x):
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
    return [(featureset(word), label) for label in labels for word in read_file(data_path + label + '.txt')]

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




def test_randomness():
    random.seed(0)
    temp = list(range(100))
    random.shuffle(temp)
    success = temp == [23, 8, 11, 7, 48, 13, 1, 91, 94, 54, 16, 63, 52, 41, 80, 2, 47, 87, 78, 66, 19, 6, 24, 10, 59, 30, 22, 29, 83, 37, 93, 81, 43, 99, 86, 28, 34, 88, 44, 14, 84, 70, 4, 20, 15, 21, 31, 76, 57, 67, 73, 50, 69, 25, 98, 46, 96, 0, 72, 35, 58, 92, 3, 95, 56, 90, 26, 40, 55, 89, 75, 71, 60, 42, 9, 82, 39, 18, 77, 68, 32, 79, 12, 85, 36, 17, 64, 27, 74, 45, 61, 38, 51, 62, 65, 33, 5, 53, 97, 49]
    if success:
        print('[INFO] Random seed OK')
    else:
        print('[WARNING] Random seed is WRONG! Test results may not be the same!')


def gender_features(name):
    return {
        'fl': name[0].lower(),
        'll': name[-1].lower(),
        'ft': name[:2].lower(),
        'lt': name[-2:].lower()
    }


# PREPARING DATA
test_randomness()
NAMES_PATH = './names/'

labeled_data = get_labeled_data(NAMES_PATH, gender_features)
train_data, test_data = split_train_test_data(labeled_data)

counts = {}

for features, label in train_data:
    for f, v in features.items():
        if (f, v, label) in counts:
            counts[f, v, label] += 1
        else:
            counts[f, v, label] = 1
print(counts)


def nemam_pojma():
    F = {}
    for l in 'abcdefghijklmnopqrstuvxyz':
        F[l] = lambda x, y: x[-1] == l

    pXandY = {}
    count = 0
    for i, (x, y) in enumerate(train_data):
        for f in F:
            xx = F[f](x,y)
            
            
            if xx:
                #print(x, xx, y, count)
                count += 1
                pXandY[xx, y] = pXandY.get((xx, y), 0) + 1
    pXandY = {(x, y): p / len(train_data) for (x, y), p in pXandY.items()}
    print(sum(pXandY.values()))


    print(pXandY)



    #p_f = [sum(p_x_y[x, y] * f(x, y) for f in F) for x, y in train_data]

    #lambdas = [0 for _ in F]
    #print(lambdas)