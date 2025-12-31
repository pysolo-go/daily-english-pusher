const video = document.getElementById('video');
const bufferCanvas = document.getElementById('buffer');
const bufferCtx = bufferCanvas.getContext('2d');
const asciiContainer = document.getElementById('ascii-container');
const errorMsg = document.getElementById('error');

// Density string from dark to light
const density = "Ñ@#W$9876543210?!abc;:+=-,._                    ";

async function setupCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 320, height: 240 } 
        });
        video.srcObject = stream;
        video.addEventListener('loadedmetadata', () => {
            startRendering();
        });
    } catch (err) {
        console.error(err);
        errorMsg.style.display = 'block';
    }
}

function startRendering() {
    const width = 120; // Resolution width (chars)
    const height = 60; // Resolution height (chars)
    
    bufferCanvas.width = width;
    bufferCanvas.height = height;
    
    function render() {
        bufferCtx.drawImage(video, 0, 0, width, height);
        const imageData = bufferCtx.getImageData(0, 0, width, height);
        const data = imageData.data;
        
        let asciiImage = "";
        
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                const offset = (y * width + x) * 4;
                const r = data[offset];
                const g = data[offset + 1];
                const b = data[offset + 2];
                
                const avg = (r + g + b) / 3;
                const len = density.length;
                const charIndex = Math.floor(map(avg, 0, 255, len - 1, 0));
                
                const c = density.charAt(charIndex);
                if (c === " ") asciiImage += "&nbsp;";
                else asciiImage += c;
            }
            asciiImage += "<br/>";
        }
        
        asciiContainer.innerHTML = asciiImage;
        requestAnimationFrame(render);
    }
    
    render();
}

function map(value, start1, stop1, start2, stop2) {
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1));
}

setupCamera();