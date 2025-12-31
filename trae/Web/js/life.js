const canvas = document.getElementById('lifeCanvas');
const ctx = canvas.getContext('2d');

let resolution = 10;
let cols, rows;
let grid;
let isPlaying = false;
let animationId;

function make2DArray(cols, rows) {
    let arr = new Array(cols);
    for (let i = 0; i < arr.length; i++) {
        arr[i] = new Array(rows).fill(0);
    }
    return arr;
}

function setup() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    cols = Math.floor(canvas.width / resolution);
    rows = Math.floor(canvas.height / resolution);

    grid = make2DArray(cols, rows);
    randomize();
    draw();
}

function randomize() {
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            grid[i][j] = Math.floor(Math.random() * 2);
        }
    }
    draw();
}

function clearGrid() {
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            grid[i][j] = 0;
        }
    }
    draw();
}

function draw() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            let x = i * resolution;
            let y = j * resolution;
            if (grid[i][j] == 1) {
                ctx.fillStyle = '#00ff88';
                ctx.fillRect(x, y, resolution - 1, resolution - 1);
            }
        }
    }
}

function computeNextGen() {
    let next = make2DArray(cols, rows);

    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            let state = grid[i][j];
            
            // Count neighbors
            let sum = 0;
            let neighbors = countNeighbors(grid, i, j);

            if (state == 0 && neighbors == 3) {
                next[i][j] = 1;
            } else if (state == 1 && (neighbors < 2 || neighbors > 3)) {
                next[i][j] = 0;
            } else {
                next[i][j] = state;
            }
        }
    }
    grid = next;
    draw();
}

function countNeighbors(grid, x, y) {
    let sum = 0;
    for (let i = -1; i < 2; i++) {
        for (let j = -1; j < 2; j++) {
            let col = (x + i + cols) % cols;
            let row = (y + j + rows) % rows;
            sum += grid[col][row];
        }
    }
    sum -= grid[x][y];
    return sum;
}

function animate() {
    if (isPlaying) {
        computeNextGen();
        animationId = requestAnimationFrame(animate);
    }
}

// UI Controls
const playBtn = document.getElementById('play-btn');
const randomBtn = document.getElementById('random-btn');
const clearBtn = document.getElementById('clear-btn');

playBtn.addEventListener('click', () => {
    isPlaying = !isPlaying;
    if (isPlaying) {
        playBtn.innerText = 'Pause';
        playBtn.classList.add('active');
        animate();
    } else {
        playBtn.innerText = 'Play';
        playBtn.classList.remove('active');
        cancelAnimationFrame(animationId);
    }
});

randomBtn.addEventListener('click', () => {
    randomize();
});

clearBtn.addEventListener('click', () => {
    clearGrid();
    if (isPlaying) {
        isPlaying = false;
        playBtn.innerText = 'Play';
        playBtn.classList.remove('active');
        cancelAnimationFrame(animationId);
    }
});

// Mouse Interaction
let isDrawing = false;

function handleMouse(e) {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / resolution);
    const y = Math.floor((e.clientY - rect.top) / resolution);
    
    if (x >= 0 && x < cols && y >= 0 && y < rows) {
        grid[x][y] = 1;
        draw();
    }
}

canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    handleMouse(e);
});

canvas.addEventListener('mousemove', (e) => {
    if (isDrawing) handleMouse(e);
});

canvas.addEventListener('mouseup', () => isDrawing = false);

window.addEventListener('resize', setup);

// Init
setup();