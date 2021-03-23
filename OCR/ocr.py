"""
Import the necessary packages
"""
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import argparse
from textblob import TextBlob
import os
from pytesseract import image_to_string
import numpy as np
import io
import urllib.request
""" 
Setting path for tesseract
"""
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'

def ocr():
        # Downloading image from firestore
        file_name = "test_image"
        url = "https://firebasestorage.googleapis.com/v0/b/abstracto-db.appspot.com/o/7.jpg?alt=media&token=1814fdb8-869c-4ec5-892a-7bb7e781868b"
        file_path = "E:"
        full_path = file_path + file_name + '.jpg'
        urllib.request.urlretrieve(url, full_path)
        
        img = cv2.imread("test_image.jpg")

        # Configurations for OCR
        config = ('-l eng --oem 1 --psm 3')
        """
        Preprocessing of image
	"""
        # Greyscaling
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Rescaling
        grey = cv2.resize(grey, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        # Thresholding
        grey = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        # Blurring
        grey = cv2.medianBlur(grey, 3)
        # Dilation and erosion
        kernel = np.ones((1, 1), np.uint8)
        grey = cv2.dilate(grey, kernel, iterations=1)
        grey = cv2.erode(grey, kernel, iterations=1)
        """
	Feeding image to tesseract OCR
	"""
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, grey)
        text = pytesseract.image_to_string(Image.open(filename), config=config)
        # print(filename)
        os.remove(filename)
        # Correcting spellings using TextBlob
        corrected_text = TextBlob(text)
        print(str(corrected_text.correct()))


ocr()	
	
