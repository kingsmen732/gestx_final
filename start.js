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

  // Get a Firestore reference
  const firestore = getFirestore(firebaseApp);

  let [seconds, minutes, hours] = [45, 0, 0];
  let timeref = document.querySelector(".timer-display");
  let maxEmotionDisplay = document.getElementById("max-emotion");
// Update this function to handle different emotions and update every 5 seconds
function updateMaxEmotionContent(maxEmotion) {
    // Initial update
    updateContent(maxEmotion);
  
    // Update content every 5 seconds
   setInterval(() => {
      updateContent(maxEmotion);
    }, 8000);
  }
  
  // New function to handle different emotions
  function updateContent(maxEmotion) {
    let content = "";
  
    // Switch statement to handle different emotions
    switch (maxEmotion.key) {
        case "Happy":
            content = "You seem happy! Keep smiling!";
            break;
        case "Sad":
            content = "Cheer up! get it better ";
            break;
        case "Neutral":
            content = "Everything is going good ";
            break;
        case "Angry":
            content = "be calm";
            break;
        
        
          
        // Add more cases for other emotions as needed
    }
  
    // Display the content on the website
    document.getElementById("emotion-content").innerHTML = `<p>${content}</p>`;

    // Set a timeout to clear the content after 2 seconds
    /*setTimeout(() => {
        document.getElementById("emotion-content").innerHTML = "";
    }, 2000);*/
}

  
  // Update this function to handle different emotions
  async function updateMaxEmotion() {
    try {
      // Fetch emotional data from Firestore
      const docRef = doc(firestore, 'emotion', 'Percentages');
      const docSnap = await getDoc(docRef);
      const emotionsData = docSnap.data().per; // Adjust this based on your actual field name
  
      // Find the key-value pair with the maximum value
      let maxEmotion = { key: null, value: -Infinity };
      for (const [key, value] of Object.entries(emotionsData)) {
        if (value > maxEmotion.value) {
          maxEmotion = { key, value };
        }
      }
  
      console.log("Emotion with Maximum Value:", maxEmotion);
  
      // Display the emotion with the maximum value on the website
      maxEmotionDisplay.innerHTML = `<p>Emotion with Maximum Value: ${maxEmotion.key} `;
  
      // Update content based on max emotion
      updateMaxEmotionContent(maxEmotion);
    } catch (error) {
      console.error("Error fetching data from Firestore:", error);
    }
  }
  
  // Function to update max emotion every 5 seconds
  function updateMaxEmotionPeriodically() {
    setInterval(() => {
      updateMaxEmotion();
    }, 6000);
  }
  
  // Event listener for the "Start" button
  document.getElementById("start-button").addEventListener("click", () => {
    // Initial update
    updateMaxEmotion();
  
    // Start updating periodically
    updateMaxEmotionPeriodically();
  
    // Start the timer
    setInterval(displayTimer, 1000);
  });
  
  // Function to display the timer
  function displayTimer() {
    seconds -= 1;
    if (seconds === 0) {
      [seconds, minutes, hours] = [0, 0, 0];
      timeref.innerHTML = "00 : 00 : 00";
      redirect();
    }
    let h = hours < 10 ? "0" + hours : hours;
    let m = minutes < 10 ? "0" + minutes : minutes;
    let s = seconds < 10 ? "0" + seconds : seconds;
  
    timeref.innerHTML = `${h} : ${m} : ${s}`;
  }
  
  // Function to redirect
  function redirect() {
    setTimeout(myURL, 1000); // Adjust the timeout as needed
  }
  
  // Function to redirect to result.html
  function myURL() {
    document.location.href = 'result.html';
  }