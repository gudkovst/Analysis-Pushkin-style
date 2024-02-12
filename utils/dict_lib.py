
def dict_sort(d: dict, regime: int = 1, reverse: bool = True) -> dict:
    return dict(sorted(d.items(), key=lambda item: item[regime], reverse=reverse))


def selection(d: dict, down: float = float('-inf'), up: float = float('inf')) -> dict:
    return dict(item for item in d.items() if up >= item[1] >= down)


def agregate(f: dict, s: dict) -> dict:
    for key in s:
        f[key] = f.get(key, 0) + s[key]
    return f


def top_n(d: dict, n: int, loser_reg: bool = False) -> dict:
    d_sort = dict_sort(d, reverse=not loser_reg)
    vals = list(d_sort.values())
    index = n - 1 if n <= len(vals) else -1
    if loser_reg:
        return selection(d_sort, up=vals[index])
    return selection(d_sort, down=vals[index])


def mean_key(d: dict, *args) -> float:
    n = args[0] if len(args) else 1
    s = 0
    for key in d:
        s += key * d[key]
    return s / sum(d.values()) / n


def select_keys_proportion(d: dict, *keys) -> dict:
    count = sum(d.values())
    return {key: d.get(key, 0) / count for key in keys}


agr_func_list = [mean_key, select_keys_proportion]

agr_functions = {func.__name__: func for func in agr_func_list}
