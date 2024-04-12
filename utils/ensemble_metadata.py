from utils.text_feature import *


def features() -> dict[str, list[TextFeature]]:
    res = {}
    fs = [TextFeature("len_words", "mean_key", args=(25,)),  TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"), 
          TextFeature("count_puncts_in_sentence", "mean_key", args=(30,)), TextFeature("count_words_in_sentence", "mean_key", args=(100,)),
          TextFeature("words", "select_keys_proportion", args=("любовь", "друг", "они", "я", "ты", "она", "что")), 
          TextFeature("puncts", "select_keys_proportion", args=("!",)), TextFeature("parts", "select_keys_proportion", args=("PRON", "ADP", "ADV", "ADJ")), 
          TextFeature("rels", "select_keys_proportion", args=("advmod", "conj", "amod")),
          TextFeature("n_grams_letter", "select_keys_proportion", args=("ной", "енн", "его")), 
          TextFeature("n_grams_all_symb", "select_keys_proportion", args=("ой ",))]
    res["model1"] = fs
    fs = [TextFeature("len_words", "mean_key", args=(25,)), TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"), 
          TextFeature("words", "select_keys_proportion", args=("любовь", "друг", "вы", "мы", "он", "они")), 
          TextFeature("puncts", "select_keys_proportion", args=("!",)), TextFeature("parts", "select_keys_proportion", args=("PRON", "PROPN")), 
          TextFeature("rels", "select_keys_proportion", args=("nsubj", "advmod", "amod", "obl", "nmod")),
          TextFeature("n_grams_all_symb", "select_keys_proportion", args=(" не", "не ", " мо")),
          TextFeature("n_grams_letter", "select_keys_proportion", args=("ста", "его"))]
    res["model2"] = fs
    fs = [TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"), 
          TextFeature("count_puncts_in_sentence", "mean_key", args=(25,)), TextFeature("count_words_in_sentence", "mean_key", args=(75,)),
          TextFeature("words", "select_keys_proportion", args=("я", "что")), TextFeature("parts", "select_keys_proportion", args=("ADJ", "PRON", "PART")), 
          TextFeature("rels", "select_keys_proportion", args=("conj", "advmod", "amod", "case", "obl", "obj", "nmod")),
          TextFeature("n_grams_all_symb", "select_keys_proportion", args=("ой ",)),
          TextFeature("n_grams_letter", "select_keys_proportion", args=("ный", "ста", "его", "что"))]
    res["model4"] = fs
    fs = [TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"), TextFeature("len_words", "mean_key", args=(25,)),
          TextFeature("count_puncts_in_sentence", "mean_key", args=(25,)), TextFeature("count_words_in_sentence", "mean_key", args=(100,)),
          TextFeature("words", "select_keys_proportion", args=("я", "что")), TextFeature("puncts", "select_keys_proportion", args=("!",)),
          TextFeature("parts", "select_keys_proportion", args=("ADJ", "PRON", "PART")), 
          TextFeature("rels", "select_keys_proportion", args=("conj", "advmod", "amod", "case", "obl", "obj", "nmod")),
          TextFeature("n_grams_letter", "select_keys_proportion", args=("ный", "ста", "его", "ень", "что"))]
    res["model4-1"] = fs
    fs = [TextFeature("len_words", "mean_key", args=(25,)), TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"),
          TextFeature("count_words_in_sentence", "mean_key", args=(100,)), TextFeature("words", "select_keys_proportion", args=("что",)),
          TextFeature("puncts", "select_keys_proportion", args=("!", "?")), TextFeature("parts", "select_keys_proportion", args=("ADJ", "PRON", "ADV")), 
          TextFeature("rels", "select_keys_proportion", args=("conj", "advmod", "amod")),
          TextFeature("n_grams_all_symb", "select_keys_proportion", args=(" на", " по")),
          TextFeature("n_grams_letter", "select_keys_proportion", args=("енн", "ень", "как", "что", "люб"))]
    res["model5"] = fs
    return res


def borders() -> dict[str, int]:
    return {"model1": 12, "model2": 14, "model4": 11, "model4-1": 14, "model5": 9}


def thresholds() -> dict[str, float]:
    return {"model1": 0.55, "model2": 0.6, "model4": 0.55, "model4-1": 0.45, "model5": 0.5}


metadata = {f.__name__: f for f in [features, borders, thresholds]}


def get(model_names: list[str], entity: str) -> list:
    mdata = metadata[entity]()
    return [mdata[model] for model in model_names]
