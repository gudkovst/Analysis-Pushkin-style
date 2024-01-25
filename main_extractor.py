from utils.features import features
from utils.agregate_feature import period_agr_features, all_periods_agr_features
import utils.extractors as extr


def extract_period(period: list, feature_name: str, params: dict = {}) -> dict:
    if feature_name in period_agr_features:
        return period_agr_features[feature_name](period)
    if feature_name in features:
        return extr.extract_period(period, feature_name, params)
    raise ValueError(f"Uncorrect feature_name: {feature_name}")


def extract_all_periods(feature_name: str, params: dict = {}) -> dict:
    if feature_name in all_periods_agr_features:
        return all_periods_agr_features[feature_name]()
    if feature_name in features:
        return extr.extract_all_periods(feature_name, params)
    raise ValueError(f"Uncorrect feature_name: {feature_name}")


def extract_text(filepath: str, feature_name: str, params: dict = {}) -> dict:
    if feature_name in features:
        filename = filepath + ".conllu"
        return extr.extract(filename, feature_name, params)
    raise ValueError(f"Uncorrect feature_name for extract from text: {feature_name}")


def text2fеatures(filename: str, features: list, params: dict = {}) -> list:
    pass