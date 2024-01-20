import os
from features import extract, features

periods = [['1813', '1814', '1815'],
           ['1816', '1817'],
           ['1817 после Лицея', '1818', '1819', '1820'],
           ['1820 Юг', '1821'],
           ['1822', '1823', '1824'],
           ['1824 Михайловское', '1825', '1826'],
           ['1827', '1828', '1829'],
           ['1830'],
           ['1831', '1832'],
           ['1833', '1834', '1835', '1836']]


def dict_sort(d: dict) -> dict:
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))


def selection(d: dict, border: int) -> dict:
    return dict(item for item in d.items() if item[1] > border)


def agregate(f: dict, s: dict) -> dict:
    for key in s:
        f[key] = f.get(key, 0) + s[key]
    return f


def extract_period(period: list, feature_name: str, params: dict = {}) -> dict:
    root = "C:\\Users\\User\\Desktop\\практика\\полное собрание\\poems_corpus"
    feature = features[feature_name]
    res = dict()
    for year in period:
        direct = root + "\\" + year
        for file in os.listdir(direct):
            filename = direct + "\\" + file
            res = agregate(res, extract(feature, filename, params))
    return res


def extract_all_periods(feature_name: str, params: dict = {}) -> dict:
    res = dict()
    for period in periods:
        res = agregate(res, extract_period(period, feature_name, params))
    return res


def rank_period(period: list) -> dict:
    words_dict = extract_period(period, words)
    words_dict = dict_sort(words_dict)
    res = dict()
    for i, word in enumerate(words_dict):
        res[i] = word
    return res


def global_word_rank() -> dict:
    words_dict = extract_all_periods(words)
    words_dict = dict_sort(words_dict)
    res = dict()
    for i, word in enumerate(words_dict):
        res[word] = i
    return res


def main():
    print(extract_all_periods('words')['где'])
main()
