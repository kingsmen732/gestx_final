#this is the sample alogrithm of how thw percentage of the  emotion is going to be calculated

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

Emotion_list=["happy","happy","confused","fear","neutral","happy","fear"]
Emotion_percentage={}
Emotion_list_percentage=[]


#this function store the list in the firebase 
def store(l):
    cred = credentials.Certificate("C:\\Users\\Pugazh Mukilan\\Desktop\\ECS project python coding\\finalize code base\\ecs-project-3a8d3-firebase-adminsdk-c3uk9-14c11f78e2.json")

    firebase_admin.initialize_app(cred)


    # Access Firestore
    db = firestore.client()

    # Example: Add a document to a collection
    data = {
        "per": l  # Replace this with your actual array data
    }
    db.collection("emotion").document("percentage").set(data)

#this will give the percentage of each emition in the list

def get_percentage(emotionlist):
    #find the unique  elements from emotion list
    set_list=set(emotionlist)
    
    #finding the percentage of each emotion in the list
    for i in set_list:
        percentage =((emotionlist.count(i)/len(emotionlist))*100)
        
        
        #adding the percentage element in the Emotion percentage dictionary
        Emotion_percentage[i]=percentage
        Emotion_list_percentage.append(percentage)
        
        
    #printing the percentage
    print(Emotion_percentage)
    print(Emotion_list_percentage)
    store(Emotion_list_percentage)
    
get_percentage(Emotion_list)



