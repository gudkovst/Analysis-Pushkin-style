from keras import models
from keras.layers import Dense


def get_dense_model(k_input: int, neurons: list[int]) -> models:
    model = models.Sequential()
    model.add(Dense(neurons[0], activation='relu', input_shape=(k_input,)))
    for neuron in neurons[1:]:
        model.add(Dense(neuron, activation='silu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    return model
