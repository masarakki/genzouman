#!/usr/bin/env python

from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator
from PIL import Image
import numpy as np
import sys

args = sys.argv
input_dir = args[1]
output_dir = args[2]

IMAGE_SIZE = 224
BATCH_SIZE = 1
model = load_model('./face_or_not.h5')
predict_datagen = ImageDataGenerator(rescale = 1.0/255)

label_mapping = ['brazil', 'china', 'japan']
predict_generator = predict_datagen.flow_from_directory(
    input_dir,
    target_size = (IMAGE_SIZE, IMAGE_SIZE),
    batch_size = BATCH_SIZE,
    class_mode = 'sparse',
    shuffle = True
)
result = model.predict_generator(predict_generator, verbose = 1)
predict_generator.reset()

for index, predict in enumerate(result):
    if predict[0] > 0.8:
        (image, label) = predict_generator[index]
        label_name = label_mapping[label[0]]
        image = image[0]
        filename = '%s/%s/%05d.jpg' % (output_dir, label_name, index)
        image = image * 255
        image = image.astype('uint8')
        pilImg = Image.fromarray(image)
        pilImg.save(filename)
