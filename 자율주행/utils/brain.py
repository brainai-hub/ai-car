from openvino.runtime import Core
from tensorflow.keras.models import model_from_json
import cv2
import numpy as np

class CNN_Model:
    def __init__(self):
        pass  
    def GetLabels(self): 
        # 레이블 불러오기
        labels = []
        file = open("model/labels.txt", "r")
        for x in file:
          labels.append(x.rstrip('\n'))

        print('labels = ', labels)
        print()
        file.close()
        return labels 
    def load_CNN_Model(self): 
        print("Loading Model")
        with open('./model/model.json', 'r') as file_model:        
            model_desc = file_model.read()
            model = model_from_json(model_desc)
        model.load_weights('./model/weights.h5')
        return model 