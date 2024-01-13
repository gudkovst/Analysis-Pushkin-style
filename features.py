import os


def isPunct(line: str) -> bool:
    return line.split()[3] == "PUNCT"


def words(**params) -> dict:
    file = params.get('file')
    res = dict()
    for line in file:
        if not line[0].isdigit():
            continue
        key = line.split()[2]
        if not isPunct(line):
            res[key] = res.get(key, 0) + 1
    return res


def len_words(**params) -> dict:
    file = params.get('file')
    res = dict()
    for line in file:
        if not line[0].isdigit():
            continue
        key = line.split()[2]
        if not isPunct(line):
            k = len(key)
            res[k] = res.get(k, 0) + 1
    return res


def puncts(**params) -> dict:
    file = params.get('file')
    res = dict()
    for line in file:
        if not line[0].isdigit():
            continue
        key = line.split()[2]
        if isPunct(line):
            res[key] = res.get(key, 0) + 1
    return res


def parts(**params) -> dict:
    file = params.get('file')
    res = dict()
    for line in file:
        if not line[0].isdigit():
            continue
        key = line.split()[3]
        res[key] = res.get(key, 0) + 1
    return res



def rels(**params) -> dict:
    file = params.get('file')
    res = dict()
    for line in file:
        if not line[0].isdigit():
            continue
        key = line.split()[7]
        res[key] = res.get(key, 0) + 1
    return res


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


def n_grams_word(**params) -> dict:
    file = params.get('file')
    n = params.get('n', 3)
    res = dict()
    window = []
    index = 0
    for line in file:
        if not line[0].isdigit():
            continue
        key = line.split()[2]
        if not isPunct(line):
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


def n_grams_punct(**params) -> dict:
    file = params.get('file')
    n = params.get('n', 3)
    res = dict()
    window = []
    index = 0
    for line in file:
        if not line[0].isdigit():
            continue
        key = line.split()[2]
        if isPunct(line):
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
            print(extract(rels, filename, {'n': 3}))
main()
