const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const btnGenerate = document.getElementById('btn-generate');
const btnSolve = document.getElementById('btn-solve');
const statusDiv = document.getElementById('status');

let cols, rows;
const w = 20; // Cell size
let grid = [];
let current; // Current cell being visited
let stack = []; // For backtracking
let start, end;
let path = [];
let openSet = [];
let closedSet = [];
let solving = false;
let generating = false;

// Cell class
class Cell {
    constructor(i, j) {
        this.i = i;
        this.j = j;
        // top, right, bottom, left
        this.walls = [true, true, true, true]; 
        this.visited = false;
        
        // For A*
        this.f = 0;
        this.g = 0;
        this.h = 0;
        this.previous = undefined;
    }

    checkNeighbors() {
        let neighbors = [];
        let top = grid[index(this.i, this.j - 1)];
        let right = grid[index(this.i + 1, this.j)];
        let bottom = grid[index(this.i, this.j + 1)];
        let left = grid[index(this.i - 1, this.j)];

        if (top && !top.visited) neighbors.push(top);
        if (right && !right.visited) neighbors.push(right);
        if (bottom && !bottom.visited) neighbors.push(bottom);
        if (left && !left.visited) neighbors.push(left);

        if (neighbors.length > 0) {
            let r = Math.floor(Math.random() * neighbors.length);
            return neighbors[r];
        } else {
            return undefined;
        }
    }
    
    // For A* neighbors (respecting walls)
    getValidNeighbors() {
        let neighbors = [];
        let top = grid[index(this.i, this.j - 1)];
        let right = grid[index(this.i + 1, this.j)];
        let bottom = grid[index(this.i, this.j + 1)];
        let left = grid[index(this.i - 1, this.j)];

        // Check walls: 0:top, 1:right, 2:bottom, 3:left
        if (top && !this.walls[0]) neighbors.push(top);
        if (right && !this.walls[1]) neighbors.push(right);
        if (bottom && !this.walls[2]) neighbors.push(bottom);
        if (left && !this.walls[3]) neighbors.push(left);
        
        return neighbors;
    }

    show() {
        let x = this.i * w;
        let y = this.j * w;
        
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        
        ctx.beginPath();
        if (this.walls[0]) { ctx.moveTo(x, y); ctx.lineTo(x + w, y); }
        if (this.walls[1]) { ctx.moveTo(x + w, y); ctx.lineTo(x + w, y + w); }
        if (this.walls[2]) { ctx.moveTo(x + w, y + w); ctx.lineTo(x, y + w); }
        if (this.walls[3]) { ctx.moveTo(x, y + w); ctx.lineTo(x, y); }
        ctx.stroke();

        if (this.visited) {
            ctx.fillStyle = '#111';
            ctx.fillRect(x, y, w, w);
        }
    }
    
    highlight(color) {
        let x = this.i * w;
        let y = this.j * w;
        ctx.fillStyle = color;
        ctx.fillRect(x + 2, y + 2, w - 4, w - 4);
    }
}

function index(i, j) {
    if (i < 0 || j < 0 || i > cols - 1 || j > rows - 1) return -1;
    return i + j * cols;
}

function removeWalls(a, b) {
    let x = a.i - b.i;
    if (x === 1) {
        a.walls[3] = false;
        b.walls[1] = false;
    } else if (x === -1) {
        a.walls[1] = false;
        b.walls[3] = false;
    }
    let y = a.j - b.j;
    if (y === 1) {
        a.walls[0] = false;
        b.walls[2] = false;
    } else if (y === -1) {
        a.walls[2] = false;
        b.walls[0] = false;
    }
}

function setup() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    cols = Math.floor(canvas.width / w);
    rows = Math.floor(canvas.height / w);
    
    grid = [];
    for (let j = 0; j < rows; j++) {
        for (let i = 0; i < cols; i++) {
            let cell = new Cell(i, j);
            grid.push(cell);
        }
    }
    
    current = grid[0];
    start = grid[0];
    end = grid[grid.length - 1];
    
    // Initial draw
    background();
    for (let i = 0; i < grid.length; i++) {
        grid[i].show();
    }
}

