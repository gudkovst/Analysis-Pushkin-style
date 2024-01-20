from utils.dict_lib import dict_sort
from utils.extractors import extract_period, extract_all_periods


def rank(period: list) -> dict:
    words_dict = extract_period(period, 'words')
    words_dict = dict_sort(words_dict)
    res = dict()
    for i, word in enumerate(words_dict):
        res[i] = word
    return res


def global_word_rank() -> dict:
    words_dict = extract_all_periods('words')
    words_dict = dict_sort(words_dict)
    res = dict()
    for i, word in enumerate(words_dict):
        res[word] = i
    return res


period_features_list = [rank]
period_agr_features = {feature.__name__: feature for feature in period_features_list}

all_periods_features_list = [global_word_rank]
all_periods_agr_features = {feature.__name__: feature for feature in all_periods_features_list}
