#!/usr/bin/env python

from keras.models import Sequential, Model
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.layers import Input, Dense, Flatten, Dropout
from keras.utils import to_categorical
from pathlib import Path
import keras
from PIL import Image
import numpy as np

countries = ['japan', 'china', 'brazil']
size = 224
shape = Input(shape=(size, size, 3))
base_model = VGG16(weights='imagenet', include_top=False, input_tensor=shape)

x = base_model.output
top_model = Sequential()
top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
top_model.add(Dense(1024, activation='relu'))
top_model.add(Dense(3, activation='softmax'))
model = Model(input=base_model.input, output=top_model(base_model.output))

print('model.layers:' , len(base_model.layers))
for layer in base_model.layers[:15]:
    layer.trainable = False
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()
model.save('cosplayer-country.h5')
