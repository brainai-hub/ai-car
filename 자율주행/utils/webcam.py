import cv2
import numpy as np

def Crop(frame):
    width = frame.shape[1]
    height = frame.shape[0]
    y1 = int(height - (height * .2))
    y2 = int(height - (height * .0))
    cropFrame = frame[y1:y2, :]  
    return cropFrame, y1, y2, width, height