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
        self.ens_vector = None

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


def ensemble_test_data(lists_fs: list[list[TextFeature]], borders: list[int], q: int,
                       ens_fs: list[TextFeature] = None) -> list[TextData]:
    if not lists_fs:
        return []
    all_data = []
    for features in lists_fs:
        d = get_data(periods, features, train_part=0, val_part=0, is_shuffle=False)
        if all_data:
            assert d.size() == all_data[-1].size()
        all_data.append(d)
    if ens_fs:
        from main_extractor import period2features
        ens_data = period2features(periods, ens_fs)
    data = []
    for i, x in enumerate(all_data[0].x_test):
        td = TextData(x, all_data[0].y_test[i])
        for d in all_data[1:]:
            td.add_sample(d.x_test[i])
        if ens_fs:
            td.ens_vector = ens_data[i]
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


def get_classes_ticks(pers: list[period_type]) -> list[str]:
    return [f'{period[0]} - {period[-1]}' for period in pers]


def threshold(val: float, tr: float) -> int:
    return 0 if val < tr else 1


def add(base: list, addition: list) -> list:
    assert len(base) == len(addition)
    return [b + a for b, a in zip(base, addition)]


def get_p_label(td) -> int:
    preds = [0] * len(periods)
    p = td.predict_dict["model1"]
    p01 = (1 - p) / 2
    p23 = p / 2
    preds = add(preds, [p01, p01, p23, p23])

    p = td.predict_dict["model2"]
    p0 = 1 - p
    p123 = p / 3
    preds = add(preds, [p0, 2.5 * p123, p123, p123])

    p = (td.predict_dict.get("model4", 0) + td.predict_dict.get("model4-1", 0)) / 2
    p012 = p / 3
    p3 = 1 - p
    preds = add(preds, [p012, p012, 2.125 * p012, p3])

    return preds.index(max(preds))


def pred2label_determ(td, pred: int) -> int:
    from random import shuffle, choice
    convs = {3: [1], 6: [0], 7: [0], 10: [1], 11: [1],
             17: [2], 19: [2, 3], 22: [2],
             24: [3], 25: [3], 26: [3], 28: [1], 29: [2],
             30: [3]}
    unconvs = [14, 15, 23, 27, 31]

    if pred in convs:
        pr = convs[pred]
        shuffle(pr)
        return choice(pr)
    elif pred in unconvs:
        return get_p_label(td)
    else:
        raise ValueError(f"index: {pred}")


def ensemble_thresholds_test(models: list[str], quorum: int) -> conf_matrix:
    fs = get(models, "features")
    borders = get(models, "borders")
    tr = get(models, "thresholds")
    data = ensemble_test_data(fs, borders, quorum)
    print(f"size data = {len(data)}")
    predict_list(models, data)
    labels = [td.label for td in data if td.predicted]
    predicts = []
    for td in data:
        if not td.predicted:
            continue
        pr = [td.predict_dict[model] for model in models]
        pr_labels = [threshold(p, t) for p, t in zip(pr, tr)]
        s = ''.join([str(p) for p in pr_labels])
        predicts.append(pred2label_determ(td, int(s, 2)))
    return confusion_matrix(labels, predicts, get_classes_ticks(periods), normalize=True)


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
    return preds
