from models.data import *
from periods import *
from utils.text_feature import *
from utils.ensemble_metadata import get
from utils.show import confusion_matrix

from keras import models
from typing import TypeAlias

conf_matrix: TypeAlias = None


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
        p = model.predict(d)
        preds.append(p)
    for i, td in enumerate(data):
        prs = {}
        for j, pr in enumerate(preds):
            prs[model_names[j]] = pr[i][0]
        td.predict_dict = prs


def get_classes_ticks(periods: list[period_type]) -> list[str]:
    return [f'{period[0]} - {period[-1]}' for period in periods]


def threshold(val: float, tr: float) -> int:
    return 0 if val < tr else 1


def pred2label(pred: int) -> int:
    from random import shuffle, choice
    a0 = [i for i in range(5)] + [6, 7, 13]
    a01, a23 = [5, 8, 9, 10, 12], [18, 20, 28]
    a3 = [17, 24, 25]
    convs = {i: [0] for i in a0} | {i: [0, 1] for i in a01} | {i: [3] for i in a3} | {i: [2, 3] for i in a23}
    convs |= {11: [0, 0, 1, 2], 14: [0, 0, 0, 1, 1], 15: [0]*4 + [1, 1, 2, 2, 3], 16: [2], 19: [0, 1, 2, 2, 3], 21: [0, 2, 3], 22: [0, 2, 2, 3, 3]}
    convs |= {23: [0, 1] + [2, 3]*3, 26: [0, 1, 2, 3], 27: [0, 1] + [2, 3]*4, 29: [0, 1, 3] + [2, 3]*2, 30: [0, 0, 1] + [2, 3]*4, 31: [0, 1, 3] + [2, 3]*2}
    pr = convs[pred]
    shuffle(pr)
    return choice(pr)


def ensemble_thresholds_test(models: list[str], quorum: int) -> conf_matrix:
    fs = get(models, "features")
    borders = get(models, "borders")
    tr = get(models, "thresholds")
    data = ensemble_test_data(fs, borders, quorum)
    print(f"size data = {len(data)}")
    predict_list(models, data)
    labels = [td.label for td in data]
    predicts = []
    for td in data:
        if not td.predicted:
            continue
        pr = [td.predict_dict[model] for model in models]
        pr_labels = [threshold(p, t) for p, t in zip(pr, tr)]
        s = ''.join([str(p) for p in pr_labels])
        predicts.append(pred2label(int(s, 2)))
    return confusion_matrix(labels, predicts, get_classes_ticks(periods))


def ensemble_thresholds_explore(models: list[str], quorum: int) -> list:
    fs = get(models, "features")
    borders = get(models, "borders")
    tr = get(models, "thresholds")
    data = ensemble_test_data(fs, borders, quorum)
    print(f"size data = {len(data)}")
    predict_list(models, data)
    k = 2 ** len(models)
    preds = [[] for i in range(k)]
    for td in data:
        if not td.predicted:
            continue
        pr = [td.predict_dict[model] for model in models]
        pr_labels = [threshold(p, t) for p, t in zip(pr, tr)]
        s = ''.join([str(p) for p in pr_labels])
        preds[int(s, 2)].append(td.label)
    return confusion_matrix(labels, preds, get_classes_ticks(periods))


def add(base: list, addition: list) -> list:
    assert len(base) == len(addition)
    return [b + a for b, a in zip(base, addition)]


def ensemble_parts_explore(models: list[str], quorum: int) -> confusion_matrix:
    fs = get(models, "features")
    borders = get(models, "borders")
    tr = get(models, "thresholds")
    data = ensemble_test_data(fs, borders, quorum)
    print(f"size data = {len(data)}")
    predict_list(models, data)
    labels = [td.label for td in data]
    predicts = []
    for td in data:
        if not td.predicted:
            continue
        preds = [0] * len(periods)
        if "model1" in models:
            p = td.predict_dict["model1"]
            p01 = (1 - p) / 2
            p23 = p / 2
            preds = add(preds, [p01, p01, p23, p23])
        if "model2" in models:
            p = td.predict_dict["model2"]
            p0 = 1 - p
            p123 = p / 3
            preds = add(preds, [p0, p123, p123, p123])
        if "model4" in models or "model4-1" in models:
            p = (td.predict_dict.get("model4", 0) + td.predict_dict.get("model4-1", 0)) / 2
            p012 = p / 3
            p3 = 1 - p
            preds = add(preds, [p012, p012, p3, p3])
        if "model5" in models:
            p = td.predict_dict["model5"]
            p1 = (1 - p) / 3
            p2 = p / 3
            preds = add(preds, [0, p1, p2, 0])
        predicts.append(preds.index(max(preds)))
    ticks = [f'{period[0]} - {period[-1]}' for period in periods]
    return confusion_matrix(labels, predicts, ticks)
        