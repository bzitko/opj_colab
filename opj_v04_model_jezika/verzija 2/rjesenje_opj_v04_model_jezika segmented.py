# coding=utf-8

import re


FILENAME = "alan_ford_002_suplji_zub segmented.txt"

txt = open(FILENAME, 'r', encoding="utf8").read()

sents = txt.split("\n")

def build_ngram(sent, ngram_size):
    ngram = []
    sent_words = sent.split()
    for i in range(len(sent_words) - ngram_size + 1):
        ngram.append(tuple(sent_words[i:i+ngram_size]))
    return ngram

unigram_model, bigram_model = {}, {}
for sent in sents:
    for unigram in build_ngram(sent, 1):
        unigram_model[unigram] = unigram_model.get(unigram, 0) + 1
    for bigram in build_ngram(sent, 2):
        bigram_model[bigram] = bigram_model.get(bigram, 0) + 1

print("Broj rečenica:\t%d" % len(sents))
print("Broj pojavnica (s ponavljanjem):\t%d" % sum(unigram_model.values()))
print()


print("Veličina unigrama:\t%d" % len(unigram_model))
print("Veličina bigrama:\t%d" % len(bigram_model))
print()

unigram, bigram = "Sir", ('platno', '</s>')
print("Broj pojavljivanja unigrama %s:\t%d" % (unigram, unigram_model[(unigram, )] ))
print("Broj pojavljivanja bigrama %s:\t%d" % (bigram, bigram_model[bigram] ))
print()

freq_unig = {t[0] for t in sorted(unigram_model, key=unigram_model.get, reverse = True)[:10]}
freq_big = {str(t) for t in sorted(bigram_model, key=bigram_model.get, reverse = True)[:10]}
print("10 najčeščih unigrama:\t%s" % ", ".join(sorted(freq_unig)))
print("10 najčešćih bigrama:\t%s" % ", ".join(sorted(freq_big)))
print()


def digram_probability(sentence, model2, model1):
    prob = 1
    for ngram in build_ngram(sentence, 2):
        cnt2 = model2.get(ngram, 0)
        cnt1 = model1.get(ngram[:1], 0)
        prob *= cnt2 / cnt1
    return prob

def digram_probability_laplace(sentence, model2, model1):
    prob = 1
    v = len(model1)
    for ngram in build_ngram(sentence, 2):
        cnt2 = model2.get(ngram, 0) + 1
        cnt1 = model1.get(ngram[:1], 0) + v
        prob *= cnt2 / cnt1
    return prob

s1 = "<s> Tu li zapamtio naziv tvrtke </s>"
s2 = "<s> Moj rođak radi o tom mikrofilmu </s>"
print("Vjerojatnost rečenice %r po bigramu je %f" % (s1, digram_probability(s1, bigram_model, unigram_model)))
print("Vjerojatnost rečenice %r po bigramu je %f" % (s2, digram_probability(s2, bigram_model, unigram_model)))

print()

s1 = "<s> Moj rođak je student </s>"
print("Vjerojatnost rečenice %r po bigramu uz dodaj1 izglađivanje je" % s1, digram_probability_laplace(s1, bigram_model, unigram_model))
#print("Vjerojatnost rečenice %r po bigramu je" % s2, digram_probability_laplace(s2, bigram_model, unigram_model))


import random
def random_chain(model):
    word = '<s>'
    sentence = []
    while word != '</s>':
        next_grams = [gram for gram in model if gram[0] == word]
        if next_grams and len(sentence)<10:
            next_gram = random.choice(next_grams)
            #next_gram = max(next_grams, key = lambda x: model[x])
            sentence.append(next_gram)
            word = next_gram[-1]
            if word == '<s>':
                break
        else:
            break
    print(sentence)
    sentence = ' '.join(' '.join(gram[1:]) for gram in sentence).strip('</sent>')
    print(sentence)


#random_chain(bigram_model)