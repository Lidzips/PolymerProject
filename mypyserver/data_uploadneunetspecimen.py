from PIL import Image
from numpy import asarray
import cv2 as cv
import base64
from io import BytesIO

def uploadspecimen(specimen, label):
    img = Image.open(BytesIO(base64.decodebytes(specimen))).convert('L')
    img = img.resize((28,28))
    img = asarray(img)
    
    #count = sum(1 for line in open('/neunet/dataset/train/labels.txt'))
    
    with open('./neunet/dataset/train/labels.txt', 'r') as fp:
        count = len(fp.readlines())
    
    cv.imwrite('./neunet/dataset/train/images/' + str(count + 1) + '.png', img)
    with open('./neunet/dataset/train/labels.txt', 'a') as f:
        f.write(label + '\n')