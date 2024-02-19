from periods import periods as prs, period_type
from main_extractor import extract_period
from utils.dict_lib import top_n
from utils.show import *


barh_features = ['words', 'puncts', 'parts', 'rels', 'n_grams_all_symb', 'n_grams_letter', 'n_grams_word', 'n_grams_punct'] 
bar_features = ['len_words', 'count_words_in_sentence', 'count_puncts_in_sentence']
emp_features = ['count_puncts_in_sentence', 'count_words_in_sentence', 'len_words', 'homogeneity', 'rank']


def label(period: list[str]) -> str:
    return f'{period[0]} - {period[-1]}'


def get_path(feature: str, period: list[str]) -> str:
     return f'features_distributions\{feature}\{label(period)}'


def barh_periods(features: list[str] = barh_features, periods: list[period_type] = prs, n: int = 20, save: bool = False) -> None:
    for feature in features:
        for period in periods:
            d = top_n(extract_period(period, feature), n)
            path = get_path(feature, period)
            show_barh(d, create_title(period, feature), save, path)
        

def bar_periods(features: list[str] = bar_features, periods: list[period_type] = prs, save: bool = False) -> None:
    for feature in features:
        for period in periods:
            d = extract_period(period, feature)
            path = get_path(feature, period)
            show_bar(d, create_title(period, feature), save, path)
            
        

def emp_periods(features: list[str] = emp_features, periods: list[period_type] = prs, save: bool = False) -> None:
    for feature in features:
        plt.title(feature)
        for period in periods:
            d = list(extract_period(period, feature).keys())
            sns.kdeplot(d, cumulative=True, label=label(period))
        plt.legend(title='Periods')
        if save:
            save_pict(get_path(feature, ['0', '7']))
        plt.show()

        
if __name__ == '__main__':
    barh_periods(save=True)
    bar_periods(save=True)
    emp_periods(save=True)
