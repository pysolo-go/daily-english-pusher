const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

let width, height;
let fireworks = [];
let particles = [];

function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}

window.addEventListener('resize', resize);
resize();

function random(min, max) {
    return Math.random() * (max - min) + min;
}

class Firework {
    constructor(targetX, targetY) {
        this.x = width / 2;
        this.y = height;
        this.targetX = targetX;
        this.targetY = targetY;
        this.speed = 2;
        this.angle = Math.atan2(targetY - this.y, targetX - this.x);
        this.vx = Math.cos(this.angle) * this.speed;
        this.vy = Math.sin(this.angle) * this.speed;
        this.acceleration = 1.05;
        this.brightness = random(50, 70);
        this.targetRadius = 1;
        this.coordinateCount = 3;
        this.coordinates = [];
        
        while(this.coordinateCount--) {
            this.coordinates.push([this.x, this.y]);
        }
    }

    update(index) {
        this.coordinates.pop();
        this.coordinates.unshift([this.x, this.y]);
        
        this.speed *= this.acceleration;
        
        this.vx = Math.cos(this.angle) * this.speed;
        this.vy = Math.sin(this.angle) * this.speed;
        
        this.x += this.vx;
        this.y += this.vy;
        
        const distance = Math.hypot(this.targetX - this.x, this.targetY - this.y);
        
        if(distance < this.speed) {
            createParticles(this.targetX, this.targetY);
            fireworks.splice(index, 1);
        }
    }

    draw() {
        ctx.beginPath();
        ctx.moveTo(this.coordinates[this.coordinates.length - 1][0], this.coordinates[this.coordinates.length - 1][1]);
        ctx.lineTo(this.x, this.y);
        ctx.strokeStyle = 'hsl(' + hue + ', 100%, ' + this.brightness + '%)';
        ctx.stroke();
    }
}

class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.angle = random(0, Math.PI * 2);
        this.speed = random(1, 10);
        this.friction = 0.95;
        this.gravity = 1;
        this.hue = random(hue - 20, hue + 20);
        this.brightness = random(50, 80);
        this.alpha = 1;
        this.decay = random(0.015, 0.03);
        
        this.coordinates = [];
        this.coordinateCount = 5;
        while(this.coordinateCount--) {
            this.coordinates.push([this.x, this.y]);
        }
    }

    update(index) {
        this.coordinates.pop();
        this.coordinates.unshift([this.x, this.y]);
        
        this.speed *= this.friction;
        this.x += Math.cos(this.angle) * this.speed;
        this.y += Math.sin(this.angle) * this.speed + this.gravity;
        this.alpha -= this.decay;
        
        if(this.alpha <= this.decay) {
            particles.splice(index, 1);
        }
    }

    draw() {
        ctx.beginPath();
        ctx.moveTo(this.coordinates[this.coordinates.length - 1][0], this.coordinates[this.coordinates.length - 1][1]);
        ctx.lineTo(this.x, this.y);
        ctx.strokeStyle = 'hsla(' + this.hue + ', 100%, ' + this.brightness + '%, ' + this.alpha + ')';
        ctx.stroke();
    }
}

function createParticles(x, y) {
    let particleCount = 30;
    while(particleCount--) {
        particles.push(new Particle(x, y));
    }
}

let hue = 120;
let limiterTotal = 5;
let limiterTick = 0;
let timerTotal = 80;
let timerTick = 0;
let mousedown = false;
let mx, my;

canvas.addEventListener('mousemove', function(e) {
    mx = e.clientX;
    my = e.clientY;
});

canvas.addEventListener('mousedown', function(e) {
    e.preventDefault();
    mousedown = true;
});

canvas.addEventListener('mouseup', function(e) {
    e.preventDefault();
    mousedown = false;
});

function loop() {
    requestAnimationFrame(loop);
    
    hue += 0.5;
    
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(0, 0, width, height);
    ctx.globalCompositeOperation = 'lighter';
    
    let i = fireworks.length;
    while(i--) {
        fireworks[i].draw();
        fireworks[i].update(i);
    }
    
    let j = particles.length;
    while(j--) {
        particles[j].draw();
        particles[j].update(j);
    }
    
    if(timerTick >= timerTotal) {
        if(!mousedown) {
            fireworks.push(new Firework(width / 2, height, random(0, width), random(0, height / 2)));
            timerTick = 0;
        }
    } else {
        timerTick++;
    }
    
    if(limiterTick >= limiterTotal) {
        if(mousedown) {
            fireworks.push(new Firework(mx, my));
            limiterTick = 0;
        }
    } else {
        limiterTick++;
    }
}

loop();