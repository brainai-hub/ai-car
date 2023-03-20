from tensorflow.keras.models import model_from_json

def GetLabels():
    # 레이블 불러오기
    labels = []
    file = open("model/labels.txt", "r")
    for x in file:
      labels.append(x.rstrip('\n'))

    print('labels = ', labels)
    print()
    file.close()

    return labels


def loadModel():
    # 모델 불러오기
    with open('./model/model.json', 'r') as file_model:
        model_desc = file_model.read()
        model = model_from_json(model_desc)
    model.load_weights('./model/weights.h5')

    return model
