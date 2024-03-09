from utils.text_feature import *


def get_features_list(model_names: list[str]) -> list[list[TextFeature]]:
    res = []
    if "model1" in model_names:
        fs = [TextFeature("len_words", "mean_key", args=(25,)),  TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"), 
              TextFeature("count_puncts_in_sentence", "mean_key", args=(30,)), TextFeature("count_words_in_sentence", "mean_key", args=(100,)),
              TextFeature("words", "select_keys_proportion", args=("любовь", "друг", "они", "я", "ты", "она", "что")), 
              TextFeature("puncts", "select_keys_proportion", args=("!",)), TextFeature("parts", "select_keys_proportion", args=("PRON", "ADP", "ADV", "ADJ")), 
              TextFeature("rels", "select_keys_proportion", args=("advmod", "conj", "amod")),
              TextFeature("n_grams_letter", "select_keys_proportion", args=("ной", "енн", "его")), 
              TextFeature("n_grams_all_symb", "select_keys_proportion", args=("ой ",))]
        res.append(fs)
    if "model2" in model_names:
        fs = [TextFeature("len_words", "mean_key", args=(25,)), TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"), 
              TextFeature("words", "select_keys_proportion", args=("любовь", "друг", "вы", "мы", "он", "они")), 
              TextFeature("puncts", "select_keys_proportion", args=("!",)), TextFeature("parts", "select_keys_proportion", args=("PRON", "PROPN")), 
              TextFeature("rels", "select_keys_proportion", args=("nsubj", "advmod", "amod", "obl", "nmod")),
              TextFeature("n_grams_all_symb", "select_keys_proportion", args=(" не", "не ", " мо")),
              TextFeature("n_grams_letter", "select_keys_proportion", args=("ста", "его"))]
        res.append(fs)
    if "model4" in model_names:
        fs = [TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"), 
              TextFeature("count_puncts_in_sentence", "mean_key", args=(25,)), TextFeature("count_words_in_sentence", "mean_key", args=(75,)),
              TextFeature("words", "select_keys_proportion", args=("я", "что")), TextFeature("parts", "select_keys_proportion", args=("ADJ", "PRON", "PART")), 
              TextFeature("rels", "select_keys_proportion", args=("conj", "advmod", "amod", "case", "obl", "obj", "nmod")),
              TextFeature("n_grams_all_symb", "select_keys_proportion", args=("ой ",)),
              TextFeature("n_grams_letter", "select_keys_proportion", args=("ный", "ста", "его", "что"))]
        res.append(fs)
    if "model4-1" in model_names:
        fs = [TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"), TextFeature("len_words", "mean_key", args=(25,)),
              TextFeature("count_puncts_in_sentence", "mean_key", args=(25,)), TextFeature("count_words_in_sentence", "mean_key", args=(100,)),
              TextFeature("words", "select_keys_proportion", args=("я", "что")), TextFeature("puncts", "select_keys_proportion", args=("!",)),
              TextFeature("parts", "select_keys_proportion", args=("ADJ", "PRON", "PART")), 
              TextFeature("rels", "select_keys_proportion", args=("conj", "advmod", "amod", "case", "obl", "obj", "nmod")),
              TextFeature("n_grams_letter", "select_keys_proportion", args=("ный", "ста", "его", "ень", "что"))]
        res.append(fs)
    if "model5" in model_names:
        fs = [TextFeature("len_words", "mean_key", args=(25,)), TextFeature("homogeneity", "mean_key", args=(100,)), TextFeature("rank", "mean_key"),
              TextFeature("count_words_in_sentence", "mean_key", args=(100,)), TextFeature("words", "select_keys_proportion", args=("что",)),
              TextFeature("puncts", "select_keys_proportion", args=("!", "?")), TextFeature("parts", "select_keys_proportion", args=("ADJ", "PRON", "ADV")), 
              TextFeature("rels", "select_keys_proportion", args=("conj", "advmod", "amod")),
              TextFeature("n_grams_all_symb", "select_keys_proportion", args=(" на", " по")),
              TextFeature("n_grams_letter", "select_keys_proportion", args=("енн", "ень", "как", "что", "люб"))]
        res.append(fs)
    return res


def get_borders(model_names: list[str]) -> list[int]:
    res = []
    if "model1" in model_names:
        res.append(12)
    if "model2" in model_names:
        res.append(14)
    if "model4" in model_names:
        res.append(11)
    if "model4-1" in model_names:
        res.append(14)
    if "model5" in model_names:
        res.append(9)
    return res
