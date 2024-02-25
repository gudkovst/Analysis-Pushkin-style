import matplotlib.pyplot as plt
import seaborn as sns
import os


def save_pict(path: str) -> None:
    filename = path + '.png'
    dir_name = os.path.dirname(filename)
    os.makedirs(dir_name, exist_ok=True)
    plt.savefig(filename)
    

def create_title(period: list[str], feature: str) -> str:
    return feature + f" on {period[0]} - {period[-1]}"


def show_barh(d: dict, title: str, save: bool = False, path: str = '') -> None:
    plt.title(title)
    d_rev = dict(reversed(list(d.items())))
    plt.barh(list(d_rev.keys()), d_rev.values())
    for index, value in enumerate(d_rev.values()):
        plt.text(value, index, str(value))
    if save:
        save_pict(path)
    plt.show()
    
    
def show_bar(d: dict, title: str, save: bool = False, path: str = '') -> None:
    plt.title(title)
    plt.bar(list(d.keys()), d.values())
    if save:
        save_pict(path)
    plt.show()


def show_dict(d: dict, title: str) -> None:
    print(title)
    print(d)

    
def show_graphic(x: list, y: list, title: str) -> None:
    plt.plot(x, y)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.title(title)
    plt.show()
