from typing import assert_never

from utils.dict_lib import agr_functions


class TextFeature:
    
    def __init__(self, feature_name: str, agr_func: str, params: dict = {}, args: tuple = ()):
        self.feature_name: str = feature_name
        self.agr_func: callable = agr_functions[agr_func]
        self.params: dict = params
        self.args: tuple = args

    def to_list(self, feature: dict) -> list[float]:
        f = self.agr_func(feature, *self.args)
        match f:
            case float():
                return [f]
            case dict():
                return [f[arg] for arg in self.args]
            case _ as unreachable:
                assert_never(unreachable)

                
def count_features(features: list[TextFeature]) -> int:
    res = 0
    for feature in features:
        res += len(feature.args) or 1
    return res


def get_names(features: list[TextFeature]) -> list[str]:
    names = []
    for feature in features:
        if feature.agr_func.__name__ == "select_keys_proportion":
            for arg in feature.args:
                names.append(feature.feature_name + '/' + arg)
        else:
            names.append(feature.feature_name)
    return names
