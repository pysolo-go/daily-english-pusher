let recorder;
let isRecording = false;
let subtitleDiv;
let loopId;

// Inject CSS
const style = document.createElement('style');
style.textContent = `
  #ai-subtitle-overlay {
    position: fixed;
    bottom: 50px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    z-index: 2147483647;
    text-align: center;
    font-size: 20px;
    font-family: sans-serif;
    pointer-events: none;
    min-width: 300px;
    max-width: 80%;
    text-shadow: 1px 1px 2px black;
  }
  #ai-subtitle-zh {
    font-size: 24px;
    font-weight: bold;
    color: #ffeb3b;
  }
  #ai-subtitle-en {
    font-size: 16px;
    color: #ddd;
    margin-top: 5px;
  }
`;
document.head.appendChild(style);

function createOverlay() {
  if (!document.getElementById('ai-subtitle-overlay')) {
    subtitleDiv = document.createElement('div');
    subtitleDiv.id = 'ai-subtitle-overlay';
    subtitleDiv.innerHTML = `
      <div id="ai-subtitle-zh">等待翻译...</div>
      <div id="ai-subtitle-en">Waiting for translation...</div>
    `;
    document.body.appendChild(subtitleDiv);
  } else {
    subtitleDiv = document.getElementById('ai-subtitle-overlay');
    subtitleDiv.style.display = 'block';
  }
}

chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.action === 'startCapture') {
    startCapture(request.streamId);
    sendResponse({status: 'started'});
  } else if (request.action === 'stopCapture') {
    stopCapture();
    sendResponse({status: 'stopped'});
  } else if (request.action === 'getStatus') {
    sendResponse({isRecording: isRecording});
  }
  return true; // Keep channel open for async response
});

async function startCapture(streamId) {
  if (isRecording) return;
  createOverlay();
  
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        mandatory: {
          chromeMediaSource: 'tab',
          chromeMediaSourceId: streamId
        }
      },
      video: false
    });
    
    // Create AudioContext to keep audio playing locally (otherwise it mutes)
    const audioCtx = new AudioContext();
    const source = audioCtx.createMediaStreamSource(stream);
    source.connect(audioCtx.destination); // Play back to speakers

    recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
    
    recorder.ondataavailable = async (e) => {
      if (e.data.size > 0) {
        await sendAudio(e.data);
      }
    };

    recorder.onstop = () => {
        if (isRecording) {
            recorder.start();
        }
    };

    recorder.start();
    isRecording = true;
    console.log("Started recording...");

    // Restart recording every 2 seconds to force valid WebM headers
    loopId = setInterval(() => {
        if (recorder && recorder.state === 'recording') {
            recorder.stop();
        }
    }, 2000);

  } catch (err) {
    console.error("Error capturing audio:", err);
    alert("Capture failed: " + err.message);
  }
}

function stopCapture() {
  if (isRecording) {
    isRecording = false; // Set flag first to prevent restart in onstop
    if (loopId) clearInterval(loopId);
    if (recorder) {
        recorder.stop();
        recorder.stream.getTracks().forEach(t => t.stop());
    }
    if (subtitleDiv) subtitleDiv.style.display = 'none';
    console.log("Stopped recording.");
  }
}

async function sendAudio(blob) {
  const formData = new FormData();
  formData.append('file', blob, 'audio.webm');

  try {
    const response = await fetch('http://localhost:8000/transcribe', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      const data = await response.json();
      updateSubtitle(data.translated, data.original);
    }
  } catch (err) {
    console.error("Server error:", err);
  }
}

function updateSubtitle(zh, en) {
  if (!zh && !en) return;
  const zhEl = document.getElementById('ai-subtitle-zh');
  const enEl = document.getElementById('ai-subtitle-en');
  if (zhEl) zhEl.innerText = zh || "";
  if (enEl) enEl.innerText = en || "";
}
