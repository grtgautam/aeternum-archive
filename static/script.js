let mediaRecorder;
let recordedChunks = [];
let stream;
let timerInterval;
const MAX_TIME = 600; // 10 minutes in seconds

// Tab Switching
function switchTab(type) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.input-section').forEach(s => s.classList.remove('active'));

    // Find the button with the matching onclick handler (naive check) or just by index
    // Better: Query buttons by text content or logic.
    // Let's assume order: 0=Video, 1=Audio, 2=Text
    const map = { 'video': 0, 'audio': 1, 'text': 2 };
    document.querySelectorAll('.tab-btn')[map[type]].classList.add('active');
    document.getElementById(type + '-section').classList.add('active');

    // Stop constraints if switching away from recording
    if (type === 'text') {
        stopStream();
    }
}

// Date Constraint (Future only)
const datePicker = document.getElementById('date-picker');
if (datePicker) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    datePicker.min = tomorrow.toISOString().split('T')[0];
}

// VIDEO RECORDING
const videoPreview = document.getElementById('video-preview');
const startVideoBtn = document.getElementById('start-video');
const stopVideoBtn = document.getElementById('stop-video');
const recIndicator = document.getElementById('rec-indicator');
const videoTimer = document.getElementById('timer');

startVideoBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        videoPreview.srcObject = stream;

        startRecording(stream, videoTimer);

        startVideoBtn.disabled = true;
        stopVideoBtn.disabled = false;
        recIndicator.style.display = 'block';
    } catch (err) {
        alert("Could not access camera/microphone: " + err);
    }
});

stopVideoBtn.addEventListener('click', () => {
    stopRecording();
    stopStream();
    startVideoBtn.disabled = false;
    stopVideoBtn.disabled = true;
    recIndicator.style.display = 'none';
    videoTimer.innerText = "Recorded!";
});

// AUDIO RECORDING
const startAudioBtn = document.getElementById('start-audio');
const stopAudioBtn = document.getElementById('stop-audio');
const audioTimer = document.getElementById('audio-timer');

startAudioBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        startRecording(stream, audioTimer);
        startAudioBtn.disabled = true;
        stopAudioBtn.disabled = false;
    } catch (err) {
        alert("Could not access microphone: " + err);
    }
});

stopAudioBtn.addEventListener('click', () => {
    stopRecording();
    stopStream();
    startAudioBtn.disabled = false;
    stopAudioBtn.disabled = true;
    audioTimer.innerText = "Recorded!";
});

// SHARED RECORDING LOGIC
function startRecording(streamToRecord, timerElement) {
    recordedChunks = [];
    // Mimetype Selection
    let options = { mimeType: 'video/webm;codecs=vp9' };
    if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        options = { mimeType: 'video/webm' };
        if (!MediaRecorder.isTypeSupported(options.mimeType)) {
            options = { mimeType: '' }; // Let browser pick
        }
    }

    mediaRecorder = new MediaRecorder(streamToRecord, options);

    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            recordedChunks.push(event.data);
        }
    };

    mediaRecorder.start();

    let seconds = 0;
    timerInterval = setInterval(() => {
        seconds++;
        const m = Math.floor(seconds / 60).toString().padStart(2, '0');
        const s = (seconds % 60).toString().padStart(2, '0');
        timerElement.innerText = `${m}:${s} / 10:00`;

        if (seconds >= MAX_TIME) {
            stopRecording(); // Auto stop
        }
    }, 1000);
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        clearInterval(timerInterval);
    }
}

function stopStream() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
}

// FORM SUBMISSION
const form = document.getElementById('capsule-form');
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Check which mode is active
    const activeSection = document.querySelector('.input-section.active').id;
    const blobFile = document.getElementById('blob-file');
    const hiddenText = document.getElementById('hidden-text');

    if (activeSection === 'text-section') {
        const textVal = document.getElementById('message-text').value;
        if (!textVal) {
            alert("Please write a message.");
            return;
        }
        hiddenText.value = textVal;
        // Clear file input
        blobFile.value = '';
    } else {
        // Video or Audio
        if (recordedChunks.length === 0) {
            alert("Please record something first!");
            return;
        }
        const blob = new Blob(recordedChunks, { type: 'video/webm' });

        // Create a file from the blob
        const file = new File([blob], "recording.webm", { type: 'video/webm' });

        // Use DataTransfer to set the file input (hacky but standard for programmatically setting file inputs)
        const container = new DataTransfer();
        container.items.add(file);
        blobFile.files = container.files;
    }

    // Submit

    // Trigger Warp Effect
    document.getElementById('warp-overlay').classList.add('active');

    // Play a "Launch" sound if we had one, or just wait a moment for effect
    // We delay submission slightly to let the user see the effect
    setTimeout(() => {
        form.submit();
    }, 2000);
});

