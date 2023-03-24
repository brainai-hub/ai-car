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

class Text_Model:
    

    def __init__(self):
        print(" -- Models -- ")
        self.horizontal_model, self.horizontal_output = self.load_text_model('horizontal-text-detection-0001')
        self.recognition_model, self.recognition_output = self.load_text_model('text-recognition-0014')
        
        self.characters = "#1234567890abcdefghijklmnopqrstuvwxyz"
        self.conf_1 = .4
        self.conf_2 = .8

    def load_text_model(self, model_name):
        print("\n Loading:", model_name)
        model =  "model/" + model_name + ".xml"
    
        ie = Core()
        model = ie.read_model(model=model)
        compiled_model = ie.compile_model(model=model, device_name="CPU")
        input_layer = model.input(0)
        output_layer = compiled_model.output(0)

        try:
            print("Input layer shape:", input_layer.shape)
            print("Output layer shape:", output_layer.shape)
            
        except: 
            print("Cannot print out layer shapes")
        
        return compiled_model,  output_layer
    
    def infer_model_1(self, frame):#Run the model and analyze predictions
    
        resized_frame = cv2.resize(src=frame, dsize=(704, 704)) 
        transposed_frame = resized_frame.transpose(2, 0, 1)
        input_frame = np.expand_dims(transposed_frame, 0)
   
        # ----------- run model ------------ #
        self.predictions_1 = self.horizontal_model([input_frame])[self.horizontal_output]
    
        text_boxes = [] 
        for i in range(len(self.predictions_1)):
            
            if self.predictions_1[i][4]> self.conf_1:
                
                (xmin, ymin, xmax, ymax, _)  = self.predictions_1[i].astype("int")
                conf = self.predictions_1[i][4]
                
                h, w, c = np.shape(frame)
                xmin = int(xmin/704*w) #normalize locations
                xmax = int(xmax/704*w)
                ymin = int(ymin/704*h)
                ymax = int(ymax/704*h)
            
                box = (xmin, xmax, ymin, ymax, conf)
                text_boxes.append(box)
     
        return text_boxes
   
    def infer_model_2(self, frame, output_1): #Run the model and analyze predictions
        
        predictions_2 = []
        words = [] 
        # ------------------ Pre-process -------------------#
        for i in range(len(output_1)):
         
            model_input = [] 
            xmin, xmax, ymin, ymax, conf = output_1[i]
            crop_frame = frame[ymin:ymax, xmin:xmax]
            crop_gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)
            (n, c, h, w) = (1,1,32,128)
            input_image = np.ndarray(shape=(n, c, h, w))

            if crop_gray.shape[:-1] != (h, w):
                crop_gray = cv2.resize(crop_gray, (w, h))
            
            input_image[0] = crop_gray
        
            # ------------------ Run Model ------------------- #
            output_2 = self.recognition_model([input_image])[self.recognition_output]
            
            word = ''
            for i in output_2:
                letter_index = np.argmax(i)
                letter = self.characters[letter_index]
                if letter != '#':
                    word += letter
            words.append(word)

        return words
    

    def predictions(self, frame): 
        
        output_1 = self.infer_model_1(frame)
        output_2 = self.infer_model_2(frame, output_1)
        
        return output_1, output_2

    def draw(self, output_1, output_2, frame):
        
        for i in range(len(output_1)):

            xmin, xmax, ymin, ymax, conf = output_1[i]
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)
                       
            text = output_2[i]
            cv2.putText(frame,text,(xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)     