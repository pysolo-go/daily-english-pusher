let mediaRecorder;
let audioChunks = [];
let intervalId;
let stream;

// Check status on load
document.addEventListener('DOMContentLoaded', async () => {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) return;

    chrome.tabs.sendMessage(tab.id, { action: 'getStatus' }, (response) => {
      // Ignore errors (content script might not be injected yet)
      if (chrome.runtime.lastError) return;
      
      if (response && response.isRecording) {
        setRecordingState(true);
      } else {
        setRecordingState(false);
      }
    });
  } catch (e) {
    console.error(e);
  }
});

document.getElementById('startBtn').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  // Use tabCapture to get stream ID
  chrome.tabCapture.getMediaStreamId({ consumerTabId: tab.id }, (streamId) => {
    if (chrome.runtime.lastError) {
      const err = chrome.runtime.lastError.message;
      if (err.includes("active stream")) {
        updateStatus("Already capturing. Please refresh the page.");
      } else {
        updateStatus('Error: ' + err);
      }
      return;
    }
    
    // Send message to content script to start capturing with this ID
    chrome.tabs.sendMessage(tab.id, { 
      action: 'startCapture', 
      streamId: streamId 
    }, (response) => {
        if (chrome.runtime.lastError) {
            updateStatus("Error: Please refresh the page.");
        }
    });
    
    setRecordingState(true);
    updateStatus('Initializing...');
  });
});

document.getElementById('stopBtn').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.tabs.sendMessage(tab.id, { action: 'stopCapture' });
  
  setRecordingState(false);
  updateStatus('Stopped');
});

function setRecordingState(isRecording) {
  document.getElementById('startBtn').disabled = isRecording;
  document.getElementById('stopBtn').disabled = !isRecording;
  if (isRecording) {
      updateStatus('Recording...');
  } else {
      updateStatus('Ready');
  }
}

function updateStatus(msg) {
  document.getElementById('status').innerText = msg;
}
