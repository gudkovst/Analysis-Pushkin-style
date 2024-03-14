from models.data import *
from periods import periods
from utils.text_feature import *
from utils.ensemble_metadata import get

from keras import models


class TextData:

    def __init__(self, sample: list[float], label: int):
        self.samples = [sample]
        self.label = label
        self.predicted = False

    @property
    def predict_dict(self):
        return self.__predict_dict

    @predict_dict.setter
    def predict_dict(self, predict: dict[str, float]):
        self.predicted = True
        self.__predict_dict = predict

    def add_sample(self, sample: list[float]) -> None:
        self.samples.append(sample)

    def quorum(self, borders: list[int], q: int) -> bool:
        k = 0
        for i, sample in enumerate(self.samples):
            if len(sample) - sample.count(0.0) >= borders[i]:
                k += 1
        return k >= q


def ensemble_test_data(lists_fs: list[list[TextFeature]], borders: list[int], q: int) -> list[TextData]:
    if not lists_fs:
        return []
    all_data = []
    for features in lists_fs:
        d = get_data(periods, features, train_part=0, val_part=0)
        if all_data:
            assert d.size() == all_data[-1].size()
        all_data.append(d)
    data = []
    for i, x in enumerate(all_data[0].x_test):
        td = TextData(x, all_data[0].y_test[i])
        for d in all_data[1:]:
            td.add_sample(d.x_test[i])
        if td.quorum(borders, q):
            data.append(td)
    return data


def predict_list(model_names: list[str], data: list[TextData]) -> None:
    preds = []
    for i, name in enumerate(model_names):
        model = models.load_model(root + f"models\\saved_models\\{name}.keras")
        d = [td.samples[i] for td in data]
        print(len(d))
        p = model.predict(d)
        preds.append(p)
    for i, td in enumerate(data):
        prs = {}
        for j, pr in enumerate(preds):
            prs[model_names[j]] = pr[i]  
        td.predict_dict = prs


def predict():
    pass


def ensemble4():
    models = ["model4", "model4-1"]
    fs = get(models, "features")
    borders = get(models, "borders") 
    tr = get(models, "thresholds")
    data = ensemble_test_data(fs, borders, 1)
    predict_list(models, data)
    preds = []
    labels = []
    for td in data:
        if not td.predicted:
            continue
        pr4 = td.predict_dict["model4"]
        pr4_1 = td.predict_dict["model4-1"]
        if pr4 < tr[0] and pr4_1 < tr[1]:
            labels.append(td.label)
            preds.append(0)
        elif pr4 > tr[0] and pr4_1 > tr[1]:
            labels.append(td.label)
            preds.append(3)
        else:
            labels.append(td.label)
            preds.append(3)
    tp = sum([l == preds[i] == 3 for i, l in enumerate(labels)])
    fp = sum([l != preds[i] == 1 for i, l in enumerate(labels)])
    tn = sum([l == preds[i] == 0 for i, l in enumerate(labels)])
    fn = sum([l != preds[i] == 0 for i, l in enumerate(labels)])
    print(tp, fp, tn, fn)
    if tp + fp == 0:
        return
    print(f"precision = {tp / (tp + fp)}")
    print(f'recall = {tp / (tp + fn)}')
    print(f'fpr = {fp / (fp + tn)}')
    print(f'acc = {(tp + tn) / (tp + tn + fp + fn)}')
