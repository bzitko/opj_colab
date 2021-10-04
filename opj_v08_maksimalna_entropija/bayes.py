import random
import os


def read_datasets(dataset_path):
    dataset = []
    classes = []
    for filename in os.listdir(dataset_path):
        if filename.endswith(".txt"):
            c = filename.replace(".txt", "")
            classes.append(c)
            for d in open(os.path.join(dataset_path, filename)).read().strip().split():
                dataset.append((d.lower(), c))
    return dataset, classes


def split_datasets(dataset, train_percent=0.8):
    random.shuffle(dataset)
    train_size = round(len(dataset) * train_percent)
    return dataset[:train_size], dataset[train_size:]


def feature(d):
    return d[-2:]


dataset, classes = read_datasets("names")
trainset, testset = split_datasets(dataset)


def train(trainset, classes):
    featureset = [(feature(d), c) for d, c in trainset]

    prior = {c: 0 for c in classes}
    megadoc = {c: {} for c in classes}
    vocabulary = set()
    for f, c in featureset:
        vocabulary.add(f)
        prior[c] += 1
        if f in megadoc[c]:
            megadoc[c][f] += 1
        else:
            megadoc[c][f] = 1

    return prior, megadoc, vocabulary


def predict(model, d, alfa=1):
    prior, megadoc, vocabulary = model
    f = feature(d)
    post = {c: prior[c] * (megadoc[c].get(f, 0) + alfa) / (len(megadoc[c]) + alfa * len(vocabulary))
            for c in prior}
    return max(post, key=post.get)


def evaluate(model, testset, alfa=1):
    evalset = [(predict(model, d, alfa), c) for d, c in testset]

    tp, fp, tn, fn = 0, 0, 0, 0
    for pc, c in evalset:
        if pc == classes[0] == c:
            tp += 1
        elif pc == classes[0] != c:
            fp += 1
        elif pc == classes[1] != c:
            tn += 1
        elif pc == classes[1] == c:
            fn += 1
    return tp, fp, tn, fn




def print_score(tp, fp, tn, fn):
    a = (tp + fn) / (tp + fp + tn + fn)
    p = tp / (tp + fp)
    r = tp / (tp + tn)
    f1 = 2 * p * r / (p + r)
    print(("+----+----+\n|{: >4}|{: >4}|\n" * 2 + "+----+----+").format(tp, fp, tn, fn))
    print("accuracy   : {:.2f}".format(a))
    print("precission : {:.2f}".format(p))
    print("recall     : {:.2f}".format(r))
    print("f1         : {:.2f}".format(f1))


model = train(trainset, classes)
matrix = evaluate(model, testset, 0.5)
print_score(*matrix)
print(matrix)
