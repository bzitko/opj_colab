import random
import math
import os
# import string


def read_dataset(dataset_path):
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


def build_vector(dataset):
    return sorted({feature(d) for d, _ in dataset})


def make_doc2features(dataset, feature):
    print("discovering features...")
    vector = build_vector(dataset)

    def d2f(d):
        f = feature(d)
        return [int(v == f) for v in vector]

    return d2f




def train(trainset, classes):
    print("training...")
    featureset = [(doc2features(d) + [1], c) for d, c in trainset]  # [1] is bias
    size = len(featureset[0][0])
    W = [0] * size
    rate = 0.1

    for epoch in range(20):

        error = 0
        random.shuffle(featureset)
        for X, c in featureset:
            y = int(c == classes[0])
            Y = [y, 1 - y]

            yh = 1 / (1 + math.exp(-sum(w * x for w, x in zip(W, X))))
            Yh = [yh, 1 - yh]

            error += (yh - y) ** 2 / len(X)
            # DL_Dw = [sum((yh - y) for yh, y in zip(Yh, Y)) * x for x in X]
            DL_Dw = [(yh - y) * x for x in X]

            W = [w - rate * dl_dw for w, dl_dw in zip(W, DL_Dw)]
        print("{}. {:.4f}".format(epoch, error))

        # W = [w - rate * dloss for w, dloss in zip(W, DLOSS)]
        # print(epoch, loss)
    return W


def predict(W, d, classes):
    X = doc2features(d) + [1]
    y = 1 / (1 + math.exp(-sum(w * x for w, x in zip(W, X))))
    Y = [y, 1 - y]

    return classes[0] if y >= 0.5 else classes[1]


def evaluate(W, testset, classes):
    print("evaluating...")
    evalset = [(predict(W, d, classes), c) for d, c in testset]

    tp, fp, tn, fn = 0, 0, 0, 0
    for pc, c in evalset:
        if pc == classes[0] == c:
            tp += 1
        elif pc == classes[0] != c:
            fp += 1
        elif pc == classes[1] != c:
            fn += 1
        elif pc == classes[1] == c:
            tn += 1
    return tp, fp, fn, tn


def measure(tp, fp, fn, tn):
    a = (tp + tn) / (tp + fp + tn + fn)
    p = tp / (tp + fp)
    r = tp / (tp + fn)
    f1 = 2 * p * r / (p + r)
    return a, p, r, f1


def print_score(tp, fp, fn, tn):
    a, p, r, f1 = measure(tp, fp, fn, tn)
    print(("+----+----+\n|{: >4}|{: >4}|\n" * 2 + "+----+----+").format(tp, fp, fn, tn))
    print("accuracy   : {:.4f}".format(a))
    print("precision : {:.4f}".format(p))
    print("recall     : {:.4f}".format(r))
    print("f1         : {:.4f}".format(f1))


dataset, classes = read_dataset("names")
trainset, testset = split_datasets(dataset)

doc2features = make_doc2features(dataset, feature)

W = train(trainset, classes)
matrix = evaluate(W, testset, classes)
print_score(*matrix)
print(matrix)
