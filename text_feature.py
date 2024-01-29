from utils.dict_lib import agr_functions


class TextFeature():
    
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
