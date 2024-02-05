import matplotlib.pyplot as plt
import seaborn as sns


def create_title(period: list, feature: str) -> str:
    return feature + f" on {period[0]} - {period[-1]}"


def label(period: list) -> str:
    return f"{period[0]} - {period[-1]}"


def show_barh(d: dict, title: str) -> None:
    plt.title(title)
    d_rev = dict(reversed(list(d.items())))
    plt.barh(list(d_rev.keys()), d_rev.values())
    for index, value in enumerate(d_rev.values()):
        plt.text(value, index, str(value))
    plt.show()
    
    
def show_bar(d: dict, title: str) -> None:
    plt.title(title)
    plt.bar(list(d.keys()), d.values())
    plt.show()


def show_dict(d: dict, title: str) -> None:
    print(title)
    print(d)
