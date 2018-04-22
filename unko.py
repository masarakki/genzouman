#!/usr/bin/env python

from keras.models import Sequential
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.layers import Input, Dense, Flatten, Dropout
from keras.utils import to_categorical
from pathlib import Path
import keras
from PIL import Image
import numpy as np

countries = ['japan', 'china', 'brazil']

model = Sequential()
shape = Input(shape=(350, 350, 3))
model = VGG16()

#model.add(Flatten(input_shape=(350, 350, 3)))
#model.add(Dense(256, activation='relu'))
#model.add(Dropout(0.5))
#model.add(Dense(len(countries), activation='softmax'))
#model.compile(optimizer='rmsprop',
#              loss='categorical_crossentropy',
#              metrics=['accuracy'])

model.summary()

def resize(image, size):
    left = (image.width - size) / 2
    return image.crop((left, 0, left + size, size))

for index, country in enumerate(countries):
    data = []
    labels = []
    path = Path('test/%s' % country)
    for filename in path.glob('*3.jpg'):
        image = Image.open(filename)
        image = image.convert('RGB')
        image = resize(image, 224)
        image = np.asarray(image)
        image = image.astype('float32')
        image /= 255
        data.append(image)
        labels.append([index])
    data = np.asarray(data)
    # model.fit(data, to_categorical(np.asarray(labels), num_classes=len(countries)), epochs=10, batch_size=32)

    preds = model.predict(preprocess_input(data))
    results = decode_predictions(preds, top=5)[0]
    for result in results:
        print(result)

#model.save('cosplayer-country.h5')
