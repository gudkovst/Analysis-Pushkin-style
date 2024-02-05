from utils.features import features
from utils.dict_lib import dict_sort
from text_feature import TextFeature
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
    filename = filepath + ".conllu"
    return extr.extract(filename, feature_name, params)


def text2fеatures(filename: str, features: list[TextFeature]) -> list[float]:
    res = list()
    for feature in features:
        f = extract_text(filename, feature.feature_name, feature.params)
        res.extend(feature.to_list(f))
    return res


def global_word_rank() -> dict:
    words_dict = extract_all_periods('words')
    words_dict = dict_sort(words_dict)
    res = dict()
    for i, word in enumerate(words_dict):
        res[word] = i
    return res
