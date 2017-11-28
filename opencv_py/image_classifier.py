from __future__ import print_function

# adapted from: https://www.bonaccorso.eu/2016/08/06/cifar-10-image-classification-with-keras-convnet/

import glob
import os
import shutil

import numpy as np
import argparse

# import cv2

# from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D
from keras.optimizers import Adam
from keras.layers.pooling import MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing import image

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=1000)
parser.add_argument('--epochs', type=int, default=100)
parser.add_argument('--batch', type=int, default=10, help='Batch size for training')
parser.add_argument('--gray', action='store_true')
parser.add_argument('--retrain', action='store_true', help='Retrain model even when loaded')
parser.add_argument('--generator', '-g', action='store_true')
parser.add_argument('--rename', '-w', action='store_true', help='Move files to predicted classes')
parser.add_argument('--threshold', '-t', type=float, default=0.8)
parser.add_argument('--save', '-o', type=str)
parser.add_argument('--load', '-i', type=str)
args = parser.parse_args()


size = (128, 128)

# For reproducibility
np.random.seed(args.seed)

# Fixed classes - subfolders of CWD
classes = sorted(d.replace(os.path.sep, '') for d in glob.glob('*/'))
num_classes = len(classes)


def get_training_set():
    # Load the dataset
    X = []
    Y = []

    for index, d in enumerate(classes):
        for image_filename in glob.glob(d+'/*.*'):
            img = image.img_to_array(image.load_img(image_filename, target_size=size, grayscale=args.gray))
            # import code; code.interact(local=locals())
            # cv2.imshow('train', img)
            # cv2.waitKey(0)
            img = img.astype(np.float32) / 256.0 - 0.5
            Y.append(index)
            X.append(img)

    X = np.asarray(X)
    return X, Y


def create_network():
    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=size + (1 if args.gray else 3,)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    # Compile the model
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=0.00001, decay=1e-6)
                  , metrics=['accuracy']
                  )

    return model


def get_training_generator():
    generator = image.ImageDataGenerator(
            rescale=1 / 255.,
            # rotation_range=180.0,
            # width_shift_range=0.05,
            # height_shift_range=0.05,
            # zoom_range=0.1,
            horizontal_flip=True,
            vertical_flip=True,
            preprocessing_function=lambda x: x - 127.5
        ).flow_from_directory(
            '.',
            target_size=size,
            batch_size=args.batch,
            color_mode='grayscale' if args.gray else 'rgb'
        )
    return generator


if __name__ == '__main__':
    model = create_network()

    if args.load:
        model.load_weights(args.load)

    if not args.load or args.retrain:
        if args.generator:
            generator = get_training_generator()
        else:
            X, Y = get_training_set()

        # Train the model

        if args.generator:
            model.fit_generator(generator, steps_per_epoch=args.batch, epochs=args.epochs)
        else:
            model.fit(
                X, to_categorical(Y), batch_size=args.batch, shuffle=True, epochs=args.epochs
                # , callbacks=[EarlyStopping(min_delta=0.001, patience=3)]
            )

    if args.save:
        model.save(args.save, overwrite=True)

    to_classify = glob.glob('*.*')

    print('Done, loading images...')
    X_test = np.asarray([
        image.img_to_array(image.load_img(image_filename, target_size=size, grayscale=args.gray)).astype(np.float32) / 256.0 - 0.5
        for image_filename in to_classify if os.path.splitext(image_filename.lower())[1] in ('.png', '.jpg', '.bmp', '.gif')
    ])


    print('Classifying...', classes)
    Y_test = model.predict(X_test)

    print('Done.')
    for preds, filename in zip(Y_test, to_classify):
        print(preds, filename, classes[np.argmax(preds)])
        if args.rename:
            idx = np.argmax(preds)
            class_ = classes[idx]
            folder = ('pred_' if preds[idx] > args.threshold else 'maybe_') + class_
            os.makedirs(folder, exist_ok=True)
            os.rename(filename, os.path.join(folder, filename))
