import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js';
import { doc, getDoc, getFirestore } from 'https://www.gstatic.com/firebasejs/10.6.0/firebase-firestore.js';

const firebaseConfig = {
    apiKey: "AIzaSyDyOXjT2mYo3g72q1NLSREZg9HX7bzDsCI",
    authDomain: "ecs-project-3a8d3.firebaseapp.com",
    projectId: "ecs-project-3a8d3",
    storageBucket: "ecs-project-3a8d3.appspot.com",
    messagingSenderId: "587479702485",
    appId: "1:587479702485:web:ccc1b75533437d281a7b5c",
    measurementId: "G-NTJ6F80SY5"
};

// Initialize Firebase app
const firebaseApp = initializeApp(firebaseConfig);

// Initialize Firestore
const db = getFirestore(firebaseApp);

document.addEventListener('DOMContentLoaded', async () => {
    console.log("dom contents loaded");
    const table = document.getElementById('dataTable');
    const maxEmotionContainer = document.getElementById('maxEmotionContainer');
    const maxEmotionElement = document.getElementById('maxEmotion');
    const singleEmotionContainer = document.getElementById('toneContainer');
    const singleEmotionElement = document.getElementById('tone');
    
    const documentIdAllEmotions = 'complete_emotion_percentage';
    const documentIdSingleEmotion = 'voice';

    try {
        // Retrieve data for all emotions
        console.log("trying to get all emotions");
        const docRefAllEmotions = doc(db, 'emotion', documentIdAllEmotions);
        const docSnapshotAllEmotions = await getDoc(docRefAllEmotions);

        if (docSnapshotAllEmotions.exists()) {
            console.log("documents for all emotion exist");
            const dataMap = docSnapshotAllEmotions.data().per;

            let maxEmotion = '';
            let maxValue = -Infinity;

            Object.entries(dataMap).forEach(([emotion, value]) => {
                var row = table.insertRow(-1);
                var emotionCell = row.insertCell(0);
                var valueCell = row.insertCell(1);

                emotionCell.innerHTML = emotion;
                valueCell.innerHTML = value;

                if (value > maxValue) {
                    maxValue = value;
                    maxEmotion = emotion;
                }
            });

            maxEmotionElement.textContent = maxEmotion;
        } else {
            console.log('No such document for all emotions!');
            table.innerHTML = '<tr><td colspan="2">No data found</td></tr>';
        }

        // Retrieve data for a single emotion
        console.log("trying to get docs for single emotions");
        const docRefSingleEmotion = doc(db, 'emotion', documentIdSingleEmotion);
        const docSnapshotSingleEmotion = await getDoc(docRefSingleEmotion);

        if (docSnapshotSingleEmotion.exists()) {
            console.log("docs for single emotion exists");
            const singleEmotionData = docSnapshotSingleEmotion.data().per;

            if (singleEmotionContainer !== null && singleEmotionElement !== null) {
                if (singleEmotionData.per !== null) {
                    singleEmotionElement.textContent = singleEmotionData;
                } else {
                    singleEmotionContainer.textContent = 'No emotion data available';
                }
            }
        } else {
            console.log('No such document for single emotion!');
            if (singleEmotionContainer !== null) {
                singleEmotionContainer.textContent = 'No data found for single emotion';
            }
        }

    } catch (error) {
        console.error('Error getting documents: ', error);
        if (table !== null) {
            table.innerHTML = '<tr><td colspan="2">Error retrieving data</td></tr>';
        }
        if (singleEmotionContainer !== null) {
            singleEmotionContainer.textContent = 'Error retrieving data for single emotion';
        }
    }
});