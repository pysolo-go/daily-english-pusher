const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

let width, height;
let particles = [];
let flowField = [];
let rows, cols;
const scale = 20; // Size of each grid cell
let zOff = 0; // Time dimension for noise
let mouse = { x: null, y: null };

// Perlin Noise Implementation
const Noise = (function() {
    // Permutation table
    const p = new Uint8Array(512);
    const permutation = [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180];
    
    for (let i = 0; i < 256; i++) p[256 + i] = p[i] = permutation[i];

    function fade(t) { return t * t * t * (t * (t * 6 - 15) + 10); }
    function lerp(t, a, b) { return a + t * (b - a); }
    function grad(hash, x, y, z) {
        const h = hash & 15;
        const u = h < 8 ? x : y;
        const v = h < 4 ? y : h === 12 || h === 14 ? x : z;
        return ((h & 1) === 0 ? u : -u) + ((h & 2) === 0 ? v : -v);
    }

    return {
        perlin3: function(x, y, z) {
            const X = Math.floor(x) & 255;
            const Y = Math.floor(y) & 255;
            const Z = Math.floor(z) & 255;
            x -= Math.floor(x);
            y -= Math.floor(y);
            z -= Math.floor(z);
            const u = fade(x);
            const v = fade(y);
            const w = fade(z);
            const A = p[X] + Y, AA = p[A] + Z, AB = p[A + 1] + Z;
            const B = p[X + 1] + Y, BA = p[B] + Z, BB = p[B + 1] + Z;
            return lerp(w, lerp(v, lerp(u, grad(p[AA], x, y, z),
                grad(p[BA], x - 1, y, z)),
                lerp(u, grad(p[AB], x, y - 1, z),
                grad(p[BB], x - 1, y - 1, z))),
                lerp(v, lerp(u, grad(p[AA + 1], x, y, z - 1),
                grad(p[BA + 1], x - 1, y, z - 1)),
                lerp(u, grad(p[AB + 1], x, y - 1, z - 1),
                grad(p[BB + 1], x - 1, y - 1, z - 1))));
        }
    };
})();

class Particle {
    constructor() {
        this.pos = { x: Math.random() * width, y: Math.random() * height };
        this.vel = { x: 0, y: 0 };
        this.acc = { x: 0, y: 0 };
        this.maxSpeed = 2 + Math.random() * 2;
        this.prevPos = { x: this.pos.x, y: this.pos.y };
        this.color = `hsla(${Math.random() * 360}, 100%, 50%, 0.5)`;
    }

    update() {
        this.prevPos.x = this.pos.x;
        this.prevPos.y = this.pos.y;
        
        // Find grid position
        let x = Math.floor(this.pos.x / scale);
        let y = Math.floor(this.pos.y / scale);
        let index = x + y * cols;
        
        if (flowField[index]) {
            this.applyForce(flowField[index]);
        }

        // Mouse attraction
        if (mouse.x !== null) {
            let dx = mouse.x - this.pos.x;
            let dy = mouse.y - this.pos.y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < 200) {
                let force = { x: dx / distance, y: dy / distance };
                force.x *= 0.5;
                force.y *= 0.5;
                this.applyForce(force);
            }
        }

        this.vel.x += this.acc.x;
        this.vel.y += this.acc.y;
        
        // Limit speed
        let speed = Math.sqrt(this.vel.x * this.vel.x + this.vel.y * this.vel.y);
        if (speed > this.maxSpeed) {
            this.vel.x = (this.vel.x / speed) * this.maxSpeed;
            this.vel.y = (this.vel.y / speed) * this.maxSpeed;
        }
        
        this.pos.x += this.vel.x;
        this.pos.y += this.vel.y;
        
        this.acc.x = 0;
        this.acc.y = 0;
        
        this.edges();
        
        // Update color based on speed/angle
        let angle = Math.atan2(this.vel.y, this.vel.x);
        let hue = (angle + Math.PI) / (2 * Math.PI) * 360 + zOff * 50;
        this.color = `hsla(${hue}, 80%, 60%, 0.8)`;
    }

    applyForce(force) {
        this.acc.x += force.x;
        this.acc.y += force.y;
    }

    edges() {
        if (this.pos.x > width) { this.pos.x = 0; this.prevPos.x = 0; }
        if (this.pos.x < 0) { this.pos.x = width; this.prevPos.x = width; }
        if (this.pos.y > height) { this.pos.y = 0; this.prevPos.y = 0; }
        if (this.pos.y < 0) { this.pos.y = height; this.prevPos.y = height; }
    }

    show() {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(this.prevPos.x, this.prevPos.y);
        ctx.lineTo(this.pos.x, this.pos.y);
        ctx.stroke();
    }
}

function init() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    
    cols = Math.floor(width / scale) + 1;
    rows = Math.floor(height / scale) + 1;
    
    particles = [];
    for (let i = 0; i < 2000; i++) {
        particles.push(new Particle());
    }
}

function resize() {
    init();
}

function animate() {
    // Semi-transparent trail effect
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, width, height);

    let yoff = 0;
    for (let y = 0; y < rows; y++) {
        let xoff = 0;
        for (let x = 0; x < cols; x++) {
            let index = x + y * cols;
            let angle = Noise.perlin3(xoff, yoff, zOff) * Math.PI * 4;
            let v = { x: Math.cos(angle), y: Math.sin(angle) };
            // Enhance vector magnitude for better flow
            v.x *= 0.5; 
            v.y *= 0.5;
            flowField[index] = v;
            xoff += 0.1;
        }
        yoff += 0.1;
    }
    zOff += 0.005;

    for (let p of particles) {
        p.update();
        p.show();
    }
    
    requestAnimationFrame(animate);
}

window.addEventListener('resize', resize);
window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});
window.addEventListener('mousedown', () => {
    // Randomize noise offset on click for new pattern
    zOff += 100;
});
window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
});

init();
animate();
