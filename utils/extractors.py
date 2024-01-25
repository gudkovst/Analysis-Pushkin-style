from os import listdir
from utils.dict_lib import agregate
from utils.features import features
from periods import periods


root = "C:\\Users\\User\\Desktop\\практика\\полное собрание\\poems_corpus"


def extract(filepath: str, feature_name: str, params: dict = {}) -> dict:
    feature = features[feature_name]
    filename = root + "\\" + filepath
    with open(filename, encoding='utf-8') as tree_file:
        args = {'file': tree_file} | params
        return feature(**args)
    

def extract_period(period: list, feature_name: str, params: dict = {}) -> dict:
    res = dict()
    for year in period:
        direct = root + "\\" + year
        for file in listdir(direct):
            filename = year + "\\" + file
            res = agregate(res, extract(filename, feature_name, params))
    return res


def extract_all_periods(feature_name: str, params: dict = {}) -> dict:
    res = dict()
    for period in periods:
        res = agregate(res, extract_period(period, feature_name, params))
    return res
