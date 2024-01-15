import os


def isPunct(line: str) -> bool:
    return line.split()[3] == "PUNCT"


def column(**params) -> dict:
    file = params.get('file')
    col: int = params.get('column')
    res = dict()
    for line in file:
        if not line[0].isdigit():
            continue
        if col == 2:
            worg_regime: bool = params.get('regime')
            if isPunct(line) == worg_regime:
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
    args = params | {'column': 3}
    return column(**args)


def rels(**params) -> dict:
    args = params | {'column': 7}
    return column(**args)


def n_grams_symb(**params) -> dict:
    file = params.get('file')
    n = params.get('n', 3)
    res = dict()
    index = "# text = "
    tail = ""
    for line in file:
        if index not in line:
            continue
        end = -1 if line[-1] == '\n' else len(line)
        tail += line[len(index):end].lower()
        while len(tail) >= n:
            key = tail[:n]
            res[key] = res.get(key, 0) + 1
            tail = tail[1:]
    return res


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
    args = params | {'regime': True}
    return n_grams(**args)


def n_grams_punct(**params) -> dict:
    args = params | {'regime': False}
    return n_grams(**args)


def extract(feature: callable, filepath: str, params: dict = {}) -> dict:
    with open(filepath, encoding='utf-8') as tree_file:
        args = {'file': tree_file} | params
        return feature(**args)


def dict_sort(d: dict) -> dict:
    return dict(sorted(d.items(), key=lambda item: item[1]))


def selection(d: dict, border: int) -> dict:
    return dict(item for item in d.items() if item[1] > border)



def main():
    root = "C:\\Users\\User\\Desktop\\практика\\полное собрание\\poems_corpus"
    for directory in os.listdir(root):
        direct = root + "\\" + directory
        for file in os.listdir(direct):
            filename = direct + "\\" + file
            print(extract(len_words, filename, {'n': 3}))
main()
