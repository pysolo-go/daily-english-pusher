const canvas = document.getElementById('gravityCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let gravity = 1;
let friction = 0.8; // Energy loss on bounce

class Ball {
    constructor(x, y, dx, dy, radius, color) {
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
        this.radius = radius;
        this.color = color;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.strokeStyle = '#333';
        ctx.stroke();
        ctx.closePath();
    }

    update() {
        // Gravity check
        if (this.y + this.radius + this.dy > canvas.height) {
            this.dy = -this.dy * friction;
            // Prevent sticking to bottom
            this.y = canvas.height - this.radius;
        } else {
            this.dy += gravity;
        }

        // Side walls check
        if (this.x + this.radius + this.dx > canvas.width || this.x - this.radius <= 0) {
            this.dx = -this.dx * friction;
        }

        this.x += this.dx;
        this.y += this.dy;

        this.draw();
    }
}

let balls = [];
const colors = ['#FF3366', '#00FF88', '#00AAFF', '#FFCC00', '#9933FF'];

function init() {
    balls = [];
    for (let i = 0; i < 5; i++) {
        spawnBall();
    }
}

function spawnBall(x, y) {
    const radius = Math.random() * 20 + 10;
    const spawnX = x || Math.random() * (canvas.width - radius * 2) + radius;
    const spawnY = y || Math.random() * (canvas.height - 300) + radius;
    const dx = (Math.random() - 0.5) * 10;
    const dy = (Math.random() - 0.5) * 10;
    const color = colors[Math.floor(Math.random() * colors.length)];
    balls.push(new Ball(spawnX, spawnY, dx, dy, radius, color));
}

function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    balls.forEach(ball => {
        ball.update();
    });
}

// Mouse Interaction
let isDragging = false;
let dragStartX, dragStartY;

window.addEventListener('mousedown', (e) => {
    if (e.button === 0) { // Left click
        isDragging = true;
        dragStartX = e.clientX;
        dragStartY = e.clientY;
    } else if (e.button === 2) { // Right click
        spawnBall(e.clientX, e.clientY);
    }
});

window.addEventListener('mouseup', (e) => {
    if (e.button === 0 && isDragging) {
        isDragging = false;
        const dragEndX = e.clientX;
        const dragEndY = e.clientY;
        
        // Velocity based on drag distance
        const dx = (dragStartX - dragEndX) * 0.2;
        const dy = (dragStartY - dragEndY) * 0.2;
        
        // Spawn a ball thrown by mouse
        const radius = Math.random() * 20 + 10;
        const color = colors[Math.floor(Math.random() * colors.length)];
        balls.push(new Ball(dragStartX, dragStartY, dx, dy, radius, color));
    }
});

// Prevent context menu on right click
window.addEventListener('contextmenu', event => event.preventDefault());

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    init();
});

init();
animate();