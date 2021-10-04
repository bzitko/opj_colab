# coding = utf-8

import os
import re
import json
import math

def write_train(filename, trainset):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(trainset, f)

def read_train(filename):
    txt = open(filename, 'r', encoding='utf8').read()
    return json.loads(txt)

def read_stopwords(filename):
    f = open(filename, 'r')
    stopwords = set()
    for line in f:
        stopwords.add(line.split()[-1].strip())
    f.close()
    return stopwords

stopwords = read_stopwords('stopwords.txt')

def preprocess_data(path):

    trainset = {}

    for cls in os.listdir(path):
        subpath = path + cls + '/'
        files = [subpath + doc for doc in os.listdir(subpath) if os.path.isfile(subpath + doc)]
        trainset[cls] = []
        for filename in files:
            trainset[cls].append(model_doc(filename))

    return trainset

def model_doc(filename):
    txt = open(filename, 'r', encoding='utf8').read()
    #open(filename, 'w', encoding='utf8').write(txt)
    txt = re.sub(r'\d+\n+[\d:,]+ --> [\d:,]+\n+', '',txt)
    txt = re.sub(r'\<\/?\w+\>', '', txt)

    model = {}
    for line in re.findall(r'\S+', txt):
        word = line.strip('.?!,;:-+*/\\"\'[]{}()<>').lower()
        if word and word not in stopwords:
            model[word] = model.get(word, 0) + 1
            
    return model

def classify(model, trainset):
    
    total_cls = sum(len(docs) for docs in trainset.values())
    count_cls = {cls: len(docs) for cls, docs in trainset.items()}
    prob_cls = {cls: count/total_cls for cls, count in count_cls.items()}
    
    
    vocabulary = set()
    for cls, docs in trainset.items():
        for doc in docs:
            vocabulary |= set(doc)


    count_doc = {cls: sum(sum(doc.values()) for doc in docs) + len(vocabulary) for cls, docs in trainset.items()}
    
    prob = {}
    for cls, docs in trainset.items():
        for doc in docs:
            for word in model:
                prob[(word, cls)] = prob.get((word, cls), 1) + doc.get(word, 0)

    prob = {(word, cls): count / count_doc[cls] for (word, cls), count in prob.items()}
    

    final = {}
    for cls in trainset:
        final[cls] = math.log(prob_cls[cls])
        for word, freq in model.items():
            final[cls] += freq * math.log(prob[(word, cls)])
        #final[cls] = 10 ** final[cls]
    print(final)
    final = sorted(final, key=lambda cls: final[cls], reverse=True)
    print(final)
    return


def test_srt():
    FILENAME = 'doctor zhivago [1965].srt'


    #trainset = preprocess_data('train/')

    #write_train('trainset.txt', trainset)
    trainset = read_train('trainset.txt')
    model = model_doc(FILENAME)
    classify(model, trainset)

def test_txt():
    FILENAME = 'd5.txt'
    trainset = preprocess_data('train2/')
    
    write_train('trainset2.txt', trainset)
    trainset = read_train('trainset2.txt')    
    model = model_doc(FILENAME)
    classify(model, trainset)

test_srt()


data = {
    'italy': ['italy florence rome' ],
    'france': ['dog']
}


