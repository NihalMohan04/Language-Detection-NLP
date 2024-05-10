// script.js

// Initialize variables
let recorder;
let audioChunks = [];
let recordedText = '';

// Function to start recording audio
async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };
    recorder.start();
    document.getElementById('start-recording').disabled = true;
    document.getElementById('stop-recording').disabled = false;
}

// Function to stop recording audio
function stopRecording() {
    recorder.stop();
    document.getElementById('start-recording').disabled = false;
    document.getElementById('stop-recording').disabled = true;
    document.getElementById('submit-audio').disabled = false;
}

// Function to submit recorded audio
async function submitAudio() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.wav'); // Key 'audio' is used here

    // Display loading spinner
    document.getElementById('loading').style.display = 'block';

    // Fetch API to send audio data to server for language detection
    const response = await fetch('/detect_language', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();

    // Hide loading spinner
    document.getElementById('loading').style.display = 'none';

    // Display result
    document.getElementById('result-audio').innerText = "The language is in " + data.language;

    // Display recorded text
    document.getElementById('recorded-text').innerText = "Recorded Text: " + recordedText;
}

// Function to detect language from text input
function detectLanguageFromText() {
    var text = document.getElementById('text').value;
    fetch('/detect_language', {
        method: 'POST',
        body: new 
