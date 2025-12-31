const canvas = document.getElementById('visualizer');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('start-btn');
const startScreen = document.getElementById('start-screen');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let audioContext;
let analyser;
let source;
let dataArray;

startBtn.addEventListener('click', async () => {
    try {
        startScreen.classList.add('hidden');
        
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        source = audioContext.createMediaStreamSource(stream);
        source.connect(analyser);
        
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
        
        animate();
    } catch (err) {
        console.error('Error accessing microphone:', err);
        alert('Could not access microphone. Please ensure you have a microphone connected and allowed permission.');
        startScreen.classList.remove('hidden');
    }
});

function animate() {
    requestAnimationFrame(animate);
    
    // Clear with fade effect
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    analyser.getByteFrequencyData(dataArray);
    
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 150;
    
    // Draw circular visualizer
    ctx.beginPath();
    ctx.strokeStyle = `hsl(${Date.now() / 20 % 360}, 100%, 50%)`;
    ctx.lineWidth = 2;
    
    const bars = dataArray.length;
    const step = (Math.PI * 2) / bars;
    
    for (let i = 0; i < bars; i++) {
        const barHeight = dataArray[i] * 1.5;
        
        // Circular coordinates
        const rad = i * step;
        const x1 = centerX + Math.cos(rad) * radius;
        const y1 = centerY + Math.sin(rad) * radius;
        const x2 = centerX + Math.cos(rad) * (radius + barHeight);
        const y2 = centerY + Math.sin(rad) * (radius + barHeight);
        
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        
        // Also draw internal circle
        const x3 = centerX + Math.cos(rad) * (radius - barHeight * 0.2);
        const y3 = centerY + Math.sin(rad) * (radius - barHeight * 0.2);
        ctx.moveTo(x1, y1);
        ctx.lineTo(x3, y3);
    }
    
    ctx.stroke();
    
    // Center pulse
    const avg = dataArray.reduce((a, b) => a + b) / dataArray.length;
    ctx.beginPath();
    ctx.arc(centerX, centerY, avg * 0.5, 0, Math.PI * 2);
    ctx.fillStyle = `hsla(${Date.now() / 20 % 360}, 100%, 50%, 0.5)`;
    ctx.fill();
}

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});