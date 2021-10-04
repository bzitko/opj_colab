# coding = utf-8
import os
import shutil
import random

path = './data/'

def read_info(path):
    kontinenti = {}
    drzave = []
    for filename in os.listdir('.'):
        if filename.endswith('.txt'):
            kontinent = filename.strip('.txt')
            drzave = open(filename, 'r', encoding='utf8').read().split('\n')
            kontinenti[kontinent] = drzave
    return kontinenti
            


def generate_train(kontinenti, min_max_broj_doc = (10, 30), path = './train/'):
    
    if not os.path.exists(path):
        os.mkdir(path)
    for kontinent in kontinenti:
        subpath = path + kontinent + '/'
        if os.path.exists(subpath):
            shutil.rmtree(subpath)
        os.mkdir(subpath)
        broj_doc = random.randint(*min_max_broj_doc)
        for i in range(1, broj_doc + 1):
            filename = subpath + kontinent + str(i).rjust(2, '0') + '.txt'
            print(filename)
            size = random.randint(2, len(kontinenti[kontinent]) * 2)
            drzave = []
            for _ in range(size):
                drzave.append(random.choice(list(kontinenti[kontinent])))
            
            ostali_kontinenti = list(set(kontinenti) - {kontinent})
            random.shuffle(ostali_kontinenti)
            size = random.randint(2, size)
            for k in ostali_kontinenti:
                ostale_drzave = kontinenti[k]

                delta = random.randint(0, min(size, len(ostale_drzave)))
                for _ in range(delta):
                    drzave.append(random.choice(ostale_drzave))
                size -= delta
                if size <= 0:
                    break

            
            random.shuffle(drzave)
            txt = ' '.join(drzave)
            open(filename, 'w', encoding='utf8').write(txt)
            
            

    


kontinenti = read_info('.')
generate_train(kontinenti)

        