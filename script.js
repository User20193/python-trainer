const canvas = document.getElementById('gridCanvas');
const ctx = canvas.getContext('2d');

const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const clearBtn = document.getElementById('clearBtn');
const randomBtn = document.getElementById('randomBtn');
const speedRange = document.getElementById('speedRange');

const cellSize = 10;
const cols = canvas.width / cellSize;
const rows = canvas.height / cellSize;

let grid = createGrid();
let isRunning = false;
let animationId;
let updateInterval = parseInt(speedRange.value);
let lastUpdateTime = 0;
let isDrawing = false;

function createGrid() {
    return new Array(cols).fill(null)
        .map(() => new Array(rows).fill(0));
}

function randomizeGrid() {
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            grid[i][j] = Math.random() > 0.85 ? 1 : 0;
        }
    }
}

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#4CAF50';
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            if (grid[i][j] === 1) {
                ctx.fillRect(i * cellSize, j * cellSize, cellSize - 1, cellSize - 1);
            }
        }
    }
}

function updateGrid() {
    let newGrid = createGrid();
    for (let i = 0; i < cols; i++) {
        for (let j = 0; j < rows; j++) {
            let neighbors = countNeighbors(i, j);
            if (grid[i][j] === 1 && (neighbors === 2 || neighbors === 3)) {
                newGrid[i][j] = 1;
            } else if (grid[i][j] === 0 && neighbors === 3) {
                newGrid[i][j] = 1;
            } else {
                newGrid[i][j] = 0;
            }
        }
    }
    grid = newGrid;
}

function countNeighbors(x, y) {
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

function gameLoop(timestamp) {
    if (!isRunning) return;

    if (timestamp - lastUpdateTime > updateInterval) {
        updateGrid();
        drawGrid();
        lastUpdateTime = timestamp;
    }

    animationId = requestAnimationFrame(gameLoop);
}

startBtn.addEventListener('click', () => {
    if (!isRunning) {
        isRunning = true;
        lastUpdateTime = performance.now();
        requestAnimationFrame(gameLoop);
    }
});

pauseBtn.addEventListener('click', () => {
    isRunning = false;
    cancelAnimationFrame(animationId);
});

clearBtn.addEventListener('click', () => {
    isRunning = false;
    cancelAnimationFrame(animationId);
    grid = createGrid();
    drawGrid();
});

randomBtn.addEventListener('click', () => {
    randomizeGrid();
    drawGrid();
});

speedRange.addEventListener('input', (e) => {
    updateInterval = parseInt(e.target.value);
});

canvas.addEventListener('mousedown', (e) => {
    isDrawing = true;
    toggleCell(e);
});

canvas.addEventListener('mousemove', (e) => {
    if (isDrawing) {
        toggleCell(e);
    }
});

window.addEventListener('mouseup', () => {
    isDrawing = false;
});

function toggleCell(e) {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) / cellSize);
    const y = Math.floor((e.clientY - rect.top) / cellSize);

    if (x >= 0 && x < cols && y >= 0 && y < rows) {
        grid[x][y] = 1;
        drawGrid();
    }
}

drawGrid();
