import keras.models
import matplotlib.pyplot as plt
import shap
from pandas import DataFrame

from models.data import Data, root
from utils.show import save_pict, show_graphic


def fit(model: keras.models, data: Data, epochs: int) -> None:
    val_data = (data.x_val, data.y_val) if len(data.x_val) else None
    history = model.fit(data.x_train, data.y_train, epochs=epochs, validation_data=val_data)
    history_dict = history.history
    results = model.evaluate(data.x_test, data.y_test)
    print(results)
    
    loss_values = history_dict['loss']
    val_loss_values = history_dict.get('val_loss', None)
    show('Loss', epochs, loss_values, 'Training loss', val_loss_values, 'Validation loss')

    acc_values = history_dict['acc']
    val_acc_values = history_dict.get('val_acc', None)
    show('Accuracy', epochs, acc_values, 'Training acc', val_acc_values, 'Validation acc')
    

def show(title: str, epochs: int, values: list[float], label: str, vals: list[float] = None, lab: str = None) -> None:
    epochs_range = range(1, epochs + 1)
    plt.plot(epochs_range, values, 'bo', label=label)
    if vals:
        plt.plot(epochs_range, vals, 'b', label=lab)
    plt.title(title)
    plt.legend()
    plt.show()


def get_metrics(predicts: list, labels: list, threshold: float) -> dict:
    preds = [1 if c[0] > threshold else 0 for c in predicts]
    tp = sum([l == preds[i] == 1 for i, l in enumerate(labels)])
    fp = sum([l != preds[i] == 1 for i, l in enumerate(labels)])
    tn = sum([l == preds[i] == 0 for i, l in enumerate(labels)])
    fn = sum([l != preds[i] == 0 for i, l in enumerate(labels)])
    metrics = dict()
    if tp + fp == 0:
        return metrics
    metrics['precision'] = tp / (tp + fp)
    metrics['recall'] = tp / (tp + fn)
    metrics['fpr'] = fp / (fp + tn)
    metrics['acc'] = (tp + tn) / (tp + tn + fp + fn)
    metrics['f1'] = 2 * metrics['precision'] * metrics['recall']
    if metrics['f1']:
        metrics['f1'] /= (metrics['precision'] + metrics['recall'])
    return metrics


def auc(x: list[float], y: list[float]) -> float:
    # x must be sorted
    area = 0
    for i in range(1, len(x)):
        area += (x[i] - x[i - 1]) * (y[i] + y[i - 1]) / 2
    return area


def show_metrics(predicts: list, labels: list, n: int = 20) -> None:
    thresholds = [i / n for i in range(n)]
    precisions = []
    recalls = []
    fprs = []
    for t in thresholds:
        pr = get_metrics(predicts, labels, t)
        if not pr:
            break
        precisions.append(pr['precision'])
        recalls.append(pr['recall'])
        fprs.append(pr['fpr'])
        print(f"threshold {t}: acc = {pr['acc']}, precision = {pr['precision']}, recall = {pr['recall']}, f1 = {pr['f1']}, fpr = {pr['fpr']}")
    print(f"auc roc = {auc(fprs[::-1], recalls[::-1])}")
    show_graphic(recalls, precisions, "Precision-Recall curve")
    show_graphic(fprs, recalls, "ROC-curve")

    
def shap_explain(data: Data, names: list[str], predict: callable, save_name: str) -> None:
    x = data.x_train + data.x_val + data.x_test
    df = DataFrame(x, columns=names)
    explainer = shap.KernelExplainer(predict, df)
    shap_values = explainer.shap_values(df)
    shap.summary_plot(shap_values[0], df, max_display=len(df.columns), show=False)
    save_pict(root + 'models\\saved_models\\shap\\' + save_name)
