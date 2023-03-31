from tensorflow import keras
from PIL import Image
from numpy import asarray
import numpy as np
import cv2 as cv
import base64
from io import BytesIO

def predict(specimen):
    model_src = '/neunet/saved_model'

    model = keras.models.load_model(model_src)

    img = Image.open(BytesIO(base64.decodebytes(specimen))).convert('L')
    img = img.resize((28,28))
    img = asarray(img)
    res = cv.resize(img, dsize=(28, 28), interpolation=cv.INTER_CUBIC)
    res = res.reshape(1,784)
    res = res / 255

    predarray = model.predict(res).ravel()
    
    prediction = str(np.argmax(predarray))
    
    return prediction