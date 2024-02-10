from os import listdir, path
from utils.features import features
from utils.dict_lib import *
from text_feature import TextFeature
from periods import periods
import utils.extractors as extr


def extract_period(period: list, feature_name: str, params: dict = {}) -> dict:
    if feature_name not in features:
        raise ValueError(f"Uncorrect feature_name: {feature_name}")
    if feature_name == "rank":
        params |= {'rank': global_word_rank()}
    return extr.extract_period(period, feature_name, params)


def extract_all_periods(feature_name: str, params: dict = {}) -> dict:
    if feature_name not in features:
        raise ValueError(f"Uncorrect feature_name: {feature_name}")
    if feature_name == "rank":
        params |= {'rank': global_word_rank()}
    return extr.extract_all_periods(feature_name, params)


def extract_text(filepath: str, feature_name: str, params: dict = {}) -> dict:
    if feature_name not in features:
        raise ValueError(f"Uncorrect feature_name: {feature_name}")
    if feature_name == "rank":
        params |= {'rank': global_word_rank()}
    if ".conllu" not in path.basename(filepath):
        filepath += ".conllu"
    return extr.extract(filepath, feature_name, params)


def text2fеatures(filename: str, features: list[TextFeature]) -> list[float]:
    res = list()
    for feature in features:
        f = extract_text(filename, feature.feature_name, feature.params)
        res.extend(feature.to_list(f))
    return res


def period2features(period: list[str], features: list[TextFeature]) -> list[list[float]]:
    res = list()
    for year in period:
        direct = extr.root + "\\" + year
        for file in listdir(direct):
            filename = year + "\\" + file
            res.append(text2fеatures(filename, features))
    return res


def global_word_rank() -> dict:
    words_dict = extract_all_periods('words')
    words_dict = dict_sort(words_dict)
    res = dict()
    for i, word in enumerate(words_dict):
        res[word] = i
    return res


def important_feature(feature: str, n_top: int = 20, rang: tuple[int] = (3, 5), params: dict = {}) -> dict:
    d = dict()
    for period in periods:
        s = {f: 1 for f in top_n(extract_period(period, feature, params), n_top)}
        d = agregate(d, s)
    return selection(d, rang[0], rang[1])
