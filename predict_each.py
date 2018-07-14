#!/usr/bin/env python

from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

(_, model_file, test_dir) = sys.argv
model = load_model(model_file)
test_datagen = ImageDataGenerator(rescale = 1.0/255)
test_base = 'predict_each'
directories = ['brazil', 'china', 'japan']

for test_type in directories:
    for subdir_key in directories:
        subdir = os.path.join(test_base, subdir_key)
        if os.path.lexists(subdir):
            if os.path.islink(subdir):
                os.unlink(subdir)
            else:
                os.rmdir(subdir)
        if subdir_key == test_type:
            fullpath = os.path.realpath(os.path.join(test_dir, test_type))
            os.symlink(fullpath, subdir)
        else:
            os.mkdir(subdir)

    test_generator = test_datagen.flow_from_directory(
        'predict_each',
        batch_size = 16,
        target_size = (224, 224),
        class_mode = 'categorical'
    )

    score = model.evaluate_generator(test_generator)
    print(test_type, score)
