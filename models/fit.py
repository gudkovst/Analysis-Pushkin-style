import keras.models
import matplotlib.pyplot as plt
from models.data import Data


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
