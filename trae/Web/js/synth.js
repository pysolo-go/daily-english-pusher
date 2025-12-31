const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const btnStart = document.getElementById('btn-start');
const overlay = document.getElementById('overlay-start');

let width, height;
let audioCtx;
let osc1, osc2, osc3;
let filter;
let gainNode;
let analyser;
let isPlaying = false;

// Synth params
let frequency = 440;
let filterFreq = 1000;
let detune = 0;

function initAudio() {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    // Master Gain
    gainNode = audioCtx.createGain();
    gainNode.gain.value = 0;
    gainNode.connect(audioCtx.destination);
    
    // Analyser
    analyser = audioCtx.createAnalyser();
    analyser.fftSize = 2048;
    gainNode.connect(analyser);

    // Filter
    filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = filterFreq;
    filter.Q.value = 5;
    filter.connect(gainNode);

    // Oscillators
    osc1 = createOsc('sawtooth', 0);
    osc2 = createOsc('square', 10); // slightly detuned
    osc3 = createOsc('sine', -10);  // sub osc
    
    // Connect oscs to filter
    osc1.connect(filter);
    osc2.connect(filter);
    osc3.connect(filter);

    // Start oscs (they will be silent due to gain)
    osc1.start();
    osc2.start();
    osc3.start();
}

function createOsc(type, detuneVal) {
    const osc = audioCtx.createOscillator();
    osc.type = type;
    osc.frequency.value = frequency;
    osc.detune.value = detuneVal;
    return osc;
}

function updateSynth(x, y) {
    if (!audioCtx) return;

    // Map X to frequency (logarithmic scale is better for pitch)
    // 50Hz to 1000Hz
    const minFreq = 50;
    const maxFreq = 1000;
    const percentX = x / width;
    frequency = minFreq * Math.pow(maxFreq / minFreq, percentX);
    
    // Map Y to filter cutoff
    // 100Hz to 5000Hz
    const minFilter = 100;
    const maxFilter = 5000;
    const percentY = 1 - (y / height); // Higher Y (top) = Higher Freq
    filterFreq = minFilter * Math.pow(maxFilter / minFilter, percentY);

    // Apply values
    const now = audioCtx.currentTime;
    osc1.frequency.setTargetAtTime(frequency, now, 0.05);
    osc2.frequency.setTargetAtTime(frequency, now, 0.05);
    osc3.frequency.setTargetAtTime(frequency / 2, now, 0.05); // Sub osc octave down

    filter.frequency.setTargetAtTime(filterFreq, now, 0.05);
}

function triggerAttack() {
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    gainNode.gain.cancelScheduledValues(now);
    gainNode.gain.setValueAtTime(gainNode.gain.value, now);
    gainNode.gain.linearRampToValueAtTime(0.3, now + 0.1);
}

function triggerRelease() {
    if (!audioCtx) return;
    const now = audioCtx.currentTime;
    gainNode.gain.cancelScheduledValues(now);
    gainNode.gain.setValueAtTime(gainNode.gain.value, now);
    gainNode.gain.exponentialRampToValueAtTime(0.001, now + 1);
}

function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
}

function draw() {
    // Retro grid background
    ctx.fillStyle = '#120024';
    ctx.fillRect(0, 0, width, height);

    // Draw Grid
    ctx.strokeStyle = 'rgba(255, 0, 255, 0.2)';
    ctx.lineWidth = 1;
    
    // Perspective Grid
    const horizon = height * 0.4;
    
    // Vertical lines
    for (let i = -width; i < width * 2; i += 50) {
        ctx.beginPath();
        ctx.moveTo(width / 2, horizon);
        ctx.lineTo(i, height);
        ctx.stroke();
    }
    
    // Horizontal lines (closer together as they go up)
    for (let i = 0; i < height - horizon; i += 20 + i * 0.1) {
        ctx.beginPath();
        ctx.moveTo(0, height - i);
        ctx.lineTo(width, height - i);
        ctx.stroke();
    }
    
    // Draw Sun
    const sunGradient = ctx.createLinearGradient(width/2, horizon - 150, width/2, horizon);
    sunGradient.addColorStop(0, '#ffcc00');
    sunGradient.addColorStop(1, '#ff00ff');
    ctx.fillStyle = sunGradient;
    ctx.beginPath();
    ctx.arc(width/2, horizon - 50, 80, 0, Math.PI * 2);
    ctx.fill();
    
    // Sun slices
    ctx.fillStyle = '#120024';
    for(let i=0; i<5; i++) {
        ctx.fillRect(width/2 - 90, horizon - 20 - i*15, 180, 5 + i);
    }

    if (analyser) {
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        analyser.getByteTimeDomainData(dataArray);

        ctx.lineWidth = 3;
        ctx.strokeStyle = '#00ffff';
        ctx.beginPath();
        ctx.shadowBlur = 10;
        ctx.shadowColor = '#00ffff';

        const sliceWidth = width * 1.0 / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const v = dataArray[i] / 128.0;
            const y = v * height / 2;

            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        ctx.lineTo(canvas.width, canvas.height / 2);
        ctx.stroke();
        ctx.shadowBlur = 0;
    }

    requestAnimationFrame(draw);
}

// Interaction
window.addEventListener('resize', resize);

window.addEventListener('mousedown', (e) => {
    if (!audioCtx && overlay.style.display === 'none') return;
    isPlaying = true;
    updateSynth(e.clientX, e.clientY);
    triggerAttack();
});

window.addEventListener('mousemove', (e) => {
    if (isPlaying) {
        updateSynth(e.clientX, e.clientY);
    }
});

window.addEventListener('mouseup', () => {
    isPlaying = false;
    triggerRelease();
});

// Touch support
window.addEventListener('touchstart', (e) => {
    if (!audioCtx && overlay.style.display === 'none') return;
    e.preventDefault();
    isPlaying = true;
    updateSynth(e.touches[0].clientX, e.touches[0].clientY);
    triggerAttack();
}, {passive: false});

window.addEventListener('touchmove', (e) => {
    e.preventDefault();
    if (isPlaying) {
        updateSynth(e.touches[0].clientX, e.touches[0].clientY);
    }
}, {passive: false});

window.addEventListener('touchend', (e) => {
    e.preventDefault();
    isPlaying = false;
    triggerRelease();
});

btnStart.addEventListener('click', () => {
    initAudio();
    overlay.style.display = 'none';
    audioCtx.resume();
});

resize();
draw();