function background() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Animation loop for generation
function generateStep() {
    if (!generating) return;

    // Speed up generation by doing multiple steps per frame
    for(let k=0; k<5; k++) {
        current.visited = true;
        let next = current.checkNeighbors();
        if (next) {
            next.visited = true;
            stack.push(current);
            removeWalls(current, next);
            current = next;
        } else if (stack.length > 0) {
            current = stack.pop();
        } else {
            generating = false;
            statusDiv.textContent = 'Maze Generated';
            btnGenerate.disabled = false;
            btnSolve.disabled = false;
            drawMaze(); // Final cleanup draw
            return;
        }
    }

    drawMaze();
    // Highlight current
    current.highlight('#00ff88');
    
    if (generating) {
        requestAnimationFrame(generateStep);
    }
}

function drawMaze() {
    background();
    for (let i = 0; i < grid.length; i++) {
        grid[i].show();
    }
    // Highlight start and end
    start.highlight('#00ff00');
    end.highlight('#ff0000');
}

// Heuristic for A*
function heuristic(a, b) {
    // Euclidean distance
    return Math.sqrt(Math.pow(a.i - b.i, 2) + Math.pow(a.j - b.j, 2));
}

function solveStep() {
    if (!solving) return;

    if (openSet.length > 0) {
        let winner = 0;
        for (let i = 0; i < openSet.length; i++) {
            if (openSet[i].f < openSet[winner].f) {
                winner = i;
            }
        }
        
        var currentCell = openSet[winner];
        
        if (currentCell === end) {
            solving = false;
            statusDiv.textContent = 'Maze Solved!';
            btnGenerate.disabled = false;
            btnSolve.disabled = false;
            
            // Reconstruct path
            path = [];
            let temp = currentCell;
            path.push(temp);
            while (temp.previous) {
                path.push(temp.previous);
                temp = temp.previous;
            }
            drawMaze();
            drawPath();
            return;
        }
        
        // Remove current from openSet
        openSet.splice(winner, 1);
        closedSet.push(currentCell);
        
        let neighbors = currentCell.getValidNeighbors();
        for (let i = 0; i < neighbors.length; i++) {
            let neighbor = neighbors[i];
            
            if (!closedSet.includes(neighbor)) {
                let tempG = currentCell.g + 1;
                
                let newPath = false;
                if (openSet.includes(neighbor)) {
                    if (tempG < neighbor.g) {
                        neighbor.g = tempG;
                        newPath = true;
                    }
                } else {
                    neighbor.g = tempG;
                    newPath = true;
                    openSet.push(neighbor);
                }
                
                if (newPath) {
                    neighbor.h = heuristic(neighbor, end);
                    neighbor.f = neighbor.g + neighbor.h;
                    neighbor.previous = currentCell;
                }
            }
        }
    } else {
        // No solution
        solving = false;
        statusDiv.textContent = 'No Solution';
        btnGenerate.disabled = false;
        btnSolve.disabled = false;
        return;
    }
    
    drawMaze();
    
    // Draw Open Set
    for (let i = 0; i < openSet.length; i++) {
        openSet[i].highlight('rgba(0, 255, 0, 0.2)');
    }
    // Draw Closed Set
    for (let i = 0; i < closedSet.length; i++) {
        closedSet[i].highlight('rgba(255, 0, 0, 0.2)');
    }
    
    // Draw current path
    path = [];
    let temp = currentCell;
    path.push(temp);
    while (temp.previous) {
        path.push(temp.previous);
        temp = temp.previous;
    }
    drawPath();

    if (solving) {
        requestAnimationFrame(solveStep);
    }
}

function drawPath() {
    ctx.beginPath();
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = w / 2;
    ctx.lineCap = 'round';
    ctx.noFill;
    
    for (let i = 0; i < path.length; i++) {
        let x = path[i].i * w + w / 2;
        let y = path[i].j * w + w / 2;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.stroke();
}

function startGeneration() {
    if (generating || solving) return;
    setup();
    generating = true;
    solving = false;
    btnGenerate.disabled = true;
    btnSolve.disabled = true;
    statusDiv.textContent = 'Generating Maze...';
    generateStep();
}

function startSolving() {
    if (generating || solving) return;
    solving = true;
    btnGenerate.disabled = true;
    btnSolve.disabled = true;
    statusDiv.textContent = 'Solving Maze...';
    
    openSet = [];
    closedSet = [];
    path = [];
    
    // Reset A* props
    for (let i = 0; i < grid.length; i++) {
        grid[i].f = 0;
        grid[i].g = 0;
        grid[i].h = 0;
        grid[i].previous = undefined;
    }
    
    openSet.push(start);
    solveStep();
}

btnGenerate.addEventListener('click', startGeneration);
btnSolve.addEventListener('click', startSolving);
window.addEventListener('resize', () => {
    if (!generating && !solving) setup();
});

// Start immediately
startGeneration();
