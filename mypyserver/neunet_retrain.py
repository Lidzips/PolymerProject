from tensorflow import keras
import tensorflow as tf
import os
import sys
from PIL import Image
import numpy as np
import cv2 as cv

def retrain(arc_batch_size, arc_epochs, layers):
    train_data = './neunet/dataset'
    layer_count = len(layers) # each element is a unique hidden layer with x = layer_info[element] neurons

    x_train_src = train_data + '/train/images'
    y_train_src = train_data + '/train/labels.txt'
    x_test_src = train_data + '/test/images'
    y_test_src = train_data + '/test/labels.txt'

    filelist = os.listdir(x_train_src)
    x_train = np.array([np.array(Image.open(x_train_src + '/' + fname)) for fname in filelist])
    y_train = np.loadtxt(y_train_src, dtype=int)
    filelist = os.listdir(x_test_src)
    x_test = np.array([np.array(Image.open(x_train_src + '/' + fname)) for fname in filelist])
    y_test = np.loadtxt(y_test_src, dtype=int)

    x_train = x_train.reshape(x_train.shape[0], 784)
    x_train = x_train / 255
    y_train = keras.utils.to_categorical(y_train, 4)
    x_test = x_test.reshape(x_test.shape[0], 784)
    x_test = x_test / 255
    y_test = keras.utils.to_categorical(y_test, 4)

    model = keras.models.Sequential()
    input = 784
    for i in range (0, layer_count - 1):
      model.add(keras.layers.Dense(layers[i], input_dim=input, activation="relu"))
      input = layers[i]
    model.add(keras.layers.Dense(4, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])

    model.fit(x_train, y_train, batch_size=arc_batch_size, epochs=arc_epochs, verbose=1)

    model.save('/neunet/saved_model')
    
    #return fitness