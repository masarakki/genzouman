#!/usr/bin/env python

import os
import numpy as np
import random as rn
import tensorflow as tf
from keras import backend as K

def fix_random():
    os.environ['PYTHONHASHSEED'] = '0'
    np.random.seed(7)
    rn.seed(7)
    session_conf = tf.ConfigProto(
        intra_op_parallelism_threads=1,
        inter_op_parallelism_threads=1
    )


    tf.set_random_seed(7)
    sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
    K.set_session(sess)


#fix_random()

from keras.datasets import mnist
from keras.utils import np_utils
from keras.callbacks import CSVLogger

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

X_validation = X_test[5000:]
Y_validation = Y_test[5000:]

X_test = X_test[:5000]
Y_test = Y_test[:5000]

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam

#for filename, validation_data in [['mnist-train', (X_train, Y_train)],
#                                 ['mnist-test', (X_test, Y_test)],
#                                  ['mnist-validation', (X_validation, Y_validation)]]:

train_data = (X_train, Y_train)
validation_data = (X_test, Y_test)

#for num in ['1']:
#    filename = 'mnist-solo-init-' + num + '.csv'
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])

model.summary()
model.fit(X_train, Y_train, epochs=20,
          validation_data=validation_data,
 #             callbacks=[CSVLogger(filename)],
)
