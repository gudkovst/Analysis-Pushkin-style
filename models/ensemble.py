from models.data import *
from periods import periods
from utils.text_feature import *

from keras import models


class TextData:

    def __init__(self, sample: list[float], label: int):
        self.samples = [sample]
        self.label = label
        self.predicted = False

    @property
    def predict_list(self):
        return self.__predict_list

    @predict_list.setter
    def predict_list(self, predict: list[float]):
        self.predicted = True
        self.predict_list = predict

    def add_sample(self, sample: list[float]) -> None:
        self.samples.append(sample)

    def quorum(self, borders: list[int], q: int) -> bool:
        k = 0
        for i, sample in enumerate(self.samples):
            if len(sample) - sample.count(0.0) >= borders[i]:
                k += 1
        return k >= q


def ansamble_test_data(lists_fs: list[list[TextFeature]], borders: list[int], q: int) -> list[TextData]:
    all_data = []
    for features in lists_fs:
        d = get_data(periods, features, train_part=0, val_part=0)
        if all_data:
            assert d.size() == all_data[-1].size()
        all_data.append(d)
    if not lists_fs:
        return []
    data = []
    for i, x in enumerate(data[0].x_test):
        td = TextData(x, data[0].y_test[i])
        for d in all_data[1:]:
            td.add_sample(d.x_test[i])
        if td.quorum(borders, q):
            data.append(td)
    return data


def predict_list(model_names: list[str], data: list[TextData]) -> None:
    ansamble = []
    for name in model_names:
        ansamble.append(models.load_model(root + f"models\\saved_models\\{name}.keras"))
    for td in data:
        if len(td.samples) != len(ansamble):
            continue
        preds = []
        for i, f in enumerate(td.samples):
            preds.append(ansamble[i].predict(f))
        td.predict_list = preds


def predict():
    pass
