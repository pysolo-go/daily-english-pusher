const canvas = document.getElementById('fractalCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let angle = 0;
let lenScale = 0;

function drawTree(startX, startY, len, angle, branchWidth) {
    ctx.beginPath();
    ctx.save();
    ctx.strokeStyle = `hsl(${Math.random() * 60 + 10}, 80%, 60%)`; // Gold/Orange hues
    ctx.fillStyle = `hsl(${Math.random() * 60 + 10}, 80%, 60%)`;
    ctx.lineWidth = branchWidth;
    ctx.translate(startX, startY);
    ctx.rotate(angle * Math.PI / 180);
    ctx.moveTo(0, 0);
    ctx.lineTo(0, -len);
    ctx.stroke();

    if (len < 10) {
        ctx.beginPath();
        ctx.arc(0, -len, 5, 0, Math.PI/2);
        ctx.fill();
        ctx.restore();
        return;
    }

    drawTree(0, -len, len * 0.75, angle + lenScale, branchWidth * 0.7);
    drawTree(0, -len, len * 0.75, angle - lenScale, branchWidth * 0.7);
    
    // Add a middle branch sometimes for complexity
    // if (Math.random() > 0.5) {
    //    drawTree(0, -len, len * 0.6, angle, branchWidth * 0.7);
    // }

    ctx.restore();
}

function animate() {
    // We don't animate in loop, we animate on mouse move for better performance/control
    // But to show initial state:
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Center bottom
    const trunkHeight = canvas.height * 0.25;
    
    // Gradient trunk
    ctx.strokeStyle = '#fff';
    
    // The recursive draw
    // Use mouse position to determine variables
    // angle: -45 to 45 depending on mouse X
    // lenScale: variation based on mouse Y
    
    // For cleaner code, let's just redraw on mousemove
}

function draw(e) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const mouseX = e ? e.clientX : window.innerWidth / 2;
    const mouseY = e ? e.clientY : window.innerHeight / 2;
    
    // Map mouse X to angle variation
    const angleVar = (mouseX / canvas.width) * 90 - 45; // -45 to +45 degrees shift
    
    // Map mouse Y to branch spread angle
    const spreadAngle = (mouseY / canvas.height) * 90; 
    
    // Recursive start
    ctx.shadowBlur = 10;
    ctx.shadowColor = 'rgba(255, 200, 0, 0.5)';
    
    // Root
    drawBranch(canvas.width / 2, canvas.height, 150, 0, 20, spreadAngle, angleVar);
}

function drawBranch(x, y, len, angle, width, spread, sway) {
    ctx.beginPath();
    ctx.save();
    
    // Color gradient based on length
    const hue = 50 - (len / 150) * 50; // 0 to 50 (Red to Gold)
    ctx.strokeStyle = `hsl(${hue}, 100%, 50%)`;
    ctx.lineWidth = width;
    
    ctx.translate(x, y);
    ctx.rotate(angle * Math.PI / 180);
    
    ctx.moveTo(0, 0);
    ctx.lineTo(0, -len);
    ctx.stroke();
    
    if (len < 10) {
        // Leaf
        ctx.fillStyle = `hsl(${Math.random() * 100 + 50}, 100%, 50%)`;
        ctx.beginPath();
        ctx.arc(0, -len, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
        return;
    }
    
    const newLen = len * 0.7;
    const newWidth = width * 0.7;
    
    drawBranch(0, -len, newLen, spread + sway, newWidth, spread, sway);
    drawBranch(0, -len, newLen, -spread + sway, newWidth, spread, sway);
    
    ctx.restore();
}

window.addEventListener('mousemove', draw);
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    draw();
});

// Initial draw
draw();