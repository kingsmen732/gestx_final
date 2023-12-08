from keras.models import load_model
import time
import threading
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pyaudio
import wave
import speech_recognition as sr

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import keras
import numpy as np
import librosa
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary



from sklearn.preprocessing import LabelEncoder


cred = credentials.Certificate(r"C:\Users\Pugazh Mukilan\Desktop\ECS project python coding\Final\ecs-project-3a8d3-firebase-adminsdk-c3uk9-ac8d5d1081.json")

firebase_admin.initialize_app(cred)


total_time=45;
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier =load_model('model.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']
Emotion_list=[]
complete_emotion_list=[]
Emotion_percentage={}
Emotion_list_percentage=[]
whole_emotion=[]
percentage_5sec={}
def openwebsite():
    driver = webdriver.Firefox()
    # Open the login page
    driver.get('file:///C:/Users/Pugazh%20Mukilan/Desktop/ECS%20project%20python%20coding/ecs-gestx-2/index.html')
    button = driver.find_element(By.ID,'start_btn')
    button.click()
    time.sleep(1)
    button1=driver.find_element(By.ID,"start-button")
    button1.click()
    
    
openwebsite()    
    

        

def store(l,document):
    
   


    # Access Firestore
    db = firestore.client()

    # Example: Add a document to a collection
    data = {
        "per": l  # Replace this with your actual array data
    }
    db.collection("emotion").document(document).set(data)
    """if (document=="Percentages"):
        storemaxemotion(l)"""
    
    Emotion_list.clear()
    Emotion_list_percentage.clear()
"""def storemaxemotion(a):
    print("===============================",a)
    db = firestore.client()
    max_emotion = max(set(a), key=a.count)
    store(max_emotion,"maxemotion")
    data = {
        "per": a  # Replace this with your actual array data
    }
    db.collection("emotion").document("maxemotion").set(data)"""
    

def store5sec(l):
    db = firestore.client()
    for i in range(len(l)):
        percentage_5sec[emotion_labels[i]] =l[i]
    data = {
        "per": percentage_5sec  # Replace this with your actual array data
    }
    db.collection("emotion").document("Percentages").set(data)
    percentage_5sec.clear()
    Emotion_list.clear()
    Emotion_list_percentage.clear()
          
       
   
    
store(None, "voice")

