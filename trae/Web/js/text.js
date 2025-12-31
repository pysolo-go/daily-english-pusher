const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const textInput = document.getElementById('text-input');

let particles = [];
let width, height;
let hue = 0;

// Configuration
const config = {
    particleSize: 2.5,
    resolution: 4, // Lower is higher density (1 = full pixels, 5 = sparse)
    mouseRadius: 120,
    returnSpeed: 0.08,
    friction: 0.92,
    explosionForce: 50
};

class Particle {
    constructor(x, y) {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.targetX = x;
        this.targetY = y;
        this.vx = 0;
        this.vy = 0;
        this.size = Math.random() * config.particleSize + 1;
        this.color = 'white'; // Will be computed dynamically
        this.angle = Math.random() * Math.PI * 2;
        this.hueShift = Math.random() * 40 - 20; // Slight color variation
    }

    draw() {
        // Dynamic color based on position and global hue
        const h = (this.targetX / width) * 360 + hue + this.hueShift;
        const s = 80;
        const l = 60;
        
        ctx.fillStyle = `hsl(${h}, ${s}%, ${l}%)`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.closePath();
        ctx.fill();
    }

    update(mouse) {
        // Physics to return to target
        let dx = this.targetX - this.x;
        let dy = this.targetY - this.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        
        // Mouse Interaction
        let mouseDx = mouse.x - this.x;
        let mouseDy = mouse.y - this.y;
        let mouseDist = Math.sqrt(mouseDx * mouseDx + mouseDy * mouseDy);
        
        // Force from mouse
        if (mouseDist < config.mouseRadius) {
            const force = (config.mouseRadius - mouseDist) / config.mouseRadius;
            const angle = Math.atan2(mouseDy, mouseDx);
            const pushX = Math.cos(angle) * force * 15;
            const pushY = Math.sin(angle) * force * 15;
            
            this.vx -= pushX;
            this.vy -= pushY;
        }

        // Spring back to target
        if (dist > 0) {
            this.vx += dx * 0.015;
            this.vy += dy * 0.015;
        }

        // Explosion / Scatter effect
        if (mouse.clicked) {
            let explodeDx = this.x - mouse.x;
            let explodeDy = this.y - mouse.y;
            let explodeDist = Math.sqrt(explodeDx * explodeDx + explodeDy * explodeDy);
            if (explodeDist < 300) {
                let force = (300 - explodeDist) / 300;
                this.vx += (explodeDx / explodeDist) * force * config.explosionForce;
                this.vy += (explodeDy / explodeDist) * force * config.explosionForce;
            }
        }

        // Friction
        this.vx *= config.friction;
        this.vy *= config.friction;

        // Update position
        this.x += this.vx;
        this.y += this.vy;
    }
}

let mouse = {
    x: null,
    y: null,
    radius: 100,
    clicked: false
};

window.addEventListener('mousemove', function(event) {
    mouse.x = event.x;
    mouse.y = event.y;
});

window.addEventListener('mousedown', () => mouse.clicked = true);
window.addEventListener('mouseup', () => mouse.clicked = false);

window.addEventListener('mouseout', function() {
    mouse.x = undefined;
    mouse.y = undefined;
});

function init() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    
    particles = [];
    
    // Draw text to get coordinates
    ctx.fillStyle = 'white';
    // Responsive font size
    let fontSize = Math.min(width / 4, 250);
    ctx.font = `900 ${fontSize}px "Arial Black", Gadget, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    const text = textInput.value || "TRAE";
    ctx.fillText(text, width / 2, height / 2);
    
    const textCoordinates = ctx.getImageData(0, 0, width, height);
    
    // Sample pixels
    for (let y = 0, y2 = textCoordinates.height; y < y2; y += config.resolution) {
        for (let x = 0, x2 = textCoordinates.width; x < x2; x += config.resolution) {
            // Check alpha > 128 (approx 50% opacity)
            if (textCoordinates.data[(y * 4 * textCoordinates.width) + (x * 4) + 3] > 128) {
                particles.push(new Particle(x, y));
            }
        }
    }
}

function animate() {
    // Trail effect
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    hue += 0.5; // Cycle colors globally

    for (let i = 0; i < particles.length; i++) {
        particles[i].update(mouse);
        particles[i].draw();
    }
    
    // Reset click flag immediately after one frame of force application
    // if we want a "shockwave" style. 
    // Or keep it true if we want continuous repulsion while holding.
    // Let's keep it continuous for "blowing away" effect.
    
    requestAnimationFrame(animate);
}

window.addEventListener('resize', init);
textInput.addEventListener('input', init);

// Add some CSS style injection for the input to look cooler
const style = document.createElement('style');
style.innerHTML = `
    #text-input {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.5);
        border: 1px solid #444;
        color: #0ff;
        padding: 10px 20px;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        text-align: center;
        z-index: 100;
        border-radius: 20px;
        outline: none;
        transition: all 0.3s;
        text-transform: uppercase;
    }
    #text-input:focus {
        border-color: #0ff;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    }
`;
document.head.appendChild(style);

init();
animate();