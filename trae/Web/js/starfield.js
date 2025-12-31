const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

let width, height;
let stars = [];
let speed = 0;
let rotation = 0;

function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}

window.addEventListener('resize', resize);
resize();

class Star {
    constructor() {
        this.reset();
    }

    reset() {
        this.x = (Math.random() * width - width / 2) * 2;
        this.y = (Math.random() * height - height / 2) * 2;
        this.z = Math.random() * width;
        this.pz = this.z;
    }

    update() {
        this.z -= speed;
        
        // Rotation logic
        const x = this.x;
        const y = this.y;
        
        const cos = Math.cos(rotation);
        const sin = Math.sin(rotation);
        
        this.x = x * cos - y * sin;
        this.y = y * cos + x * sin;

        if (this.z < 1) {
            this.reset();
            this.z = width;
            this.pz = this.z;
        }
    }

    draw() {
        const sx = (this.x / this.z) * width / 2 + width / 2;
        const sy = (this.y / this.z) * height / 2 + height / 2;

        const r = Math.max(0, (1 - this.z / width) * 4);

        // Previous position for trail
        const px = (this.x / this.pz) * width / 2 + width / 2;
        const py = (this.y / this.pz) * height / 2 + height / 2;
        
        this.pz = this.z;

        if (sx >= 0 && sx <= width && sy >= 0 && sy <= height) {
            const alpha = 1 - this.z / width;
            ctx.beginPath();
            ctx.moveTo(px, py);
            ctx.lineTo(sx, sy);
            ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.lineWidth = r;
            ctx.stroke();
            
            ctx.beginPath();
            ctx.arc(sx, sy, r/2, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(200, 220, 255, ${alpha})`;
            ctx.fill();
        }
    }
}

// Init stars
for (let i = 0; i < 800; i++) {
    stars.push(new Star());
}

// Mouse interaction
let targetSpeed = 10;
let targetRotation = 0;

document.addEventListener('mousemove', (e) => {
    const x = (e.clientX - width / 2) / width;
    const y = (e.clientY - height / 2) / height;
    
    targetSpeed = 20 + x * 50;
    targetRotation = y * 0.1;
});

function animate() {
    // Clear background with slight trail
    ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
    ctx.fillRect(0, 0, width, height);

    // Smooth interpolation
    speed += (targetSpeed - speed) * 0.1;
    rotation += (targetRotation - rotation) * 0.1;

    stars.forEach(star => {
        star.update();
        star.draw();
    });

    requestAnimationFrame(animate);
}

animate();