const gameBoard = document.getElementById('game-board');
const scoreElement = document.getElementById('score');
const startBtn = document.getElementById('start-btn');

let snake = [{ x: 10, y: 10 }];
let food = { x: 15, y: 15 };
let direction = { x: 0, y: 0 };
let lastInputDirection = { x: 0, y: 0 };
let score = 0;
let gameInterval;
let gameSpeed = 5;
let lastRenderTime = 0;
let gameOver = false;

const GRID_SIZE = 20;

function main(currentTime) {
    if (gameOver) {
        if (confirm('Game Over! Press OK to restart.')) {
            resetGame();
        }
        return;
    }

    window.requestAnimationFrame(main);
    const secondsSinceLastRender = (currentTime - lastRenderTime) / 1000;
    if (secondsSinceLastRender < 1 / gameSpeed) return;

    lastRenderTime = currentTime;

    update();
    draw();
}

function update() {
    const inputDirection = getInputDirection();
    for (let i = snake.length - 2; i >= 0; i--) {
        snake[i + 1] = { ...snake[i] };
    }

    snake[0].x += inputDirection.x;
    snake[0].y += inputDirection.y;

    // Check for food collision
    if (snake[0].x === food.x && snake[0].y === food.y) {
        expandSnake();
        score++;
        scoreElement.innerText = score;
        generateFood();
        gameSpeed += 0.2; // Increase speed slightly
    }

    // Check for wall or self collision
    if (checkCollision()) {
        gameOver = true;
    }
}

function draw() {
    gameBoard.innerHTML = '';
    
    // Draw Snake
    snake.forEach(segment => {
        const snakeElement = document.createElement('div');
        snakeElement.style.gridRowStart = segment.y;
        snakeElement.style.gridColumnStart = segment.x;
        snakeElement.classList.add('snake');
        gameBoard.appendChild(snakeElement);
    });

    // Draw Food
    const foodElement = document.createElement('div');
    foodElement.style.gridRowStart = food.y;
    foodElement.style.gridColumnStart = food.x;
    foodElement.classList.add('food');
    gameBoard.appendChild(foodElement);
}

function expandSnake() {
    snake.push({ ...snake[snake.length - 1] });
}

function generateFood() {
    let newFoodPosition;
    while (newFoodPosition == null || onSnake(newFoodPosition)) {
        newFoodPosition = {
            x: Math.floor(Math.random() * GRID_SIZE) + 1,
            y: Math.floor(Math.random() * GRID_SIZE) + 1
        };
    }
    food = newFoodPosition;
}

function onSnake(position, { ignoreHead = false } = {}) {
    return snake.some((segment, index) => {
        if (ignoreHead && index === 0) return false;
        return segment.x === position.x && segment.y === position.y;
    });
}

function checkCollision() {
    // Wall Collision
    if (
        snake[0].x < 1 || snake[0].x > GRID_SIZE ||
        snake[0].y < 1 || snake[0].y > GRID_SIZE
    ) {
        return true;
    }
    
    // Self Collision
    if (onSnake(snake[0], { ignoreHead: true })) {
        return true;
    }
    
    return false;
}

function getInputDirection() {
    lastInputDirection = direction;
    return direction;
}

function resetGame() {
    snake = [{ x: 10, y: 10 }];
    food = { x: 15, y: 15 };
    direction = { x: 0, y: 0 };
    lastInputDirection = { x: 0, y: 0 };
    score = 0;
    scoreElement.innerText = score;
    gameSpeed = 5;
    gameOver = false;
    lastRenderTime = 0;
    window.requestAnimationFrame(main);
}

window.addEventListener('keydown', e => {
    switch (e.key) {
        case 'ArrowUp':
            if (lastInputDirection.y !== 0) break;
            direction = { x: 0, y: -1 };
            break;
        case 'ArrowDown':
            if (lastInputDirection.y !== 0) break;
            direction = { x: 0, y: 1 };
            break;
        case 'ArrowLeft':
            if (lastInputDirection.x !== 0) break;
            direction = { x: -1, y: 0 };
            break;
        case 'ArrowRight':
            if (lastInputDirection.x !== 0) break;
            direction = { x: 1, y: 0 };
            break;
    }
    
    // Start game on first key press if not started
    if (!gameInterval && !gameOver) {
        // Just ensuring direction is set starts the movement in update()
    }
});

startBtn.addEventListener('click', () => {
    resetGame();
    // Start moving right by default
    direction = { x: 1, y: 0 }; 
});

// Initial draw
draw();