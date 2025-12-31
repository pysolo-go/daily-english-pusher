const canvas = document.getElementById('clothCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Configuration
const physicsAccuracy = 3;
const mouseInfluence = 20;
const mouseCut = 5;
const gravity = 1200;
const clothY = 50;
const spacing = 15; // increased spacing for optimization
const tearDist = 60;
const friction = 0.99;
const bounce = 0.5;

let points = [];
let constraints = []; // Separate constraints array is standard but here we might embed in points or simple loop

class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.px = x;
        this.py = y;
        this.vx = 0;
        this.vy = 0;
        this.pinX = null;
        this.pinY = null;
        
        this.constraints = [];
    }

    update(delta) {
        if (this.pinX != null && this.pinY != null) return;

        if (mouse.down) {
            const dx = this.x - mouse.x;
            const dy = this.y - mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (mouse.button === 0 && dist < mouseInfluence) { // Left click pull
                this.px = this.x - (mouse.x - mouse.px) * 1.8;
                this.py = this.y - (mouse.y - mouse.py) * 1.8;
            } else if (mouse.button === 2 && dist < mouseCut) { // Right click cut
                this.constraints = [];
            }
        }

        // Verlet Integration
        // vx = x - px
        // x = x + vx + a * dt * dt
        
        // Add gravity
        this.addForce(0, gravity);

        const nx = this.x + (this.x - this.px) * friction + this.vx * delta * delta;
        const ny = this.y + (this.y - this.py) * friction + this.vy * delta * delta;

        this.px = this.x;
        this.py = this.y;
        this.x = nx;
        this.y = ny;
        this.vx = 0;
        this.vy = 0;
        
        // Floor collision
        if (this.y > canvas.height) {
            this.y = canvas.height;
            this.py = this.y + (this.py - this.y) * bounce;
        }
    }
    
    addForce(x, y) {
        this.vx += x;
        this.vy += y;
    }

    draw() {
        if (this.constraints.length === 0) return;
        /* Draw handled by constraints */
    }

    resolveConstraints() {
        if (this.pinX != null && this.pinY != null) {
            this.x = this.pinX;
            this.y = this.pinY;
            return;
        }

        this.constraints.forEach(constraint => constraint.resolve());
    }
    
    attach(point) {
        this.constraints.push(new Constraint(this, point));
    }
    
    removeConstraint(constraint) {
        this.constraints.splice(this.constraints.indexOf(constraint), 1);
    }
}

class Constraint {
    constructor(p1, p2) {
        this.p1 = p1;
        this.p2 = p2;
        this.length = spacing;
    }

    resolve() {
        const dx = this.p1.x - this.p2.x;
        const dy = this.p1.y - this.p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist > tearDist) {
            this.p1.removeConstraint(this);
            return;
        }

        const diff = (this.length - dist) / dist;

        // Inverse mass (simplified, assumed equal)
        const px = dx * diff * 0.5;
        const py = dy * diff * 0.5;

        if (this.p1.pinX == null) {
            this.p1.x += px;
            this.p1.y += py;
        }
        if (this.p2.pinX == null) {
            this.p2.x -= px;
            this.p2.y -= py;
        }
    }

    draw() {
        ctx.moveTo(this.p1.x, this.p1.y);
        ctx.lineTo(this.p2.x, this.p2.y);
    }
}

function init() {
    points = [];
    const cols = Math.floor(canvas.width / spacing) - 4;
    const rows = Math.floor(canvas.height / spacing) - 10;
    
    const startX = (canvas.width - cols * spacing) / 2;

    for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
            const p = new Point(startX + x * spacing, clothY + y * spacing);
            
            // Pin top row
            if (y === 0) {
                p.pinX = p.x;
                p.pinY = p.y;
            }
            
            // Attach to left
            if (x !== 0) {
                p.attach(points[points.length - 1]);
            }
            // Attach to top
            if (y !== 0) {
                p.attach(points[x + (y - 1) * cols]);
            }
            
            points.push(p);
        }
    }
}

function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Update Physics
    // Delta time is fixed for stability in this simple implementation
    const delta = 0.016; 

    for (let i = 0; i < physicsAccuracy; i++) {
        points.forEach(p => p.resolveConstraints());
    }

    points.forEach(p => p.update(delta));

    // Draw
    ctx.beginPath();
    ctx.strokeStyle = '#888';
    points.forEach(p => {
        p.constraints.forEach(c => c.draw());
    });
    ctx.stroke();

    requestAnimationFrame(update);
}

// Mouse Interactions
const mouse = {
    down: false,
    button: 0,
    x: 0,
    y: 0,
    px: 0,
    py: 0
};

canvas.addEventListener('mousedown', (e) => {
    mouse.down = true;
    mouse.button = e.button;
    mouse.px = mouse.x;
    mouse.py = mouse.y;
});

canvas.addEventListener('mousemove', (e) => {
    mouse.px = mouse.x;
    mouse.py = mouse.y;
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

canvas.addEventListener('mouseup', () => mouse.down = false);
canvas.addEventListener('contextmenu', e => e.preventDefault());

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    init();
});

init();
update();