p = pyaudio.PyAudio()
frames = []
stop = True
def startvoice():
    print("inside the voicestart")
    
    stream = p.open(format=pyaudio.paInt16,channels=2,rate=44100, input=True, frames_per_buffer=1024)

    print("**** recording")

    

    for i in range(0, int(44100 / 1024 * total_time)):
        data = stream.read(1024)
        frames.append(data)

    print("**** done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

   

class livePredictions:
    
        """
        Main class of the application.
        """

        def __init__(self, path, file):
            """
            Init method is used to initialize the main parameters.
            """
            self.path = path
            self.file = file

        def load_model(self):
            """
            Method to load the chosen model.
            :param path: path to your h5 model.
            :return: summary of the model with the .summary() function.
            """
            self.loaded_model = keras.models.load_model(self.path)
            return self.loaded_model.summary()
        
        def makepredictions(self):
            """
            Method to process the files and create your features.
            """
            data, sampling_rate = librosa.load(self.file)
            mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
            x = np.expand_dims(mfccs, axis=1)
            x = np.expand_dims(x, axis=0)
            predictions = self.loaded_model.predict(x)
            predicted_class = np.argmax(predictions)
            emotion = self.convertclasstoemotion(predicted_class)
            print("Prediction is", emotion)
            return emotion

        @staticmethod
        def convertclasstoemotion(pred):
            """
            Method to convert the predictions (int) into human readable strings.
            """
            
            label_conversion = {'0': 'neutral',
                                '1': 'calm',
                                '2': 'happy',
                                '3': 'sad',
                                '4': 'angry',
                                '5': 'fearful',
                                '6': 'disgust',
                                '7': 'surprised'}
            #for key, value in label_conversion.items():
                #if int(key) == pred:
                    #label = value
            return label_conversion.get(str(pred), 'unknown')
def storecompletepercentage(l):
    db = firestore.client()
    for i in range(6):
        Emotion_percentage[emotion_labels[i]]=l[i]
        
    print("================================")
    print(Emotion_percentage)
    data = {
         # Replace this with your actual array data
        "per":Emotion_percentage
    }
    db.collection("emotion").document("complete_emotion_percentage").set(data)
    Emotion_percentage.clear
        
#this function store the list in the firebase



#this will give the percentage of each emition in the list

def get_percentage(emotionlist,option):
    #find the unique  elements from emotion list
    if (option ==1):
        doc="Percentages"
    else:
        doc="complete_emotion_percentage"
    
    #finding the percentage of each emotion in the list
    for i in emotion_labels:
        try:
            percentage =((emotionlist.count(i)/len(emotionlist))*100)
            
            
            #adding the percentage element in the Emotion percentage dictionary
            Emotion_percentage[i]=percentage
            Emotion_list_percentage.append(percentage)
        except:
            print("nothing")
        
        
    #printing the percentage
    #print(Emotion_percentage)
    if (option==1):
    
        store5sec(Emotion_list_percentage)
    else:
        storecompletepercentage(Emotion_list_percentage)
    
    
def voiceresults():
    wf = wave.open('output.wav', 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()

    harvard = sr.AudioFile('output.wav')
    r = sr.Recognizer()
    with harvard as source:
        audio = r.record(source)
        text = r.recognize_google(audio)
    try:
        print("You said: " +text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        

    data, sampling_rate = librosa.load('output.wav')
    print("loaded the voice")


    
    
        
            
        

    # Here you can replace path and file with the path of your model and of the file 
    #from the RAVDESS dataset you want to use for the prediction,
    # Below, I have used a neutral file: the prediction made is neutral.

    pred = livePredictions(path='SER_model.h5',file='output.wav')
    pred.load_model()
    result = pred.makepredictions()
    # Save the result in the 'result' variable
    print("Result:", result)
    store(result, "voice")
    print("Done")
def scheduled_function(interval):
    while stop:
        #print("scheuled function")
        #get_percentage(Emotion_list,1)
        
        get_percentage(Emotion_list,1)
        
        time.sleep(interval)
        
        
interval_seconds = 5
voicethread = threading.Thread(target=startvoice)
voicethread.daemon = True  # Daemonize the thread so it automatically exits when the main program exits
voicethread.start()
print(" voice thread started")

# Create a thread that will run the scheduled_function
thread = threading.Thread(target=scheduled_function, args=(interval_seconds,))
thread.daemon = True  # Daemonize the thread so it automatically exits when the main program exits
thread.start()
print("thread started")
'''webthread = threading.Thread(target=openwebsite)
webthread.daemon = True  # Daemonize the thread so it automatically exits when the main program exits
webthread.start()
print("website thread started")'''



cap = cv2.VideoCapture(0)
start_time = time.time()
  # Set the duration in seconds
elapsed_time = time.time() - start_time
while elapsed_time<total_time:
    elapsed_time = time.time() - start_time

    #if elapsed_time >= total_time:
     #   print("Time limit reached. Stopping the video capture.")
        
     #   break
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    try:
        Emotion_list.append(emotion_labels[prediction.argmax()])
        complete_emotion_list.append(emotion_labels[prediction.argmax()])
    except:
        print("passing by:)")
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        get_percentage(complete_emotion_list,2)
        store(complete_emotion_list,"Completedetail")
        stop=False
        print("percentage cal thread is stopped")
        print("getting your voice results")
        voiceresults()
        
        
        break
get_percentage(complete_emotion_list,2)
store(complete_emotion_list,"Completedetail")

stop=False
print("percentage cal thread is stopped")
print("getting your voice results")
voiceresults()


cap.release()
cv2.destroyAllWindows()