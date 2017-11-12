from __future__ import print_function

# adapted from: https://www.bonaccorso.eu/2016/08/06/cifar-10-image-classification-with-keras-convnet/

import glob
import os
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
parser.add_argument('--gray', action='store_true')
args = parser.parse_args()


size = (128, 128)

# For reproducibility
np.random.seed(args.seed)

if __name__ == '__main__':
    # Load the dataset
    classes = sorted(d.replace(os.path.sep, '') for d in glob.glob('*/'))
    num_classes = len(classes)
    X = []
    Y = []

    for index, d in enumerate(classes):
        for image_filename in glob.glob(d+'/*.png'):
            img = image.img_to_array(image.load_img(image_filename, target_size=size, grayscale=args.gray))
            # import code; code.interact(local=locals())
            # cv2.imshow('train', img)
            # cv2.waitKey(0)
            img = img.astype(np.float32) / 256.0 - 0.5
            Y.append(index)
            X.append(img)

    X = np.asarray(X)
    print(Y)

    # Create the model
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

    # Train the model
    model.fit(X, to_categorical(Y),
              batch_size=10,
              shuffle=True,
              epochs=args.epochs
              # , callbacks=[EarlyStopping(min_delta=0.001, patience=3)]
              )

    to_classify = glob.glob('*.png')

    print('Training done, loading images...')
    X_test = np.asarray([
        image.img_to_array(image.load_img(image_filename, target_size=size)).astype(np.float32) / 256.0 - 0.5
        for image_filename in to_classify
    ])

    print('Classifying...')
    Y_test = model.predict(X_test)

    print('Done.')
    for preds, filename in zip(Y_test, to_classify):
        print(preds, filename)
        if preds[1] > preds[0]:
            print('-'*50)
