$baseUrl = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.9/wasm"
$modelUrl = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
$destDir = "c:\Users\chi.zhang\Documents\trae_projects\trae\jarvis-holographic-main\public\models"

Write-Output "Downloading MediaPipe assets to $destDir..."

# Download WASM files
Invoke-WebRequest -Uri "$baseUrl/vision_wasm_internal.wasm" -OutFile "$destDir\vision_wasm_internal.wasm"
Invoke-WebRequest -Uri "$baseUrl/vision_wasm_internal.js" -OutFile "$destDir\vision_wasm_internal.js"

# Download Model
Invoke-WebRequest -Uri $modelUrl -OutFile "$destDir\gesture_recognizer.task"

Write-Output "Assets downloaded successfully."
