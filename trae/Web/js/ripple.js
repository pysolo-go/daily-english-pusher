const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

let width = window.innerWidth;
let height = window.innerHeight;
let halfWidth = width >> 1;
let halfHeight = height >> 1;
let size = width * (height + 2) * 2;
let delay = 30;
let oldInd = width;
let newInd = width * (height + 3);
let riprad = 3;
let rippleMap = [];
let lastMap = [];
let mapInd;
let ripple;
let texture;
let line_width = 20;
let step = line_width * 2; 
let count = height / line_width;

canvas.width = width;
canvas.height = height;

// Initialize maps with zeros to prevent undefined values
function initMaps() {
    // Ensure size is integer
    size = Math.floor(width * (height + 2) * 2);
    rippleMap = new Int16Array(size);
    lastMap = new Int16Array(size);
    
    oldInd = width;
    newInd = width * (height + 3);
}

function run() {
    newframe();
    ctx.putImageData(ripple, 0, 0);
}

function newframe() {
    let i, a, b, data, curPixel, newPixel, oldPixel;
    
    i = oldInd;
    oldInd = newInd;
    newInd = i;
    
    i = 0;
    mapInd = oldInd;
    
    // Ripple propagation
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            // Check boundaries for rippleMap access
            let data = (
                rippleMap[mapInd - width] + 
                rippleMap[mapInd + width] + 
                rippleMap[mapInd - 1] + 
                rippleMap[mapInd + 1]
            ) >> 1;
            
            data -= rippleMap[newInd + i];
            data -= data >> 5;
            
            rippleMap[newInd + i] = data;

            // Clamp
            data = 1024 - data;
            
            oldPixel = newPixel = 0;
            
            // Apply refraction (simple version)
            if (lastMap[i] != data) {
                lastMap[i] = data;
                
                // Calculate offset
                a = (((x - halfWidth) * data / 1024) << 0) + halfWidth;
                b = (((y - halfHeight) * data / 1024) << 0) + halfHeight;

                // Bounds check
                if (a >= width) a = width - 1;
                if (a < 0) a = 0;
                if (b >= height) b = height - 1;
                if (b < 0) b = 0;

                newPixel = (a + (b * width)) * 4;
                curPixel = i * 4;
                
                // Safety check for pixel array bounds
                if (newPixel < texture.data.length && curPixel < ripple.data.length) {
                    ripple.data[curPixel] = texture.data[newPixel];
                    ripple.data[curPixel + 1] = texture.data[newPixel + 1];
                    ripple.data[curPixel + 2] = texture.data[newPixel + 2];
                    // Set alpha to fully opaque
                    ripple.data[curPixel + 3] = 255;
                }
            }
            
            mapInd++;
            i++;
        }
    }
}

function disturb(dx, dy) {
    dx = Math.floor(dx);
    dy = Math.floor(dy);
    
    // Safety bounds check for disturb area
    if (dx < riprad || dx >= width - riprad || dy < riprad || dy >= height - riprad) return;
    
    for (let j = dy - riprad; j < dy + riprad; j++) {
        for (let k = dx - riprad; k < dx + riprad; k++) {
            let index = oldInd + (j * width) + k;
            if (index >= 0 && index < size) {
                rippleMap[index] += 128; // Energy
            }
        }
    }
}

function init() {
    width = window.innerWidth;
    height = window.innerHeight;
    halfWidth = width >> 1;
    halfHeight = height >> 1;
    
    canvas.width = width;
    canvas.height = height;
    
    initMaps();
    
    // Create background texture
    const bgCanvas = document.createElement('canvas');
    bgCanvas.width = width;
    bgCanvas.height = height;
    const bgCtx = bgCanvas.getContext('2d');
    
    // Draw gradient background
    const grad = bgCtx.createLinearGradient(0, 0, 0, height);
    grad.addColorStop(0, '#001133');
    grad.addColorStop(0.5, '#003366');
    grad.addColorStop(1, '#001133');
    bgCtx.fillStyle = grad;
    bgCtx.fillRect(0, 0, width, height);
    
    // Draw grid lines
    bgCtx.strokeStyle = '#4488ff';
    bgCtx.lineWidth = 1;
    bgCtx.globalAlpha = 0.3;
    
    const gridSize = 40;
    for(let x=0; x<width; x+=gridSize) {
        bgCtx.beginPath();
        bgCtx.moveTo(x, 0);
        bgCtx.lineTo(x, height);
        bgCtx.stroke();
    }
    for(let y=0; y<height; y+=gridSize) {
        bgCtx.beginPath();
        bgCtx.moveTo(0, y);
        bgCtx.lineTo(width, y);
        bgCtx.stroke();
    }
    
    // Draw some text/shapes
    bgCtx.fillStyle = '#ffffff';
    bgCtx.font = 'bold 100px Arial';
    bgCtx.textAlign = 'center';
    bgCtx.globalAlpha = 0.1;
    bgCtx.fillText('FLUID', width/2, height/2);
    
    texture = bgCtx.getImageData(0, 0, width, height);
    ripple = ctx.getImageData(0, 0, width, height);
    
    // Initial render
    ctx.putImageData(ripple, 0, 0);
    
    // Clear any existing interval if re-initializing
    if (window.animationInterval) clearInterval(window.animationInterval);
    if (window.rainInterval) clearInterval(window.rainInterval);
    
    window.animationInterval = setInterval(run, delay);
    
    // Rain effect
    window.rainInterval = setInterval(() => {
        if(Math.random() > 0.95) {
            disturb(Math.random() * width, Math.random() * height);
        }
    }, 100);
}

canvas.addEventListener('mousemove', function(e) {
    disturb(e.clientX, e.clientY);
});

canvas.addEventListener('click', function(e) {
    // Big splash
    for(let i=0; i<5; i++)
        disturb(e.clientX + (Math.random()-0.5)*20, e.clientY + (Math.random()-0.5)*20);
});

window.addEventListener('resize', init);

init();