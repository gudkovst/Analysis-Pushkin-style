
def dict_sort(d: dict, regime: int = 1) -> dict:
    return dict(sorted(d.items(), key=lambda item: item[regime], reverse=True))


def selection(d: dict, border: int) -> dict:
    return dict(item for item in d.items() if item[1] > border)


def agregate(f: dict, s: dict) -> dict:
    for key in s:
        f[key] = f.get(key, 0) + s[key]
    return f


def top_n(d: dict, n: int) -> dict:
    d_sort = dict_sort(d)
    vals = list(d_sort.values())
    index = n - 1 if n <= len(vals) else -1
    bord = vals[index] - 1
    return selection(d_sort, bord)


def mean_key(d: dict) -> int:
    s = 0
    for key in d:
        s += key * d[key]
    return s / sum(d.values())


def select_keys_proportion(d: dict, keys: list) -> dict:
    count = sum(d.values())
    return {key: d[key] / count for key in keys}
        