import cv2
import numpy as np
from tensorflow.keras.models import load_model


model = load_model("model/emotion_model.h5", compile=False)


emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def detect_emotion(img_path):
   
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        
        face_img = gray[y:y+h, x:x+w]
        resized = cv2.resize(face_img, (64, 64)) / 255.0
        reshaped = np.reshape(resized, (1, 64, 64, 1))

       
        result = model.predict(reshaped, verbose=0)
        return emotion_labels[np.argmax(result)]

    
    return "Neutral"
