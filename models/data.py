from random import shuffle
from os import path
import sys
root = 'C:\\Users\\User\\Desktop\\практика\\полное собрание\\'
sys.path.append(root)

from periods import period_type
from main_extractor import period2features 
from utils.text_feature import *


class Data():
    
    def __init__(self, train, val, test):
        self.x_train = [f[0] for f in train]
        self.y_train = [f[1] for f in train]
        self.x_val = [f[0] for f in val]
        self.y_val = [f[1] for f in val]
        self.x_test = [f[0] for f in test]
        self.y_test = [f[1] for f in test]
        
    def save(self, filename: str) -> None:
        filen = root + 'models\\data\\' + path.basename(filename) + '.txt'
        with open(filen, 'w') as file:
            for i, x in enumerate(self.x_train):
                record = construct_record('train', self.y_train[i], x)
                file.write(record)
            for i, x in enumerate(self.x_val):
                record = construct_record('val', self.y_val[i], x)
                file.write(record)
            for i, x in enumerate(self.x_test):
                record = construct_record('test', self.y_test[i], x)
                file.write(record)
                
    def size(self) -> int:
        return len(self.x_train) + len(self.x_val) + len(self.x_test)


def construct_record(name: str, y: int, xs: list[float]) -> str:
    record = name + ' ' + str(y)
    for x in xs:
        record += ' ' + str(x)
    record += '\n'
    return record
                
                
def load_data(filename: str) -> Data:
    filen = root + 'models\\data\\' + path.basename(filename) + '.txt'
    train, val, test = [], [], []
    with open(filen, 'r') as file:
        for line in file:
            record = line.split()
            x = [float(s) for s in record[2:]]
            locals()[record[0]].append((x, int(record[1])))
    return Data(train, val, test)

                
def get_data(periods: list[period_type], features: list[TextFeature], labels: list[int], train_part: float = 0.7, val_part: float = 0.15, 
             bord_file_size: int = 0, not_null_bord: int = 0) -> Data:
    fs = list()
    lens_train = list()
    lens_val = list()
    for period in periods:
        f = period2features(period, features, bord_file_size, not_null_bord)
        shuffle(f)
        fs.append(f)
        lens_train.append(int(len(f) * train_part))
        lens_val.append(lens_train[-1] + int(len(f) * val_part))
    train, val, test = [], [], []
    for i, fi in enumerate(fs):
        train += [(f, labels[i]) for f in fi[:lens_train[i]]]
        val += [(f, labels[i]) for f in fi[lens_train[i]:lens_val[i]]]
        test += [(f, labels[i]) for f in fi[lens_val[i]:]]
    shuffle(train)
    shuffle(val)
    shuffle(test)
    return Data(train, val, test)
