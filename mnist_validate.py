#!/usr/bin/env python

from keras.datasets import mnist
from keras.utils import np_utils

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

from keras.models import load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam

model = load_model('mnist.model')

score = model.evaluate(X_test, Y_test)
print('[loss, accuracy] = ', score)
