from keras import models
from keras.layers import Dense
from keras.regularizers import L2


def get_model1(k: int) -> models:
    model = models.Sequential()
    model.add(Dense(16, activation='relu', input_shape=(k,)))
    model.add(Dense(12, activation='silu'))
    model.add(Dense(6, activation='silu'))
    model.add(Dense(4, activation='silu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    return model
