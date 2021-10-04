# coding=utf-8

def read_file(filename):
    labeled_data = []
    for line in open(filename, 'r').read().strip().split('\n'):
        line = line.strip()
        if line:
            word, label = line.split()
            labeled_data.append((word, label))
    return labeled_data


def make_features(labeled_data, prev_label):
    pass

(read_file('./data/dev.txt'))