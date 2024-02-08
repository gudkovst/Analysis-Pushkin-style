
def isPunct(line: str) -> bool:
    return line.split()[3] == "PUNCT"


def column(**params) -> dict:
    file = params.get('file')
    col: int = params.get('column')
    word_regime: bool = params.get('regime')
    res = dict()
    for line in file:
        if not line[0].isdigit():
            continue
        if isPunct(line) == word_regime:
            continue
        key = line.split()[col]
        res[key] = res.get(key, 0) + 1
    return res


def words(**params) -> dict:
    args = params | {'column': 2, 'regime': True}
    return column(**args)


def len_words(**params) -> dict:
    words_dict = words(**params)
    res = dict()
    for word in words_dict:
        ln = len(word)
        res[ln] = res.get(ln, 0) + words_dict[word]
    return res


def count_in_sentence(**params) -> dict:
    file = params.get('file')
    word_regime: bool = params.get('regime')
    res = dict()
    counter = 0
    for line in file:
        if not line[0].isdigit():
            if counter:
                res[counter] = res.get(counter, 0) + 1
                counter = 0
            continue
        if isPunct(line) != word_regime:
            counter += 1
    return res


def count_words_in_sentence(**params) -> dict:
    args = params | {'regime': True}
    return count_in_sentence(**args)


def count_puncts_in_sentence(**params) -> dict:
    args = params | {'regime': False}
    return count_in_sentence(**args)


def puncts(**params) -> dict:
    args = params | {'column': 2, 'regime': False}
    return column(**args)


def parts(**params) -> dict:
    args = params | {'column': 3, 'regime': True}
    return column(**args)


def rels(**params) -> dict:
    args = params | {'column': 7, 'regime': True}
    return column(**args)


def n_grams_symb(**params) -> dict:
    file = params.get('file')
    n = params.get('n', 3)
    letter_regime: bool = params.get('regime')
    res = dict()
    rus_alf = [chr(code) for code in range(ord('а'), (ord('я') + 1))]
    index = "# text = "
    tail = ""
    for line in file:
        if index not in line:
            continue
        end = -1 if line[-1] == '\n' else len(line)
        if letter_regime:
            new_tail = list(filter(lambda s: s in rus_alf, line[len(index):end].lower()))
            tail += "".join(new_tail)
        else:
            tail += line[len(index):end].lower()
        while len(tail) >= n:
            key = tail[:n]
            res[key] = res.get(key, 0) + 1
            tail = tail[1:]
    return res


def n_grams_all_symb(**params) -> dict:
    args = params | {'regime': False}
    return n_grams_symb(**args)


def n_grams_letter(**params) -> dict:
    args = params | {'regime': True}
    return n_grams_symb(**args)


def n_grams(**params) -> dict:
    file = params.get('file')
    n: int = params.get('n', 3)
    word_regime: bool = params.get('regime')
    res = dict()
    window = []
    index = 0
    for line in file:
        if not line[0].isdigit():
            continue
        key = line.split()[2]
        if isPunct(line) != word_regime:
            if index < n:
                window.append(key)
                index += 1
                continue
            window = window[1:]
            window.append(key)
            s = ""
            for w in window:
                s += w + " "
            res[s] = res.get(s, 0) + 1
    return res


def n_grams_word(**params) -> dict:
    n = params.get('n', 2)
    args = params | {'regime': True, 'n': n}
    return n_grams(**args)


def n_grams_punct(**params) -> dict:
    args = params | {'regime': False}
    return n_grams(**args)


def passing(word_list: list) -> list:
    res = [0]
    word_used = set()
    for word in word_list:
        if word in word_used:
            res.append(res[-1])
        else:
            word_used.add(word)
            res.append(res[-1] + 1)
    return res[1:]


def homogeneity(**params) -> dict:
    file = params.get('file')
    word_list = list()
    for line in file:
        if not line[0].isdigit():
            continue
        if not isPunct(line):
            word_list.append(line.split()[2])
    forward = passing(word_list)
    word_list.reverse()
    backward = passing(word_list)
    sub = [f - backward[i] for i, f in enumerate(forward)]
    hom = round(sum(sub) / len(word_list))
    return {hom: 1}


def statistics(**params) -> dict:
    file = params.get('file')
    words_dict = words(**params)
    res = {"texts": 1, "words": sum(words_dict.values()), "unique_words": len(words_dict)}
    file.seek(0)
    puncts_dict = puncts(**params)
    res |= {"puncts": sum(puncts_dict.values()), "unique_puncts": len(puncts_dict)}
    file.seek(0)
    sentences = count_words_in_sentence(**params)
    res |= {"sentence": sum(sentences.values())}
    return res


def rank(**params) -> dict:
    file = params.get('file')
    words_rank = params.get('rank')
    words_dict = words(**params)
    count = sum(words_dict.values())
    rank = 0
    for word in words_dict:
        rank += words_rank[word] * words_dict[word]
    return {rank / count / len(words_rank): 1}


features_list = [words, len_words, count_words_in_sentence, count_puncts_in_sentence, puncts, parts, rels, 
                 n_grams_all_symb, n_grams_letter, n_grams_word, n_grams_punct, statistics, homogeneity, rank]
features = {feature.__name__: feature for feature in features_list}
