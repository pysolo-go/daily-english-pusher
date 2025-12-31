const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let width, height;
let particles = [];

let mouse = { x: -1000, y: -1000 };

// Configuration
const particleCount = 400;
const colors = ['#FF0055', '#00AAFF', '#55FF00', '#FFDD00', '#AA00FF'];

class Particle {
    constructor() {
        this.reset();
        // Randomize initial position
        this.x = Math.random() * width;
        this.y = Math.random() * height;
    }

    reset() {
        this.x = mouse.x;
        this.y = mouse.y;
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 5 + 1;
        this.vx = Math.cos(angle) * speed;
        this.vy = Math.sin(angle) * speed;
        this.life = 1.0;
        this.decay = Math.random() * 0.02 + 0.005;
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.size = Math.random() * 3 + 1;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vx *= 0.96; // Friction
        this.vy *= 0.96;
        this.life -= this.decay;
        this.size *= 0.98;

        // Reset if dead
        if (this.life <= 0 || this.size <= 0.1) {
            // Only respawn if mouse is active (simple check, or random respawn)
            if (Math.random() > 0.5) {
                this.reset();
                // Add some randomness to spawn location if mouse isn't moving fast
                this.x += (Math.random() - 0.5) * 50;
                this.y += (Math.random() - 0.5) * 50;
            } else {
                // Random spawn elsewhere to keep screen busy
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.life = 1;
                this.vx = (Math.random() - 0.5) * 2;
                this.vy = (Math.random() - 0.5) * 2;
            }
        }
    }

    draw() {
        ctx.globalAlpha = this.life;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
}

function init() {
    resize();
    particles = []; // Clear existing
    for(let i=0; i<particleCount; i++) {
        particles.push(new Particle());
    }
}

function animate() {
    // Trail effect
    ctx.globalAlpha = 0.1;
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, width, height);
    
    ctx.globalCompositeOperation = 'screen'; // Additive blending
    
    particles.forEach(p => {
        p.update();
        p.draw();
    });
    
    ctx.globalCompositeOperation = 'source-over';

    // Auto move mouse center if idle
    const time = Date.now() * 0.001;
    if (mouse.x === -1000) {
       // Initial auto animation
       mouse.x = width/2 + Math.cos(time) * (width/3);
       mouse.y = height/2 + Math.sin(time * 1.3) * (height/3);
    }

    requestAnimationFrame(animate);
}

window.addEventListener('resize', () => {
    resize();
    // Re-init particles to fit new screen? Or just let them be.
    // Ideally resizing shouldn't kill particles but for simplicity:
    // init(); 
});
window.addEventListener('mousemove', e => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});
window.addEventListener('touchmove', e => {
    e.preventDefault();
    mouse.x = e.touches[0].clientX;
    mouse.y = e.touches[0].clientY;
}, {passive: false});

init();
animate();
