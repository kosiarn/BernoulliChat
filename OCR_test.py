import pytesseract
import cv2
import numpy as np
from PIL import Image
import requests


def get_string(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("removed_noise.png", img)
    cv2.imwrite(img_path, img)   

    result = pytesseract.image_to_string(Image.open(img_path), lang="pol")
    return result

img_path = 'tekst.jpg'
pytesseract.pytesseract.tesseract_cmd = r'C:/Users/pc/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
print(get_string(img_path))

