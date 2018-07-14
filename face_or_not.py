#!/usr/bin/env python

from keras.models import Sequential, Model
from keras.layers import Input, Dense, Flatten, Dropout, GlobalAveragePooling2D
from keras.applications.vgg16 import VGG16
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import CSVLogger
import sys


IMAGE_SIZE = 224
BATCH_SIZE = 8 #32
EPOCH_NUM = 10

category_num = 2

train_datagen = ImageDataGenerator(
    rescale = 1.0 / 255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True)

validation_datagen = ImageDataGenerator(rescale = 1.0 / 255)

def train(train_dir):
    print("start train:", train_dir)
    filename = train_dir

    base_model = VGG16(weights = 'imagenet', include_top = False,
                       input_tensor = Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3)))

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    prediction = Dense(category_num, activation='softmax')(x)
    model = Model(input = base_model.input, output = prediction)

    for layer in base_model.layers[:15]:
        layer.trainable = False

    model.compile(optimizer = SGD(lr = 0.0001, momentum = 0.9),
                  loss = 'categorical_crossentropy',
                  metrics = ['accuracy'])

#    model.summary()

    with open(filename + '.json', 'w') as f:
        f.write(model.to_json())


    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size = (IMAGE_SIZE, IMAGE_SIZE),
        batch_size = BATCH_SIZE,
        class_mode = 'categorical',
        shuffle = True
    )

    model.fit_generator(train_generator,
                        epochs = EPOCH_NUM,
                        callbacks = [CSVLogger(filename + '.csv')])

    model.save(filename + '.h5')

train('face_or_not')
